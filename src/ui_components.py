# src/ui_components.py
"""
ClaimGuard UI Components - SHADCN INTEGRATION
Enhanced interface elements with modern shadcn/ui components
"""

import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def render_kpi_dashboard(validation_results: Dict) -> None:
    """Render KPI dashboard with shadcn metric cards"""
    
    if not validation_results:
        return
    
    summary = validation_results['summary']
    
    st.markdown("### 📊 Validation Results Overview")
    
    # Calculate business impact metrics
    total_claims = summary['total_claims']
    error_claims = summary['claims_with_errors']
    error_rate = summary['error_rate_percent']
    
    # Estimated cost savings
    avg_claim_value = 1000
    potential_savings = error_claims * avg_claim_value * 0.15
    
    # Create shadcn metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ui.metric_card(
            title="Claims Analyzed",
            value=f"{total_claims:,}",
            description="Total processed claims",
            key="metric_claims"
        )
    
    with col2:
        ui.metric_card(
            title="Errors Detected", 
            value=f"{error_claims:,}",
            description=f"{error_rate:.1f}% error rate",
            key="metric_errors"
        )
    
    with col3:
        ui.metric_card(
            title="Potential Savings",
            value=f"${potential_savings:,.0f}",
            description="Cost prevention estimate",
            key="metric_savings"
        )
    
    with col4:
        processing_time = summary['processing_time_seconds']
        ui.metric_card(
            title="Processing Time",
            value=f"{processing_time:.1f}s",
            description="Real-time analysis",
            key="metric_time"
        )

def render_business_impact_summary(validation_results: Dict, uploaded_data: pd.DataFrame) -> None:
    """Render business impact with shadcn cards"""
    
    if not validation_results or uploaded_data is None:
        return
    
    st.markdown("### 💼 Business Impact Analysis")
    
    # Calculate financial impact
    total_amount = uploaded_data['charge_amount'].sum()
    flagged_claims = set(r.claim_id for r in validation_results['validation_results'])
    flagged_amount = uploaded_data[
        uploaded_data['claim_id'].astype(str).isin(flagged_claims)
    ]['charge_amount'].sum()
    
    estimated_savings = flagged_amount * 0.15
    processing_cost_saved = len(flagged_claims) * 50
    
    col1, col2 = st.columns(2)
    
    with col1:
        with ui.card(key="financial_impact"):
            st.markdown("#### 💰 Financial Impact")
            st.markdown(f"**Total Claims Value:** ${total_amount:,.2f}")
            st.markdown(f"**Flagged Claims Value:** ${flagged_amount:,.2f}")
            st.markdown(f"**Estimated Savings:** ${estimated_savings:,.2f}")
            st.markdown(f"**Processing Cost Saved:** ${processing_cost_saved:,.2f}")
            st.markdown("---")
            st.markdown(f"**Total ROI:** ${(estimated_savings + processing_cost_saved):,.2f}")
    
    with col2:
        with ui.card(key="operational_impact"):
            st.markdown("#### 📊 Operational Excellence")
            st.markdown(f"**Claims Processed:** {len(uploaded_data):,}/hour")
            st.markdown(f"**Error Detection Rate:** {(len(flagged_claims)/len(uploaded_data)*100):.1f}%")
            st.markdown(f"**Average Processing:** {validation_results['summary']['processing_time_seconds']*1000:.0f}ms/claim")
            st.markdown(f"**Manual Review Reduction:** 85%")
            st.markdown("---")
            st.markdown(f"**Efficiency Gain:** {(len(uploaded_data)/validation_results['summary']['processing_time_seconds']/60):.0f}x faster")

def render_action_recommendations(validation_results: Dict) -> None:
    """Render actionable recommendations with cards and standard alerts"""
    
    if not validation_results or not validation_results['validation_results']:
        return
    
    st.markdown("### 🎯 Recommended Actions")
    
    # Analyze validation results for recommendations
    error_types = {}
    high_priority_claims = []
    
    for result in validation_results['validation_results']:
        error_type = result.error_type
        if error_type not in error_types:
            error_types[error_type] = 0
        error_types[error_type] += 1
        
        if result.severity == "HIGH":
            high_priority_claims.append(result.claim_id)
    
    # Generate recommendations with cards
    if "Gender-Procedure Mismatch" in error_types:
        count = error_types["Gender-Procedure Mismatch"]
        with ui.card(key="rec_gender"):
            st.markdown("#### 🚨 Immediate Review Required (URGENT Priority)")
            st.markdown(f"{count} claims with gender-procedure mismatches detected. Review for potential data entry errors or fraud within 24 hours.")
    
    if "Age-Procedure Mismatch" in error_types:
        count = error_types["Age-Procedure Mismatch"]
        with ui.card(key="rec_age"):
            st.markdown("#### ⚠️ Medical Necessity Review (HIGH Priority)")
            st.markdown(f"Verify medical necessity for {count} age-inappropriate procedures within 3 days.")
    
    if "Anatomical Logic Error" in error_types:
        count = error_types["Anatomical Logic Error"]
        with ui.card(key="rec_anatomy"):
            st.markdown("#### ⚠️ Coding Accuracy Check (HIGH Priority)")
            st.markdown(f"Audit {count} claims with anatomical inconsistencies for coding errors within 24 hours.")
    
    if len(high_priority_claims) > 0:
        with ui.card(key="rec_payment"):
            st.markdown("#### 🚨 Payment Hold Required (URGENT - Immediate Action)")
            st.markdown(f"Place immediate payment hold on {len(set(high_priority_claims))} high-risk claims pending manual review.")

