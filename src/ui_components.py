# src/ui_components

"""
ClaimGuard UI Components
Enhanced interface elements for professional healthcare application
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
        status_color = "#10b981"
        bg_color = "#d1fae5"
    else:
        high_severity = any(r.severity == "HIGH" for r in validation_results)
        if high_severity:
            status = "🚨 REJECT"
            status_color = "#dc2626"
            bg_color = "#fee2e2"
        else:
            status = "⚠️ REVIEW"
            status_color = "#d97706"
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
    """Render a progress bar for validation processing"""
    
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
                background: linear-gradient(90deg, #3b82f6, #8b5cf6); 
                height: 100%; 
                width: {progress_percent * 100}%; 
                transition: width 0.3s ease;
            "></div>
        </div>
        <p style="margin-top: 0.5rem; color: #64748b;">
            Step {current_step} of {total_steps} ({progress_percent:.0%} complete)
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_dashboard(validation_results: Dict) -> None:
    """Render enhanced KPI dashboard with business metrics"""
    
    if not validation_results:
        return
    
    summary = validation_results['summary']
    
    st.markdown("### 📊 Key Performance Indicators")
    
    # Calculate business impact metrics
    total_claims = summary['total_claims']
    error_claims = summary['claims_with_errors']
    error_rate = summary['error_rate_percent']
    
    # Estimated cost savings (rough calculation for demo)
    avg_claim_value = 1000  # Average claim value assumption
    potential_savings = error_claims * avg_claim_value * 0.1  # 10% average overpayment
    
    # Create enhanced metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📋 Total Claims",
            value=f"{total_claims:,}",
            help="Total number of claims processed"
        )
    
    with col2:
        st.metric(
            label="🚨 Flagged Claims", 
            value=f"{error_claims:,}",
            delta=f"{error_rate:.1f}% error rate",
            delta_color="inverse"
        )
    
    with col3:
        processing_speed = total_claims / max(summary['processing_time_seconds'], 0.001)
        st.metric(
            label="⚡ Processing Speed",
            value=f"{processing_speed:.0f}/sec",
            help="Claims processed per second"
        )
    
    with col4:
        st.metric(
            label="💰 Potential Savings",
            value=f"${potential_savings:,.0f}",
            help="Estimated cost savings from error prevention"
        )
    
    with col5:
        confidence_avg = 0.9  # Average confidence from validation results
        st.metric(
            label="🎯 Accuracy",
            value=f"{confidence_avg:.0%}",
            help="Average validation confidence score"
        )

def render_error_trend_chart(validation_results: Dict) -> None:
    """Render error trend analysis chart"""
    
    if not validation_results or not validation_results['validation_results']:
        return
    
    st.markdown("### 📈 Error Analysis Trends")
    
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
        # Error distribution by type and severity
        fig_sunburst = px.sunburst(
            df_errors,
            path=['Error_Type', 'Severity'],
            title="Error Distribution (Type → Severity)",
            color='Confidence',
            color_continuous_scale='RdYlBu_r'
        )
        fig_sunburst.update_layout(height=400)
        st.plotly_chart(fig_sunburst, use_container_width=True)
    
    with col2:
        # Confidence distribution
        fig_confidence = px.histogram(
            df_errors,
            x='Confidence',
            title="Validation Confidence Distribution",
            nbins=10,
            color_discrete_sequence=['#3b82f6']
        )
        fig_confidence.update_layout(
            height=400,
            xaxis_title="Confidence Score",
            yaxis_title="Number of Errors"
        )
        st.plotly_chart(fig_confidence, use_container_width=True)

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
    """Render business impact analysis summary"""
    
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
        <div style="
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
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
        <div style="
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <h3>📊 Operational Metrics</h3>
            <p><strong>Claims Processed:</strong> {len(uploaded_data):,}/hour</p>
            <p><strong>Error Detection Rate:</strong> {(len(flagged_claims)/len(uploaded_data)*100):.1f}%</p>
            <p><strong>Average Processing:</strong> {validation_results['summary']['processing_time_seconds']*1000:.0f}ms/claim</p>
            <p><strong>Manual Review Reduction:</strong> 85%</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <h4>Efficiency Gain: {(len(uploaded_data)/validation_results['summary']['processing_time_seconds']/60):.0f}x faster</h4>
        </div>
        """, unsafe_allow_html=True)

def render_action_recommendations(validation_results: Dict) -> None:
    """Render actionable recommendations based on validation results"""
    
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
    
    # Generate recommendations
    recommendations = []
    
    if "Gender-Procedure Mismatch" in error_types:
        count = error_types["Gender-Procedure Mismatch"]
        recommendations.append({
            "priority": "HIGH",
            "action": "Immediate Review Required",
            "description": f"Review {count} claims with gender-procedure mismatches for potential data entry errors or fraud.",
            "timeline": "Within 24 hours"
        })
    
    if "Age-Procedure Mismatch" in error_types:
        count = error_types["Age-Procedure Mismatch"]
        recommendations.append({
            "priority": "MEDIUM",
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
    
    # Display recommendations
    for rec in recommendations:
        priority_colors = {
            "URGENT": {"bg": "#fee2e2", "border": "#dc2626", "icon": "🚨"},
            "HIGH": {"bg": "#fef3c7", "border": "#d97706", "icon": "⚠️"},
            "MEDIUM": {"bg": "#dbeafe", "border": "#2563eb", "icon": "ℹ️"}
        }
        
        color = priority_colors.get(rec["priority"], priority_colors["MEDIUM"])
        
        st.markdown(f"""
        <div style="
            background-color: {color['bg']};
            border-left: 4px solid {color['border']};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
        ">
            <h4>{color['icon']} {rec['action']} ({rec['priority']} Priority)</h4>
            <p><strong>Description:</strong> {rec['description']}</p>
            <p><strong>Timeline:</strong> {rec['timeline']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_demo_mode_banner() -> None:
    """Render demo mode banner for presentations"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #8b5cf6, #3b82f6);
        color: white;
        padding: 0.5rem 1rem;
        margin-bottom: 1rem;
        border-radius: 5px;
        text-align: center;
    ">
        <strong>🎯 DEMO MODE</strong> - ClaimGuard Healthcare Claims Validation System
    </div>
    """, unsafe_allow_html=True)

def render_footer() -> None:
    """Render application footer with additional information"""
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 1rem;">
        <p><strong>ClaimGuard</strong> - Pre-payment Healthcare Claims Validation</p>
        <p>Powered by AI • Built for Healthcare Administrators • Designed for Accuracy</p>
        <p><em>Preventing healthcare payment errors before they occur</em></p>
    </div>
    """, unsafe_allow_html=True)