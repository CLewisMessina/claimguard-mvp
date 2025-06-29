# src/ui_components.py
"""
ClaimGuard UI Components - STREAMLINED VERSION
Enhanced interface elements for professional healthcare application
Focus on business value, performance clutter removed
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def render_claim_summary_card(claim_data: Dict, validation_results: List) -> None:
    """Render a summary card for an individual claim"""
    
    # Determine overall status
    if not validation_results:
        status = "✅ VALID"
        status_color = "#7ed321"  # Machinify green
        bg_color = "#f0fdf4"
    else:
        high_severity = any(r.severity == "HIGH" for r in validation_results)
        if high_severity:
            status = "🚨 REJECT"
            status_color = "#dc2626"
            bg_color = "#fee2e2"
        else:
            status = "⚠️ REVIEW"
            status_color = "#f59e0b"
            bg_color = "#fef3c7"
    
    # Create claim card
    st.markdown(f"""
    <div style="
        background-color: {bg_color}; 
        border: 2px solid {status_color}; 
        border-radius: 10px; 
        padding: 1rem; 
        margin: 1rem 0;
    ">
        <div style="display: flex; justify-content: between; align-items: center;">
            <h3 style="color: {status_color}; margin: 0;">
                Claim {claim_data.get('claim_id', 'Unknown')} - {status}
            </h3>
        </div>
        <div style="margin-top: 0.5rem;">
            <p><strong>Patient:</strong> {claim_data.get('age', 'N/A')} year old {claim_data.get('gender', 'N/A')}</p>
            <p><strong>Procedure:</strong> {claim_data.get('cpt_code', 'N/A')} | <strong>Diagnosis:</strong> {claim_data.get('diagnosis_code', 'N/A')}</p>
            <p><strong>Amount:</strong> ${claim_data.get('charge_amount', 'N/A')} | <strong>Date:</strong> {claim_data.get('service_date', 'N/A')}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_processing_progress(current_step: int, total_steps: int, step_name: str) -> None:
    """Render simplified progress bar for validation processing"""
    
    progress_percent = current_step / total_steps
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <h4>🔄 Processing: {step_name}</h4>
        <div style="
            background-color: #e5e7eb; 
            border-radius: 10px; 
            height: 20px; 
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #7ed321, #6bb91a); 
                height: 100%; 
                width: {progress_percent * 100}%; 
                transition: width 0.3s ease;
            "></div>
        </div>
        <p style="margin-top: 0.5rem; color: #667085;">
            Step {current_step} of {total_steps} ({progress_percent:.0%} complete)
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_dashboard(validation_results: Dict) -> None:
    """Render streamlined KPI dashboard focused on business value"""
    
    if not validation_results:
        return
    
    summary = validation_results['summary']
    
    st.markdown("### 📊 Validation Results Overview")
    
    # Calculate business impact metrics
    total_claims = summary['total_claims']
    error_claims = summary['claims_with_errors']
    error_rate = summary['error_rate_percent']
    
    # Estimated cost savings (rough calculation for demo)
    avg_claim_value = 1000  # Average claim value assumption
    potential_savings = error_claims * avg_claim_value * 0.15  # 15% average overpayment prevention
    
    # Create streamlined business-focused metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Claims Analyzed",
            value=f"{total_claims:,}",
            help="Total number of claims processed for validation"
        )
    
    with col2:
        st.metric(
            label="🚨 Errors Detected", 
            value=f"{error_claims:,}",
            delta=f"{error_rate:.1f}% error rate",
            delta_color="inverse",
            help="Claims flagged for manual review or rejection"
        )
    
    with col3:
        st.metric(
            label="💰 Potential Savings",
            value=f"${potential_savings:,.0f}",
            help="Estimated cost savings from preventing overpayments"
        )
    
    with col4:
        processing_time = summary['processing_time_seconds']
        st.metric(
            label="⚡ Processing Time",
            value=f"{processing_time:.1f}s",
            delta="Real-time analysis",
            help="Total time to analyze all claims with AI"
        )

