# src/app.py
"""
Healthcare Claims Validation with AI-Powered Explanations
"""

import streamlit as st
import sys
import os
import time
import asyncio
import concurrent.futures
from typing import Dict, Any

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

# Load updated CSS with dark theme and Lucide icons
def load_custom_css():
    """Load updated CSS with Machinify-inspired dark theme and modern icons"""
    st.markdown("""
    <style>
        /* Import Satoshi Font */
        @import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700&display=swap');
        
        /* Machinify Dark Theme Colors */
        :root {
            --primary-dark: #283B45;
            --secondary-dark: #0C1F28;
            --accent-dark: #081D27;
            --light-accent: #E2EAEF;
            --action-green: #7ed321;
            --success-green: #10b981;
            
            /* Sophisticated Red Palette */
            --primary-accent: #D24D57;      /* Muted Crimson - main error states */
            --soft-warning: #C0392B;        /* Desaturated Brick - warnings */
            --text-accent: #B23B3B;         /* Dark Clay Red - text highlights */
            --button-hover: #E74C3C;        /* Warm Alert Red - interactive states */
            --outline-subtle: #AD3E3E;      /* Auburn Edge - borders/outlines */
            
            --warning-orange: #f59e0b;
            --info-blue: #2563eb;
            
            --font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Global Dark Theme */
        .stApp {
            font-family: var(--font-family);
            background-color: var(--light-accent);
            color: var(--primary-dark);
        }
        
        /* Main Content Background */
        .main .block-container {
            background-color: var(--light-accent);
            padding-top: 1rem;
        }
        
        /* Main Header - Dark with Light Text */
        .main-header {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
            color: var(--light-accent);
            font-size: 2.5rem;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-bottom: 4px solid var(--action-green);
            border-radius: 0 0 15px 15px;
            font-weight: 700;
        }
        
        .tagline {
            background: var(--action-green);
            color: var(--primary-dark);
            padding: 0.4rem 1rem;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9rem;
            display: inline-block;
            margin-left: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Demo Banner - Dark Theme */
        .demo-banner {
            background: linear-gradient(90deg, var(--secondary-dark), var(--primary-dark));
            color: var(--light-accent);
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            border: 2px solid var(--action-green);
        }
        
        /* Card Backgrounds - Dark */
        .success-card {
            background: linear-gradient(135deg, var(--action-green) 0%, var(--success-green) 100%);
            color: var(--primary-dark);
            border-left: 4px solid #5a9f18;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
            font-weight: 500;
        }
        
        /* Error Cards with Sophisticated Red Palette */
        .error-high {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
            color: var(--light-accent);
            border-left: 4px solid var(--primary-accent);
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        .error-medium {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
            color: var(--light-accent);
            border-left: 4px solid var(--soft-warning);
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        .error-low {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
            color: var(--light-accent);
            border-left: 4px solid var(--info-blue);
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        /* AI Analysis Container - Enhanced Dark */
        .ai-analysis-container {
            background: linear-gradient(135deg, var(--accent-dark) 0%, var(--secondary-dark) 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            color: var(--light-accent);
            box-shadow: 0 8px 25px rgba(8, 29, 39, 0.4);
            border: 2px solid var(--action-green);
        }
        
        .ai-section {
            background: rgba(226, 234, 239, 0.1);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(126, 211, 33, 0.3);
        }
        
        .ai-section h4 {
            color: var(--action-green);
            margin-bottom: 0.5rem;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .ai-section p {
            color: var(--light-accent);
            line-height: 1.6;
            margin-bottom: 0;
        }
        
        /* Business Impact Cards - Dark Theme */
        .business-impact-card {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
            color: var(--light-accent);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(40, 59, 69, 0.3);
            border: 2px solid var(--action-green);
        }
        
        .operational-metrics-card {
            background: linear-gradient(135deg, var(--accent-dark) 0%, var(--secondary-dark) 100%);
            color: var(--light-accent);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(8, 29, 39, 0.3);
            border: 2px solid var(--action-green);
        }
        
        .business-impact-card h3, .operational-metrics-card h3 {
            margin-top: 0;
            font-weight: 700;
            font-size: 1.3rem;
            color: var(--action-green);
        }
        
        /* Risk Indicators with Sophisticated Reds */
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
            background-color: var(--primary-accent);
            color: white;
        }
        
        .risk-medium {
            background-color: var(--soft-warning);
            color: white;
        }
        
        .risk-low {
            background-color: var(--action-green);
            color: var(--primary-dark);
        }
        
        /* Confidence Badge */
        .confidence-badge {
            background: var(--action-green);
            color: var(--primary-dark);
            padding: 0.4rem 1.2rem;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        
        /* AI Powered Banner */
        .ai-powered-banner {
            background: linear-gradient(90deg, var(--action-green), var(--primary-dark));
            color: var(--light-accent);
            padding: 0.8rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        /* Sidebar Styling - Dark Theme */
        .sidebar-info {
            background: var(--primary-dark);
            border: 2px solid var(--action-green);
            color: var(--light-accent);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .sidebar-info h3 {
            color: var(--action-green);
            margin-top: 0;
            font-weight: 700;
        }
        
        /* Button Styling */
        .stButton > button {
            background: var(--action-green) !important;
            color: var(--primary-dark) !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s ease !important;
            font-family: var(--font-family) !important;
        }
        
        .stButton > button:hover {
            background: var(--success-green) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.3) !important;
        }
        
        /* Secondary Button */
        .stButton > button[kind="secondary"] {
            background: var(--primary-dark) !important;
            color: var(--light-accent) !important;
            border: 2px solid var(--action-green) !important;
        }
        
        /* Streamlit Metrics - Dark Theme */
        [data-testid="metric-container"] {
            background: var(--primary-dark);
            border: 2px solid var(--action-green);
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(8, 29, 39, 0.2);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            border-color: var(--action-green);
            box-shadow: 0 4px 12px rgba(126, 211, 33, 0.2);
            transform: translateY(-1px);
        }
        
        [data-testid="metric-container"] label {
            color: var(--light-accent) !important;
            font-weight: 600 !important;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            color: var(--action-green) !important;
            font-weight: 700 !important;
        }
        
        /* File Uploader - Dark Theme */
        .stFileUploader > div {
            background-color: var(--primary-dark);
            border: 2px dashed var(--action-green);
            color: var(--light-accent);
            border-radius: 10px;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--action-green), var(--success-green)) !important;
        }
        
        /* Recommendations - Sophisticated Red Palette */
        .recommendation-high {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
            color: var(--light-accent);
            border-left: 4px solid var(--soft-warning);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
        }
        
        .recommendation-medium {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
            color: var(--light-accent);
            border-left: 4px solid var(--warning-orange);
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
        }
        
        .recommendation-urgent {
            background: linear-gradient(135deg, var(--primary-accent) 0%, var(--soft-warning) 100%);
            color: white;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
            border: 2px solid var(--outline-subtle);
        }
        
        /* Fraud Indicators - Sophisticated Red */
        .fraud-indicators {
            background: linear-gradient(135deg, var(--primary-dark), var(--secondary-dark));
            border: 2px solid var(--outline-subtle);
            color: var(--light-accent);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .fraud-indicators h5 {
            color: var(--text-accent);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        /* Footer - Dark Theme */
        .footer {
            background: var(--accent-dark);
            color: var(--light-accent);
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-radius: 15px 15px 0 0;
            border-top: 4px solid var(--action-green);
        }
        
        .footer strong {
            color: var(--action-green);
        }
        
        /* Processing Progress - Dark Theme */
        .processing-progress-simple {
            background: var(--primary-dark);
            border: 2px solid var(--action-green);
            color: var(--light-accent);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            text-align: center;
        }
        
        /* Welcome Screen Icons with Lucide Style */
        .welcome-step {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
            padding: 0.5rem;
            border-radius: 6px;
            transition: background-color 0.2s ease;
        }
        
        .welcome-step:hover {
            background-color: rgba(126, 211, 33, 0.1);
        }
        
        .step-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            margin-right: 0.5rem;
            color: var(--action-green);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
                padding: 1.5rem 0;
            }
            
            .tagline {
                display: block;
                margin: 0.5rem auto 0;
                width: fit-content;
            }
            
            .business-impact-card, .operational-metrics-card {
                padding: 1rem;
            }
        }
        
        /* Dataframe Styling */
        .stDataFrame {
            background-color: var(--primary-dark);
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: var(--primary-dark) !important;
            color: var(--light-accent) !important;
            border-radius: 8px !important;
        }
        
        .streamlit-expanderContent {
            background-color: var(--primary-dark) !important;
            color: var(--light-accent) !important;
            border-radius: 0 0 8px 8px !important;
        }

        /* Performance Status Styling */
        .parallel-processing-status {
            background: linear-gradient(90deg, var(--action-green), var(--success-green));
            color: var(--primary-dark);
            padding: 0.8rem 1.5rem;
            margin: 1rem 0;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            border: 2px solid var(--primary-dark);
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header with Lucide icons and updated branding"""
    render_demo_mode_banner()
    st.markdown("""
    <h1 class="main-header">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; margin-right: 0.5rem; vertical-align: middle;">
            <path d="M11 2a2 2 0 0 0-2 2v5H4a2 2 0 0 0-2 2v2c0 1.1.9 2 2 2h5v5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-5h5a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-5V4a2 2 0 0 0-2-2h-2z"/>
        </svg>
        ClaimGuard
        <span class="tagline">DETECT. EXPLAIN. IMPROVE.</span>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #667085; margin-bottom: 2rem;">Pre-payment healthcare claims validation powered by advanced AI</p>', unsafe_allow_html=True)

def render_demo_mode_banner():
    """Render demo mode banner with Lucide icon"""
    st.markdown("""
    <div class="demo-banner">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; margin-right: 0.5rem; vertical-align: middle;">
            <circle cx="12" cy="12" r="10"/>
            <polygon points="10,8 16,12 10,16 10,8"/>
        </svg>
        <strong>DEMO MODE</strong> - Healthcare Claims Validation System
    </div>
    """, unsafe_allow_html=True)

def render_parallel_processing_status(message: str, workers: int = 5):
    """Render parallel processing status indicator"""
    st.markdown(f"""
    <div class="parallel-processing-status">
        <h4>⚡ {message}</h4>
        <p>Processing with {workers} parallel AI workers for maximum speed...</p>
    </div>
    """, unsafe_allow_html=True)

def process_claims_validation_parallel(enable_ai: bool, max_ai_claims: int):
    """Process claims validation with parallel AI analysis for maximum speed"""
    
    with st.spinner("🔄 Validating claims with parallel AI analysis..."):
        try:
            # Show parallel processing status
            render_parallel_processing_status("🤖 Analyzing claims with parallel AI processing...")
            
            # Initialize validator
            validator = ClaimValidator()
            
            # Run validation
            uploaded_data = SessionManager.get_uploaded_data()
            validation_results = validator.validate_batch(uploaded_data)
            SessionManager.set_validation_results(validation_results)
            
            # Generate AI explanations if enabled - NOW WITH PARALLEL PROCESSING
            if enable_ai and validation_results['validation_results']:
                render_parallel_processing_status("🧠 Generating AI explanations with 5 parallel workers...")
                ai_explanations = generate_ai_explanations_parallel(validation_results, uploaded_data, max_ai_claims)
                SessionManager.set_ai_explanations(ai_explanations)
            
            SessionManager.mark_processing_complete()
            
            # Show success message with performance info
            total_claims = len(uploaded_data)
            ai_count = len(SessionManager.get_ai_explanations()) if enable_ai else 0
            st.success(f"✅ Claims validation completed! Analyzed {total_claims} claims with {ai_count} AI explanations.")
            
        except Exception as e:
            st.error(f"❌ Validation failed: {str(e)}")

def generate_ai_explanations_parallel(validation_results: dict, uploaded_data, max_ai_claims: int):
    """Generate AI explanations using parallel processing for maximum speed"""
    
    ai_explanations = {}
    
    try:
        explainer = ClaimExplainer()
        claims_dict = uploaded_data.set_index('claim_id').to_dict('index')
        
        # Prepare tasks for parallel processing
        validation_tasks = []
        for i, result in enumerate(validation_results['validation_results']):
            if i >= max_ai_claims:
                break
                
            claim_data = claims_dict.get(int(result.claim_id), {})
            error_dict = {
                'error_type': result.error_type,
                'description': result.description,
                'severity': result.severity
            }
            
            validation_tasks.append({
                'claim_id': result.claim_id,
                'error_dict': error_dict,
                'claim_data': claim_data
            })
        
        if not validation_tasks:
            return {}
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def process_single_claim(task):
            """Process a single claim's AI analysis"""
            try:
                ai_explanation = explainer.generate_explanation(task['error_dict'], task['claim_data'])
                return task['claim_id'], ai_explanation
            except Exception as e:
                st.warning(f"AI analysis failed for claim {task['claim_id']}: {str(e)}")
                return task['claim_id'], None
        
        # Execute parallel processing with ThreadPoolExecutor
        completed_count = 0
        total_tasks = len(validation_tasks)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            future_to_claim = {
                executor.submit(process_single_claim, task): task['claim_id'] 
                for task in validation_tasks
            }
            
            # Process completed tasks as they finish
            for future in concurrent.futures.as_completed(future_to_claim):
                claim_id, ai_explanation = future.result()
                
                if ai_explanation:
                    ai_explanations[claim_id] = ai_explanation
                
                completed_count += 1
                
                # Update progress
                progress = completed_count / total_tasks
                progress_bar.progress(progress)
                status_text.text(f"Completed AI analysis for {completed_count} of {total_tasks} claims")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Show performance summary
        st.markdown(f"""
        <div class="parallel-processing-status">
            🚀 <strong>Parallel Processing Complete!</strong><br>
            Generated {len(ai_explanations)} AI explanations using 5 parallel workers
        </div>
        """, unsafe_allow_html=True)
        
        return ai_explanations
        
    except Exception as e:
        st.warning(f"⚠️ AI explanations unavailable: {str(e)}")
        st.info("💡 Validation results still available with rule-based analysis")
        return {}

def render_main_content_parallel(enable_ai: bool, severity_filter: list, max_ai_claims: int):
    """Render main content area with parallel processing interface"""
    
    if not SessionManager.has_data():
        # Show welcome screen
        ValidationUI.render_welcome_screen()
        return
    
    # Show processing controls
    validate_button = SidebarControls.render_processing_controls()
    
    # Handle validation processing with parallel AI
    if validate_button:
        process_claims_validation_parallel(enable_ai, max_ai_claims)
    
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
    """Main application orchestration function - now with parallel processing"""
    # Initialize application
    load_custom_css()
    SessionManager.initialize_session_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get user settings
    enable_ai, ai_depth, max_ai_claims, severity_filter = SidebarControls.render_sidebar()
    
    # Render main content with parallel processing
    render_main_content_parallel(enable_ai, severity_filter, max_ai_claims)
    
    # Render footer
    render_footer()

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>ClaimGuard</strong> - Pre-payment Healthcare Claims Validation</p>
        <p>Detect. Explain. Improve.</p>
        <p><em>Preventing healthcare payment errors before they occur</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()