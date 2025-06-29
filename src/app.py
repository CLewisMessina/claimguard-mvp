# src/app.py
"""
Healthcare Claims Validation with AI-Powered Explanations
"""

import streamlit as st
import sys
import os
import time

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import modular components
from session_management import SessionManager
from sidebar_controls import SidebarControls
from validation_ui import ValidationUI
from ai_ui_components import AIUIComponents
from validator import ClaimValidator
from ai_explainer import ClaimExplainer
from ui_components import (
    render_kpi_dashboard, render_error_trend_chart, render_claim_details_table,
    render_business_impact_summary, render_action_recommendations, 
    render_demo_mode_banner, render_footer
)

# Page configuration
st.set_page_config(
    page_title="ClaimGuard - Healthcare Claims Validation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS styling (streamlined version)
def load_custom_css():
    """Load streamlined CSS focused on business value presentation"""
    st.markdown("""
    <style>
        /* Import Satoshi Font */
        @import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700&display=swap');
        
        /* Machinify Brand Colors */
        :root {
            --machinify-dark-navy: #2a3f47;
            --machinify-bright-green: #7ed321;
            --machinify-white: #ffffff;
            --machinify-light-gray: #f5f5f5;
            --machinify-medium-gray: #e8e8e8;
            --machinify-dark-text: #2a3f47;
            --machinify-secondary-text: #667085;
            
            --error-red: #dc2626;
            --warning-orange: #f59e0b;
            --success-green: var(--machinify-bright-green);
            --info-blue: #2563eb;
            
            --font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Global Styles */
        .stApp {
            font-family: var(--font-family);
        }
        
        /* Main Header */
        .main-header {
            background: linear-gradient(135deg, var(--machinify-dark-navy) 0%, #1a2a32 100%);
            color: var(--machinify-white);
            font-size: 2.5rem;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-bottom: 4px solid var(--machinify-bright-green);
            border-radius: 0 0 15px 15px;
        }
        
        .machinify-badge {
            background: var(--machinify-bright-green);
            color: var(--machinify-dark-navy);
            padding: 0.4rem 1rem;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9rem;
            display: inline-block;
            margin-left: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Demo Banner */
        .demo-banner {
            background: linear-gradient(90deg, var(--machinify-dark-navy), var(--machinify-bright-green));
            color: var(--machinify-white);
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
        }
        
        /* Success Card */
        .success-card {
            background: linear-gradient(135deg, var(--machinify-bright-green) 0%, #6bb91a 100%);
            color: var(--machinify-white);
            border-left: 4px solid #5a9f18;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
            font-weight: 500;
        }
        
        /* Error Severity Styling */
        .error-high {
            background-color: #fee2e2;
            border-left: 4px solid var(--error-red);
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        .error-medium {
            background-color: #fef3c7;
            border-left: 4px solid var(--warning-orange);
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        .error-low {
            background-color: #dbeafe;
            border-left: 4px solid var(--info-blue);
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        /* AI Analysis Container */
        .ai-analysis-container {
            background: linear-gradient(135deg, var(--machinify-dark-navy) 0%, #1a2a32 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            color: var(--machinify-white);
            box-shadow: 0 8px 25px rgba(42, 63, 71, 0.2);
            border: 2px solid var(--machinify-bright-green);
        }
        
        .ai-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(126, 211, 33, 0.3);
        }
        
        .ai-section h4 {
            color: var(--machinify-bright-green);
            margin-bottom: 0.5rem;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .ai-section p {
            color: #f1f5f9;
            line-height: 1.6;
            margin-bottom: 0;
        }
        
        /* Risk Indicators */
        .risk-indicator {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .risk-high {
            background-color: var(--error-red);
            color: white;
        }
        
        .risk-medium {
            background-color: var(--warning-orange);
            color: white;
        }
        
        .risk-low {
            background-color: var(--machinify-bright-green);
            color: var(--machinify-dark-navy);
        }
        
        /* Confidence Badge */
        .confidence-badge {
            background: var(--machinify-bright-green);
            color: var(--machinify-dark-navy);
            padding: 0.4rem 1.2rem;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        
        /* AI Powered Banner */
        .ai-powered-banner {
            background: linear-gradient(90deg, var(--machinify-bright-green), var(--machinify-dark-navy));
            color: var(--machinify-white);
            padding: 0.8rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        /* Business Impact Cards */
        .business-impact-card {
            background: linear-gradient(135deg, var(--machinify-bright-green) 0%, #6bb91a 100%);
            color: var(--machinify-white);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(126, 211, 33, 0.2);
        }
        
        .operational-metrics-card {
            background: linear-gradient(135deg, var(--machinify-dark-navy) 0%, #1a2a32 100%);
            color: var(--machinify-white);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(42, 63, 71, 0.2);
            border: 2px solid var(--machinify-bright-green);
        }
        
        .business-impact-card h3, .operational-metrics-card h3 {
            margin-top: 0;
            font-weight: 700;
            font-size: 1.3rem;
        }
        
        .operational-metrics-card h3 {
            color: var(--machinify-bright-green);
        }
        
        /* Sidebar Styling */
        .sidebar-info {
            background: var(--machinify-light-gray);
            border: 2px solid var(--machinify-medium-gray);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .sidebar-info h3 {
            color: var(--machinify-dark-navy);
            margin-top: 0;
            font-weight: 700;
        }
        
        /* Button Styling */
        .stButton > button {
            background: var(--machinify-bright-green) !important;
            color: var(--machinify-dark-navy) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s ease !important;
            font-family: var(--font-family) !important;
        }
        
        .stButton > button:hover {
            background: #6bb91a !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.3) !important;
        }
        
        /* Secondary Button */
        .stButton > button[kind="secondary"] {
            background: var(--machinify-dark-navy) !important;
            color: var(--machinify-white) !important;
            border: 2px solid var(--machinify-bright-green) !important;
        }
        
        /* Streamlit Metrics */
        [data-testid="metric-container"] {
            background: var(--machinify-white);
            border: 2px solid var(--machinify-medium-gray);
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            border-color: var(--machinify-bright-green);
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.1);
        }
        
        /* File Uploader */
        .stFileUploader > div {
            background-color: var(--machinify-light-gray);
            border: 2px dashed var(--machinify-bright-green);
            border-radius: 10px;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--machinify-bright-green), #6bb91a) !important;
        }
        
        /* Recommendations */
        .recommendation-high {
            background-color: #fee2e2;
            border-left: 4px solid var(--error-red);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
        }
        
        .recommendation-medium {
            background-color: #fef3c7;
            border-left: 4px solid var(--warning-orange);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
        }
        
        .recommendation-urgent {
            background: linear-gradient(135deg, var(--error-red) 0%, #b91c1c 100%);
            color: white;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
            border: 2px solid #7f1d1d;
        }
        
        /* Fraud Indicators */
        .fraud-indicators {
            background: rgba(220, 38, 38, 0.1);
            border: 2px solid rgba(220, 38, 38, 0.3);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .fraud-indicators h5 {
            color: var(--error-red);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        /* Footer */
        .footer {
            background: var(--machinify-dark-navy);
            color: var(--machinify-white);
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-radius: 15px 15px 0 0;
        }
        
        .footer strong {
            color: var(--machinify-bright-green);
        }
        
        /* Processing Progress - SIMPLIFIED */
        .processing-progress-simple {
            background: var(--machinify-light-gray);
            border: 2px solid var(--machinify-bright-green);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
                padding: 1.5rem 0;
            }
            
            .machinify-badge {
                display: block;
                margin: 0.5rem auto 0;
                width: fit-content;
            }
            
            .business-impact-card, .operational-metrics-card {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header with Machinify branding"""
    render_demo_mode_banner()
    st.markdown("""
    <h1 class="main-header">
        🏥 ClaimGuard
        <span class="machinify-badge">MACHINIFY INSPIRED</span>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #667085; margin-bottom: 2rem;">Pre-payment healthcare claims validation powered by advanced AI</p>', unsafe_allow_html=True)

def render_demo_mode_banner():
    """Render demo mode banner"""
    st.markdown("""
    <div class="demo-banner">
        <strong>🎯 DEMO MODE</strong> - Healthcare Claims Validation System
    </div>
    """, unsafe_allow_html=True)

def render_simple_processing_status(message: str):
    """Render simplified processing status without performance clutter"""
    st.markdown(f"""
    <div class="processing-progress-simple">
        <h4>{message}</h4>
        <p>Processing your claims with AI-powered validation...</p>
    </div>
    """, unsafe_allow_html=True)

def process_claims_validation_streamlined(enable_ai: bool, max_ai_claims: int):
    """Process claims validation with simplified progress tracking"""
    
    with st.spinner("🔄 Validating claims with AI analysis..."):
        try:
            # Show simple processing message
            render_simple_processing_status("🤖 Analyzing claims for validation errors...")
            
            # Initialize validator
            validator = ClaimValidator()
            
            # Run validation
            uploaded_data = SessionManager.get_uploaded_data()
            validation_results = validator.validate_batch(uploaded_data)
            SessionManager.set_validation_results(validation_results)
            
            # Generate AI explanations if enabled
            if enable_ai and validation_results['validation_results']:
                render_simple_processing_status("🧠 Generating AI explanations...")
                ai_explanations = generate_ai_explanations_streamlined(validation_results, uploaded_data, max_ai_claims)
                SessionManager.set_ai_explanations(ai_explanations)
            
            SessionManager.mark_processing_complete()
            
            # Show simple success message
            st.success(f"✅ Claims validation completed! Analyzed {len(uploaded_data)} claims.")
            
        except Exception as e:
            st.error(f"❌ Validation failed: {str(e)}")

def generate_ai_explanations_streamlined(validation_results: dict, uploaded_data, max_ai_claims: int):
    """Generate AI explanations with simplified progress tracking"""
    
    ai_explanations = {}
    processed_count = 0
    
    try:
        explainer = ClaimExplainer()
        claims_dict = uploaded_data.set_index('claim_id').to_dict('index')
        
        # Simple progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for result in validation_results['validation_results']:
            if processed_count >= max_ai_claims:
                break
            
            claim_data = claims_dict.get(int(result.claim_id), {})
            error_dict = {
                'error_type': result.error_type,
                'description': result.description,
                'severity': result.severity
            }
            
            try:
                ai_explanation = explainer.generate_explanation(error_dict, claim_data)
                ai_explanations[result.claim_id] = ai_explanation
                processed_count += 1
                
                # Update simple progress
                progress = processed_count / min(max_ai_claims, len(validation_results['validation_results']))
                progress_bar.progress(progress)
                status_text.text(f"Generated AI analysis for {processed_count} of {min(max_ai_claims, len(validation_results['validation_results']))} claims")
                
            except Exception as e:
                st.warning(f"AI analysis failed for claim {result.claim_id}: {str(e)}")
                continue
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return ai_explanations
        
    except Exception as e:
        st.warning(f"⚠️ AI explanations unavailable: {str(e)}")
        st.info("💡 Validation results still available with rule-based analysis")
        return {}

def render_main_content_streamlined(enable_ai: bool, severity_filter: list, max_ai_claims: int):
    """Render main content area with streamlined interface"""
    
    if not SessionManager.has_data():
        # Show welcome screen
        ValidationUI.render_welcome_screen()
        return
    
    # Show processing controls
    validate_button = SidebarControls.render_processing_controls()
    
    # Handle validation processing
    if validate_button:
        process_claims_validation_streamlined(enable_ai, max_ai_claims)
    
    # Display results if available
    if SessionManager.has_results():
        validation_results = SessionManager.get_validation_results()
        ai_explanations = SessionManager.get_ai_explanations()
        uploaded_data = SessionManager.get_uploaded_data()
        
        # Show AI summary dashboard if AI explanations were generated
        if ai_explanations:
            AIUIComponents.render_ai_summary_dashboard(ai_explanations)
        
        # Render core business value results
        render_kpi_dashboard(validation_results)
        render_business_impact_summary(validation_results, uploaded_data)
        render_error_trend_chart(validation_results)
        ValidationUI.render_validation_results(
            validation_results, severity_filter, enable_ai, max_ai_claims, ai_explanations
        )
        ValidationUI.render_duplicate_errors(validation_results)
        render_claim_details_table(uploaded_data, validation_results)
        render_action_recommendations(validation_results)
        
        # Export options
        ValidationUI.render_export_options(validation_results)

def main():
    """Main application orchestration function - streamlined version"""
    # Initialize application
    load_custom_css()
    SessionManager.initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get user settings
    enable_ai, ai_depth, max_ai_claims, severity_filter = SidebarControls.render_sidebar()
    
    # Render main content with streamlined interface
    render_main_content_streamlined(enable_ai, severity_filter, max_ai_claims)
    
    # Render footer
    render_footer()

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>ClaimGuard</strong> - Pre-payment Healthcare Claims Validation</p>
        <p>Built with Machinify-inspired design principles</p>
        <p><em>Preventing healthcare payment errors before they occur</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()