def render_simplified_ai_summary(ai_explanations: Dict[str, Any]):
    """Render simplified AI analysis summary focused on business value"""
    if not ai_explanations:
        return
    
    st.markdown("### 🤖 AI Analysis Summary")
    
    # Calculate AI analysis metrics
    total_analyses = len(ai_explanations)
    risk_levels = [exp.risk_level for exp in ai_explanations.values()]
    avg_confidence = sum(exp.confidence for exp in ai_explanations.values()) / total_analyses
    
    risk_counts = {
        'HIGH': risk_levels.count('HIGH'),
        'MEDIUM': risk_levels.count('MEDIUM'),
        'LOW': risk_levels.count('LOW')
    }
    
    # Simple business-focused metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🧠 AI Analyses Generated",
            value=f"{total_analyses}",
            help="Number of detailed AI explanations provided"
        )
    
    with col2:
        st.metric(
            label="🚨 High Risk Claims",
            value=f"{risk_counts['HIGH']}",
            delta=f"{(risk_counts['HIGH']/total_analyses*100):.0f}% of analyzed",
            delta_color="inverse",
            help="Claims requiring immediate attention"
        )
    
    with col3:
        st.metric(
            label="🎯 AI Confidence",
            value=f"{avg_confidence:.0%}",
            help="Average confidence in AI analysis accuracy"
        )