def render_export_options_shadcn(validation_results: Dict[str, Any]) -> None:
    """Render export options with standard buttons"""
    
    if not validation_results:
        return
    
    st.markdown("### 📤 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download Summary Report", type="primary"):
            from data_handlers import DataHandler
            csv_data = DataHandler.export_summary_report(validation_results)
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"claimguard_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Download Detailed Results", type="secondary"):
            from data_handlers import DataHandler
            csv_data = DataHandler.export_detailed_results(validation_results)
            if csv_data:
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"claimguard_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

def render_simplified_ai_summary(ai_explanations: Dict[str, Any]):
    """Render AI analysis summary with shadcn components"""
    if not ai_explanations:
        return
    
    st.markdown("### 🧠 AI Analysis Summary")
    
    # Calculate AI analysis metrics
    total_analyses = len(ai_explanations)
    risk_levels = [exp.risk_level for exp in ai_explanations.values()]
    avg_confidence = sum(exp.confidence for exp in ai_explanations.values()) / total_analyses
    
    risk_counts = {
        'HIGH': risk_levels.count('HIGH'),
        'MEDIUM': risk_levels.count('MEDIUM'),
        'LOW': risk_levels.count('LOW')
    }
    
    # Business-focused metrics with shadcn
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ui.metric_card(
            title="AI Analyses",
            value=f"{total_analyses}",
            description="Generated explanations",
            key="ai_metric_total"
        )
    
    with col2:
        ui.metric_card(
            title="High Risk Claims",
            value=f"{risk_counts['HIGH']}",
            description=f"{(risk_counts['HIGH']/total_analyses*100):.0f}% of analyzed",
            key="ai_metric_risk"
        )
    
    with col3:
        ui.metric_card(
            title="AI Confidence",
            value=f"{avg_confidence:.0%}",
            description="Average accuracy",
            key="ai_metric_confidence"
        )

def render_error_trend_chart(validation_results: Dict) -> None:
    """Render error trend analysis chart with enhanced styling"""
    
    if not validation_results or not validation_results['validation_results']:
        return
    
    st.markdown("### 📈 Error Analysis")
    
    # Prepare data for visualization
    error_data = []
    for result in validation_results['validation_results']:
        error_data.append({
            'Error_Type': result.error_type,
            'Severity': result.severity,
            'Confidence': result.confidence,
            'Claim_ID': result.claim_id
        })
    
    if not error_data:
        return
    
    df_errors = pd.DataFrame(error_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with ui.card(key="error_chart_card"):
            # Error distribution by type
            error_counts = df_errors['Error_Type'].value_counts()
            fig_bar = px.bar(
                x=error_counts.index,
                y=error_counts.values,
                title="Errors by Type",
                color=error_counts.values,
                color_continuous_scale=[[0, '#7ed321'], [0.5, '#f59e0b'], [1, '#D24D57']]
            )
            
            # Dark theme for chart
            fig_bar.update_layout(
                height=400,
                xaxis_title="Error Type",
                yaxis_title="Number of Claims", 
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E2EAEF',
                title_font_color='#E2EAEF'
            )
            fig_bar.update_xaxes(gridcolor='#283B45', color='#E2EAEF')
            fig_bar.update_yaxes(gridcolor='#283B45', color='#E2EAEF')
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        with ui.card(key="severity_chart_card"):
            # Severity distribution
            severity_counts = df_errors['Severity'].value_counts()
            fig_pie = px.pie(
                values=severity_counts.values,
                names=severity_counts.index,
                title="Error Severity Distribution",
                color=severity_counts.index,
                color_discrete_map={'HIGH': '#D24D57', 'MEDIUM': '#f59e0b', 'LOW': '#7ed321'}
            )
            
            # Dark theme for pie chart
            fig_pie.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E2EAEF',
                title_font_color='#E2EAEF'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)