def render_error_trend_chart(validation_results: Dict) -> None:
    """Render simplified error trend analysis chart"""
    
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
        # Error distribution by type
        error_counts = df_errors['Error_Type'].value_counts()
        fig_bar = px.bar(
            x=error_counts.index,
            y=error_counts.values,
            title="Errors by Type",
            color=error_counts.values,
            color_continuous_scale=[[0, '#7ed321'], [0.5, '#f59e0b'], [1, '#dc2626']]
        )
        fig_bar.update_layout(
            height=400,
            xaxis_title="Error Type",
            yaxis_title="Number of Claims",
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Severity distribution
        severity_counts = df_errors['Severity'].value_counts()
        fig_pie = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Error Severity Distribution",
            color=severity_counts.index,
            color_discrete_map={'HIGH': '#dc2626', 'MEDIUM': '#f59e0b', 'LOW': '#7ed321'}
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

def render_claim_details_table(uploaded_data: pd.DataFrame, validation_results: Dict) -> None:
    """Render interactive table with claim details and validation status"""
    
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
    
    # Add filtering options
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
    
    # Display filtered table
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

def render_business_impact_summary(validation_results: Dict, uploaded_data: pd.DataFrame) -> None:
    """Render business impact analysis with Machinify styling"""
    
    if not validation_results or uploaded_data is None:
        return
    
    st.markdown("### 💼 Business Impact Analysis")
    
    # Calculate financial impact
    total_amount = uploaded_data['charge_amount'].sum()
    flagged_claims = set(r.claim_id for r in validation_results['validation_results'])
    flagged_amount = uploaded_data[
        uploaded_data['claim_id'].astype(str).isin(flagged_claims)
    ]['charge_amount'].sum()
    
    # Estimated savings calculation
    estimated_savings = flagged_amount * 0.15  # 15% average overpayment prevention
    processing_cost_saved = len(flagged_claims) * 50  # $50 per claim processing cost
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="business-impact-card">
            <h3>💰 Financial Impact</h3>
            <p><strong>Total Claims Value:</strong> ${total_amount:,.2f}</p>
            <p><strong>Flagged Claims Value:</strong> ${flagged_amount:,.2f}</p>
            <p><strong>Estimated Savings:</strong> ${estimated_savings:,.2f}</p>
            <p><strong>Processing Cost Saved:</strong> ${processing_cost_saved:,.2f}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <h4>Total ROI: ${(estimated_savings + processing_cost_saved):,.2f}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="operational-metrics-card">
            <h3>📊 Operational Excellence</h3>
            <p><strong>Claims Processed:</strong> {len(uploaded_data):,}/hour</p>
            <p><strong>Error Detection Rate:</strong> {(len(flagged_claims)/len(uploaded_data)*100):.1f}%</p>
            <p><strong>Average Processing:</strong> {validation_results['summary']['processing_time_seconds']*1000:.0f}ms/claim</p>
            <p><strong>Manual Review Reduction:</strong> 85%</p>
            <hr style="border-color: rgba(126, 211, 33, 0.3);">
            <h4>Efficiency Gain: {(len(uploaded_data)/validation_results['summary']['processing_time_seconds']/60):.0f}x faster</h4>
        </div>
        """, unsafe_allow_html=True)

def render_action_recommendations(validation_results: Dict) -> None:
    """Render actionable recommendations with Machinify styling"""
    
    if not validation_results or not validation_results['validation_results']:
        return
    
    st.markdown("### 🎯 Recommended Actions")
    
    # Analyze validation results for recommendations
    error_types = {}
    high_priority_claims = []
    
    for result in validation_results['validation_results']:
        # Count error types
        error_type = result.error_type
        if error_type not in error_types:
            error_types[error_type] = 0
        error_types[error_type] += 1
        
        # Identify high priority claims
        if result.severity == "HIGH":
            high_priority_claims.append(result.claim_id)
    
    # Generate recommendations with Machinify styling
    recommendations = []
    
    if "Gender-Procedure Mismatch" in error_types:
        count = error_types["Gender-Procedure Mismatch"]
        recommendations.append({
            "priority": "URGENT",
            "action": "Immediate Review Required",
            "description": f"Review {count} claims with gender-procedure mismatches for potential data entry errors or fraud.",
            "timeline": "Within 24 hours"
        })
    
    if "Age-Procedure Mismatch" in error_types:
        count = error_types["Age-Procedure Mismatch"]
        recommendations.append({
            "priority": "HIGH",
            "action": "Medical Necessity Review",
            "description": f"Verify medical necessity for {count} age-inappropriate procedures.",
            "timeline": "Within 3 days"
        })
    
    if "Anatomical Logic Error" in error_types:
        count = error_types["Anatomical Logic Error"]
        recommendations.append({
            "priority": "HIGH",
            "action": "Coding Accuracy Check",
            "description": f"Audit {count} claims with anatomical inconsistencies for coding errors.",
            "timeline": "Within 24 hours"
        })
    
    if len(high_priority_claims) > 0:
        recommendations.append({
            "priority": "URGENT",
            "action": "Immediate Payment Hold",
            "description": f"Place payment hold on {len(set(high_priority_claims))} high-risk claims pending manual review.",
            "timeline": "Immediate"
        })
    
    # Display recommendations with Machinify styling
    for rec in recommendations:
        priority_class = f"recommendation-{rec['priority'].lower()}"
        
        if rec["priority"] == "URGENT":
            icon = "🚨"
        elif rec["priority"] == "HIGH":
            icon = "⚠️"
        else:
            icon = "ℹ️"
        
        st.markdown(f"""
        <div class="{priority_class}">
            <h4>{icon} {rec['action']} ({rec['priority']} Priority)</h4>
            <p><strong>Description:</strong> {rec['description']}</p>
            <p><strong>Timeline:</strong> {rec['timeline']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_demo_mode_banner() -> None:
    """Render demo mode banner with Machinify styling"""
    
    st.markdown("""
    <div class="demo-banner">
        <strong>🎯 DEMO MODE</strong> - Healthcare Claims Validation System
    </div>
    """, unsafe_allow_html=True)

def render_footer() -> None:
    """Render application footer with Machinify styling"""
    
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>ClaimGuard</strong> - Pre-payment Healthcare Claims Validation</p>
        <p>Built with Machinify-inspired design principles</p>
        <p><em>Preventing healthcare payment errors before they occur</em></p>
    </div>
    """, unsafe_allow_html=True)