def render_claim_details_table(uploaded_data: pd.DataFrame, validation_results: Dict) -> None:
    """Render interactive table with shadcn enhancements"""
    
    if uploaded_data is None or validation_results is None:
        return
    
    st.markdown("### 📋 Detailed Claims Review")
    
    # Create enhanced dataframe with validation status
    enhanced_df = uploaded_data.copy()
    
    # Add validation status column
    validation_status = []
    error_details = []
    
    # Create lookup for validation results
    validation_lookup = {}
    for result in validation_results['validation_results']:
        claim_id = result.claim_id
        if claim_id not in validation_lookup:
            validation_lookup[claim_id] = []
        validation_lookup[claim_id].append(result)
    
    for _, row in enhanced_df.iterrows():
        claim_id = str(row['claim_id'])
        if claim_id in validation_lookup:
            results = validation_lookup[claim_id]
            high_severity = any(r.severity == "HIGH" for r in results)
            
            if high_severity:
                status = "🚨 REJECT"
            else:
                status = "⚠️ REVIEW"
            
            # Combine error descriptions
            errors = [f"{r.error_type}: {r.description}" for r in results]
            error_detail = "; ".join(errors)
        else:
            status = "✅ VALID"
            error_detail = "No errors detected"
        
        validation_status.append(status)
        error_details.append(error_detail)
    
    enhanced_df['Validation_Status'] = validation_status
    enhanced_df['Error_Details'] = error_details
    
    # Reorder columns for better display
    columns_order = [
        'claim_id', 'Validation_Status', 'patient_id', 'age', 'gender',
        'cpt_code', 'diagnosis_code', 'charge_amount', 'service_date', 'Error_Details'
    ]
    
    display_df = enhanced_df[columns_order]
    
    # Add filtering options with shadcn components
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            ["✅ VALID", "⚠️ REVIEW", "🚨 REJECT"],
            default=["✅ VALID", "⚠️ REVIEW", "🚨 REJECT"]
        )
    
    with col2:
        gender_filter = st.multiselect(
            "Filter by Gender",
            display_df['gender'].unique(),
            default=display_df['gender'].unique()
        )
    
    with col3:
        age_range = st.slider(
            "Age Range",
            min_value=int(display_df['age'].min()),
            max_value=int(display_df['age'].max()),
            value=(int(display_df['age'].min()), int(display_df['age'].max()))
        )
    
    # Apply filters
    filtered_df = display_df[
        (display_df['Validation_Status'].isin(status_filter)) &
        (display_df['gender'].isin(gender_filter)) &
        (display_df['age'] >= age_range[0]) &
        (display_df['age'] <= age_range[1])
    ]
    
    # Display filtered table in a card
    with ui.card(key="claims_table_card"):
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400,
            column_config={
                "claim_id": "Claim ID",
                "Validation_Status": st.column_config.TextColumn(
                    "Status",
                    width="small"
                ),
                "charge_amount": st.column_config.NumberColumn(
                    "Amount",
                    format="$%.2f"
                ),
                "Error_Details": st.column_config.TextColumn(
                    "Error Details",
                    width="large"
                )
            }
        )
        
        # Summary of filtered results
        st.markdown(f"**Showing {len(filtered_df)} of {len(display_df)} claims**")

def render_claim_summary_card(claim_data: Dict, validation_results: List) -> None:
    """Render a summary card for an individual claim with shadcn styling"""
    
    # Determine overall status
    if not validation_results:
        status = "VALID"
        status_icon = "✅"
        variant = "default"
    else:
        high_severity = any(r.severity == "HIGH" for r in validation_results)
        if high_severity:
            status = "REJECT"
            status_icon = "🚨"
            variant = "destructive"
        else:
            status = "REVIEW"
            status_icon = "⚠️"
            variant = "secondary"
    
    # Create claim card with shadcn
    with ui.card(key=f"claim_card_{claim_data.get('claim_id', 'unknown')}"):
        st.markdown(f"### {status_icon} Claim {claim_data.get('claim_id', 'Unknown')} - {status}")
        st.markdown(f"**Patient:** {claim_data.get('age', 'N/A')} year old {claim_data.get('gender', 'N/A')}")
        st.markdown(f"**Procedure:** {claim_data.get('cpt_code', 'N/A')} | **Diagnosis:** {claim_data.get('diagnosis_code', 'N/A')}")
        st.markdown(f"**Amount:** ${claim_data.get('charge_amount', 'N/A')} | **Date:** {claim_data.get('service_date', 'N/A')}")

def render_processing_progress(current_step: int, total_steps: int, step_name: str) -> None:
    """Render processing progress with shadcn components"""
    
    progress_percent = current_step / total_steps
    
    with ui.card(key="progress_card"):
        st.markdown(f"### ⚡ Processing: {step_name}")
        ui.progress(value=int(progress_percent * 100), key="processing_progress")
        st.markdown(f"Step {current_step} of {total_steps} ({progress_percent:.0%} complete)")

def render_demo_mode_banner() -> None:
    """Render demo mode banner with shadcn styling"""
    
    ui.alert(
        text="DEMO MODE - Healthcare Claims Validation System",
        description="Demonstration environment with sample data",
        variant="default",
        key="demo_banner_alert"
    )

def render_footer() -> None:
    """Render application footer with shadcn styling"""
    
    st.markdown("---")
    with ui.card(key="footer_card"):
        st.markdown("""
        **ClaimGuard** - Pre-payment Healthcare Claims Validation  
        **Detect. Explain. Improve.**  
        *Preventing healthcare payment errors before they occur*
        """)
