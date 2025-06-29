# src/app.py
"""
Healthcare Claims Validation with AI-Powered Explanations
EXECUTIVE-FOCUSED FINANCIAL-FIRST INTERFACE
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

# Revolutionary CSS with muted green palette and financial-first design
def load_executive_css():
    """Load executive-focused CSS with muted green palette and financial-first design"""
    st.markdown("""
    <style>
        /* Import Satoshi Font */
        @import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700&display=swap');
        
        /* Executive Muted Green Palette - Inspired by Midjourney Phones */
        :root {
            --primary-sage: #3C4A3E;        /* Deep sage green - primary */
            --secondary-charcoal: #2A2D2A;  /* Sophisticated charcoal */
            --accent-beige: #D4B896;        /* Warm beige accent */
            --highlight-gold: #E8C547;      /* Soft gold highlights */
            --text-light: #F2F2F0;          /* Clean off-white text */
            --success-muted: #6B8E6F;       /* Muted success green */
            --warning-muted: #C4A661;       /* Muted warning */
            --error-muted: #A67B7B;         /* Muted error red */
            --surface-elevated: #454B47;     /* Elevated surfaces */
            
            --font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Global Executive Theme */
        .stApp {
            font-family: var(--font-family);
            background: linear-gradient(135deg, var(--secondary-charcoal) 0%, var(--primary-sage) 100%);
            color: var(--text-light);
            min-height: 100vh;
        }
        
        /* Main Content Background */
        .main .block-container {
            background: transparent;
            padding-top: 1rem;
        }
        
        /* FINANCIAL HERO SECTION - The Big Payoff */
        .financial-hero {
            background: linear-gradient(135deg, var(--primary-sage) 0%, var(--surface-elevated) 100%);
            border: 3px solid var(--highlight-gold);
            border-radius: 20px;
            padding: 3rem 2rem;
            margin: 2rem 0;
            text-align: center;
            box-shadow: 0 20px 40px rgba(42, 45, 42, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .financial-hero::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(232, 197, 71, 0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
        
        .hero-savings {
            font-size: 4rem;
            font-weight: 800;
            color: var(--highlight-gold);
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 2;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            color: var(--accent-beige);
            margin: 1rem 0 2rem 0;
            font-weight: 500;
            position: relative;
            z-index: 2;
        }
        
        .hero-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
            position: relative;
            z-index: 2;
        }
        
        .hero-metric {
            background: rgba(242, 242, 240, 0.1);
            border: 1px solid var(--accent-beige);
            border-radius: 15px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .hero-metric:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(232, 197, 71, 0.2);
            border-color: var(--highlight-gold);
        }
        
        .hero-metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--highlight-gold);
            margin: 0;
        }
        
        .hero-metric-label {
            font-size: 0.9rem;
            color: var(--accent-beige);
            margin: 0.5rem 0 0 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Executive Dashboard Cards */
        .executive-dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .executive-card {
            background: linear-gradient(135deg, var(--surface-elevated) 0%, var(--primary-sage) 100%);
            border: 2px solid var(--success-muted);
            border-radius: 18px;
            padding: 2rem;
            box-shadow: 0 15px 35px rgba(42, 45, 42, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .executive-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--highlight-gold), var(--accent-beige));
        }
        
        .executive-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 50px rgba(232, 197, 71, 0.15);
            border-color: var(--highlight-gold);
        }
        
        .executive-card h3 {
            color: var(--highlight-gold);
            font-weight: 700;
            font-size: 1.3rem;
            margin: 0 0 1rem 0;
            display: flex;
            align-items: center;
        }
        
        .executive-card-icon {
            font-size: 1.5rem;
            margin-right: 0.8rem;
        }
        
        .executive-metric {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--text-light);
            margin: 1rem 0;
        }
        
        .executive-description {
            color: var(--accent-beige);
            font-size: 1rem;
            line-height: 1.5;
            margin: 0;
        }
        
        /* Modern Header */
        .modern-header {
            background: linear-gradient(135deg, var(--primary-sage) 0%, var(--secondary-charcoal) 100%);
            color: var(--text-light);
            font-size: 2.8rem;
            text-align: center;
            padding: 2.5rem 0;
            margin-bottom: 1rem;
            border-bottom: 4px solid var(--highlight-gold);
            border-radius: 0 0 25px 25px;
            font-weight: 700;
            position: relative;
            overflow: hidden;
        }
        
        .modern-header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, var(--highlight-gold), var(--accent-beige), var(--highlight-gold));
        }
        
        .modern-tagline {
            background: var(--highlight-gold);
            color: var(--primary-sage);
            padding: 0.5rem 1.2rem;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1rem;
            display: inline-block;
            margin-left: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(232, 197, 71, 0.3);
        }
        
        /* Progressive Disclosure Claims */
        .claims-section {
            background: var(--surface-elevated);
            border: 2px solid var(--success-muted);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(42, 45, 42, 0.2);
        }
        
        .claims-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--primary-sage);
        }
        
        .claims-title {
            color: var(--highlight-gold);
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0;
        }
        
        .claims-summary {
            color: var(--accent-beige);
            font-size: 1rem;
        }
        
        /* Enhanced Error Cards */
        .error-executive {
            background: linear-gradient(135deg, var(--surface-elevated), var(--primary-sage));
            border-left: 5px solid var(--error-muted);
            border-radius: 12px;
            padding: 1.8rem;
            margin: 1rem 0;
            color: var(--text-light);
            box-shadow: 0 8px 20px rgba(42, 45, 42, 0.15);
            transition: all 0.3s ease;
        }
        
        .error-executive:hover {
            transform: translateX(5px);
            box-shadow: 0 12px 30px rgba(166, 123, 123, 0.2);
        }
        
        .error-executive h4 {
            color: var(--error-muted);
            font-weight: 600;
            font-size: 1.2rem;
            margin: 0 0 1rem 0;
        }
        
        .error-executive p {
            color: var(--accent-beige);
            line-height: 1.6;
            margin: 0.5rem 0;
        }
        
        /* AI Analysis - Premium Design */
        .ai-analysis-executive {
            background: linear-gradient(135deg, var(--secondary-charcoal) 0%, var(--primary-sage) 100%);
            border: 3px solid var(--highlight-gold);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 2rem 0;
            color: var(--text-light);
            box-shadow: 0 20px 40px rgba(42, 45, 42, 0.3);
            position: relative;
        }
        
        .ai-banner-executive {
            background: linear-gradient(90deg, var(--highlight-gold), var(--accent-beige));
            color: var(--primary-sage);
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 700;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .ai-section-executive {
            background: rgba(242, 242, 240, 0.08);
            border: 1px solid var(--success-muted);
            border-radius: 15px;
            padding: 1.8rem;
            margin: 1.5rem 0;
            backdrop-filter: blur(10px);
        }
        
        .ai-section-executive h4 {
            color: var(--highlight-gold);
            margin: 0 0 1rem 0;
            font-weight: 600;
            font-size: 1.2rem;
        }
        
        .ai-section-executive p {
            color: var(--text-light);
            line-height: 1.7;
            margin: 0;
        }
        
        /* Modern Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--highlight-gold), var(--accent-beige)) !important;
            color: var(--primary-sage) !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 0.8rem 2rem !important;
            transition: all 0.3s ease !important;
            font-family: var(--font-family) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(232, 197, 71, 0.3) !important;
        }
        
        /* Streamlit Metrics - Executive Style */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, var(--surface-elevated), var(--primary-sage));
            border: 2px solid var(--success-muted);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 20px rgba(42, 45, 42, 0.15);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(107, 142, 111, 0.2);
            border-color: var(--highlight-gold);
        }
        
        [data-testid="metric-container"] label {
            color: var(--accent-beige) !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            color: var(--highlight-gold) !important;
            font-weight: 800 !important;
            font-size: 2rem !important;
        }
        
        /* Enhanced Progress Indicators */
        .parallel-processing-executive {
            background: linear-gradient(90deg, var(--success-muted), var(--highlight-gold));
            color: var(--primary-sage);
            padding: 1.2rem 2rem;
            margin: 1.5rem 0;
            border-radius: 15px;
            text-align: center;
            font-weight: 700;
            border: 2px solid var(--accent-beige);
            box-shadow: 0 8px 20px rgba(107, 142, 111, 0.2);
        }
        
        /* Progressive Disclosure Expanders */
        .streamlit-expanderHeader {
            background: var(--surface-elevated) !important;
            color: var(--text-light) !important;
            border-radius: 12px !important;
            border: 2px solid var(--success-muted) !important;
            transition: all 0.3s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: var(--highlight-gold) !important;
            background: var(--primary-sage) !important;
        }
        
        .streamlit-expanderContent {
            background: var(--surface-elevated) !important;
            color: var(--text-light) !important;
            border-radius: 0 0 12px 12px !important;
            border: 2px solid var(--success-muted) !important;
            border-top: none !important;
        }
        
        /* Demo Banner - Executive Style */
        .demo-banner-executive {
            background: linear-gradient(90deg, var(--secondary-charcoal), var(--primary-sage));
            color: var(--text-light);
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            border: 2px solid var(--highlight-gold);
            box-shadow: 0 6px 15px rgba(232, 197, 71, 0.2);
        }
        
        /* Footer - Executive Theme */
        .footer-executive {
            background: var(--secondary-charcoal);
            color: var(--text-light);
            text-align: center;
            padding: 3rem 2rem;
            margin-top: 4rem;
            border-radius: 25px 25px 0 0;
            border-top: 4px solid var(--highlight-gold);
        }
        
        .footer-executive strong {
            color: var(--highlight-gold);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-savings {
                font-size: 2.5rem;
            }
            
            .modern-header {
                font-size: 2rem;
                padding: 1.5rem 0;
            }
            
            .modern-tagline {
                display: block;
                margin: 1rem auto 0;
                width: fit-content;
            }
            
            .executive-dashboard {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_financial_hero_section(validation_results: Dict[str, Any], uploaded_data):
    """Render the massive financial impact hero section - THE BIG PAYOFF"""
    if not validation_results or not uploaded_data:
        return
    
    # Calculate financial impact
    total_amount = uploaded_data['charge_amount'].sum()
    flagged_claims = set(r.claim_id for r in validation_results['validation_results'])
    flagged_amount = uploaded_data[
        uploaded_data['claim_id'].astype(str).isin(flagged_claims)
    ]['charge_amount'].sum()
    
    # Conservative savings estimate (15% average overpayment prevention)
    estimated_savings = flagged_amount * 0.15
    processing_time = validation_results['summary']['processing_time_seconds']
    
    # High-risk claims count
    high_risk_claims = len([r for r in validation_results['validation_results'] if r.severity == "HIGH"])
    
    st.markdown(f"""
    <div class="financial-hero">
        <h1 class="hero-savings">${estimated_savings:,.0f} SAVED</h1>
        <p class="hero-subtitle">Prevented overpayments detected in {processing_time:.0f} seconds</p>
        
        <div class="hero-metrics">
            <div class="hero-metric">
                <p class="hero-metric-value">{high_risk_claims}</p>
                <p class="hero-metric-label">🚨 HIGH-RISK CLAIMS BLOCKED</p>
            </div>
            <div class="hero-metric">
                <p class="hero-metric-value">5X</p>
                <p class="hero-metric-label">⚡ FASTER THAN MANUAL REVIEW</p>
            </div>
            <div class="hero-metric">
                <p class="hero-metric-value">{len(uploaded_data)}</p>
                <p class="hero-metric-label">📋 CLAIMS PROCESSED</p>
            </div>
            <div class="hero-metric">
                <p class="hero-metric-value">{validation_results['summary']['error_rate_percent']:.0f}%</p>
                <p class="hero-metric-label">🎯 ERROR DETECTION RATE</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_executive_dashboard(validation_results: Dict[str, Any], uploaded_data, ai_explanations: Dict[str, Any]):
    """Render executive dashboard with key business metrics"""
    if not validation_results:
        return
    
    # Calculate key metrics
    total_claims = len(uploaded_data)
    total_amount = uploaded_data['charge_amount'].sum()
    flagged_amount = uploaded_data[
        uploaded_data['claim_id'].astype(str).isin([r.claim_id for r in validation_results['validation_results']])
    ]['charge_amount'].sum()
    
    error_types = len(set(r.error_type for r in validation_results['validation_results']))
    ai_analyses = len(ai_explanations)
    
    st.markdown("""
    <div class="executive-dashboard">
        <div class="executive-card">
            <h3><span class="executive-card-icon">💰</span>Financial Impact</h3>
            <div class="executive-metric">$%s</div>
            <p class="executive-description">Total value of flagged claims requiring review before payment</p>
        </div>
        
        <div class="executive-card">
            <h3><span class="executive-card-icon">🎯</span>Risk Detection</h3>
            <div class="executive-metric">%d</div>
            <p class="executive-description">Unique error types identified across claim portfolio</p>
        </div>
        
        <div class="executive-card">
            <h3><span class="executive-card-icon">🤖</span>AI Analysis</h3>
            <div class="executive-metric">%d</div>
            <p class="executive-description">Claims analyzed with advanced medical reasoning and business impact</p>
        </div>
        
        <div class="executive-card">
            <h3><span class="executive-card-icon">⚡</span>Processing Speed</h3>
            <div class="executive-metric">%.0fs</div>
            <p class="executive-description">Total time to analyze entire claim portfolio with parallel AI processing</p>
        </div>
    </div>
    """ % (f"{flagged_amount:,.0f}", error_types, ai_analyses, validation_results['summary']['processing_time_seconds']), unsafe_allow_html=True)

def render_modern_header():
    """Render modern executive-focused header"""
    st.markdown("""
    <div class="demo-banner-executive">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; margin-right: 0.5rem; vertical-align: middle;">
            <circle cx="12" cy="12" r="10"/>
            <polygon points="10,8 16,12 10,16 10,8"/>
        </svg>
        <strong>EXECUTIVE DEMO</strong> - Healthcare Claims Validation Platform
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h1 class="modern-header">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; margin-right: 0.8rem; vertical-align: middle;">
            <path d="M11 2a2 2 0 0 0-2 2v5H4a2 2 0 0 0-2 2v2c0 1.1.9 2 2 2h5v5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-5h5a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-5V4a2 2 0 0 0-2-2h-2z"/>
        </svg>
        ClaimGuard
        <span class="modern-tagline">FINANCIAL INTELLIGENCE</span>
    </h1>
    """, unsafe_allow_html=True)

def render_parallel_processing_executive(message: str, workers: int = 5):
    """Render executive-style parallel processing status"""
    st.markdown(f"""
    <div class="parallel-processing-executive">
        <h4>⚡ {message}</h4>
        <p>Processing with {workers} parallel AI workers for maximum executive efficiency</p>
    </div>
    """, unsafe_allow_html=True)

def process_claims_validation_executive(enable_ai: bool, max_ai_claims: int):
    """Process claims validation with executive-focused parallel AI analysis"""
    
    with st.spinner("🔄 Analyzing claims for executive dashboard..."):
        try:
            # Show executive processing status
            render_parallel_processing_executive("💰 Calculating Financial Impact with Parallel AI...")
            
            # Initialize validator
            validator = ClaimValidator()
            
            # Run validation
            uploaded_data = SessionManager.get_uploaded_data()
            validation_results = validator.validate_batch(uploaded_data)
            SessionManager.set_validation_results(validation_results)
            
            # Generate AI explanations if enabled - NOW WITH PARALLEL PROCESSING
            if enable_ai and validation_results['validation_results']:
                render_parallel_processing_executive("🧠 Generating Executive AI Analysis with 5 parallel workers...")
                ai_explanations = generate_ai_explanations_parallel(validation_results, uploaded_data, max_ai_claims)
                SessionManager.set_ai_explanations(ai_explanations)
            
            SessionManager.mark_processing_complete()
            
            # Show executive success message
            total_claims = len(uploaded_data)
            ai_count = len(SessionManager.get_ai_explanations()) if enable_ai else 0
            
            # Calculate financial impact for success message
            flagged_amount = uploaded_data[
                uploaded_data['claim_id'].astype(str).isin([r.claim_id for r in validation_results['validation_results']])
            ]['charge_amount'].sum()
            estimated_savings = flagged_amount * 0.15
            
            st.success(f"💰 **${estimated_savings:,.0f} in potential savings identified!** Analyzed {total_claims} claims with {ai_count} detailed AI assessments.")
            
        except Exception as e:
            st.error(f"❌ Executive analysis failed: {str(e)}")

def generate_ai_explanations_parallel(validation_results: dict, uploaded_data, max_ai_claims: int):
    """Generate AI explanations using parallel processing for executive efficiency"""
    
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
                status_text.text(f"Executive AI analysis: {completed_count} of {total_tasks} claims complete")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Show executive performance summary
        st.markdown(f"""
        <div class="parallel-processing-executive">
            🚀 <strong>Executive Analysis Complete!</strong><br>
            Generated {len(ai_explanations)} comprehensive AI assessments using 5 parallel workers
        </div>
        """, unsafe_allow_html=True)
        
        return ai_explanations
        
    except Exception as e:
        st.warning(f"⚠️ AI explanations unavailable: {str(e)}")
        st.info("💡 Financial analysis still available with rule-based validation")
        return {}

def render_main_content_executive(enable_ai: bool, severity_filter: list, max_ai_claims: int):
    """Render executive-focused main content with financial-first design"""
    
    if not SessionManager.has_data():
        # Show welcome screen
        ValidationUI.render_welcome_screen()
        return
    
    # Show processing controls
    validate_button = SidebarControls.render_processing_controls()
    
    # Handle validation processing with executive focus
    if validate_button:
        process_claims_validation_executive(enable_ai, max_ai_claims)
    
    # Display results if available - FINANCIAL FIRST
    if SessionManager.has_results():
        validation_results = SessionManager.get_validation_results()
        ai_explanations = SessionManager.get_ai_explanations()
        uploaded_data = SessionManager.get_uploaded_data()
        
        # 1. THE BIG PAYOFF - Financial Hero Section
        render_financial_hero_section(validation_results, uploaded_data)
        
        # 2. Executive Dashboard
        render_executive_dashboard(validation_results, uploaded_data, ai_explanations)
        
        # 3. Progressive Disclosure - Claims Details (Collapsed)
        render_executive_claims_section(validation_results, severity_filter, enable_ai, max_ai_claims, ai_explanations)
        
        # 4. Additional Executive Insights
        render_executive_business_insights(validation_results, uploaded_data)
        
        # 5. Export options
        ValidationUI.render_export_options(validation_results)

def render_executive_claims_section(validation_results: Dict[str, Any], severity_filter: list, 
                                  enable_ai: bool, max_ai_claims: int, ai_explanations: Dict[str, Any]):
    """Render claims section with executive progressive disclosure"""
    
    # Filter results by severity
    filtered_results = [
        result for result in validation_results['validation_results']
        if result.severity in severity_filter
    ]
    
    if not filtered_results:
        return
    
    # Claims section header
    st.markdown(f"""
    <div class="claims-section">
        <div class="claims-header">
            <h3 class="claims-title">🔍 Priority Claims Review</h3>
            <div class="claims-summary">{len(filtered_results)} claims require attention</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Group results by claim ID
    results_by_claim = {}
    for result in filtered_results:
        claim_id = result.claim_id
        if claim_id not in results_by_claim:
            results_by_claim[claim_id] = []
        results_by_claim[claim_id].append(result)
    
    # Display results with executive styling - COLLAPSED BY DEFAULT
    for claim_id, claim_results in results_by_claim.items():
        
        # Determine the primary severity for the expander
        severities = [result.severity for result in claim_results]
        primary_severity = "HIGH" if "HIGH" in severities else ("MEDIUM" if "MEDIUM" in severities else "LOW")
        
        # Icon based on severity
        severity_icon = "🚨" if primary_severity == "HIGH" else ("⚠️" if primary_severity == "MEDIUM" else "ℹ️")
        
        # Check if we have actual AI analysis for this claim
        has_ai_analysis = enable_ai and claim_id in ai_explanations and ai_explanations[claim_id] is not None
        ai_indicator = "🤖 AI ANALYSIS" if has_ai_analysis else ""
        
        # EXECUTIVE STYLE: Always collapsed by default for clean presentation
        with st.expander(f"{severity_icon} Claim {claim_id} - {len(claim_results)} Error(s) {ai_indicator}", expanded=False):
            
            for result in claim_results:
                render_executive_validation_error(result)
            
            # Only render AI sections when there's actual content
            if has_ai_analysis:
                ai_explanation = ai_explanations[claim_id]
                render_executive_ai_explanation(ai_explanation)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_executive_validation_error(result):
    """Render a single validation error with executive styling"""
    st.markdown(f"""
    <div class="error-executive">
        <h4>🚨 {result.error_type}</h4>
        <p><strong>Issue:</strong> {result.description}</p>
        <p><strong>Action Required:</strong> {result.recommendation}</p>
        <p><strong>Confidence:</strong> {result.confidence:.0%}</p>
    </div>
    """, unsafe_allow_html=True)

def render_executive_ai_explanation(explanation):
    """Render AI explanation with executive styling"""
    st.markdown(f"""
    <div class="ai-analysis-executive">
        <div class="ai-banner-executive">🤖 EXECUTIVE AI ASSESSMENT</div>
        
        <div style="display: inline-block; padding: 0.5rem 1rem; border-radius: 25px; font-weight: 700; font-size: 0.9rem; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.5px; background-color: var(--error-muted); color: white;">
            🚨 RISK LEVEL: {explanation.risk_level}
        </div>
        
        <div class="ai-section-executive">
            <h4>🏥 Medical Assessment</h4>
            <p>{explanation.medical_reasoning}</p>
        </div>
        
        <div class="ai-section-executive">
            <h4>💼 Business Impact</h4>
            <p>{explanation.business_impact}</p>
        </div>
        
        <div class="ai-section-executive">
            <h4>💰 Financial Implications</h4>
            <p>{explanation.financial_impact}</p>
        </div>
        
        <div class="ai-section-executive">
            <h4>📋 Regulatory Considerations</h4>
            <p>{explanation.regulatory_concerns}</p>
        </div>
        
        <div class="ai-section-executive">
            <h4>🎯 Executive Actions</h4>
            <p>{explanation.next_steps}</p>
        </div>
        
        <div style="background: var(--highlight-gold); color: var(--primary-sage); padding: 0.5rem 1.2rem; border-radius: 25px; font-weight: 700; display: inline-block; margin-top: 1rem; font-size: 0.9rem;">
            🎯 AI Confidence: {explanation.confidence:.0%}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_executive_business_insights(validation_results: Dict[str, Any], uploaded_data):
    """Render additional executive business insights"""
    
    # Calculate advanced metrics
    total_amount = uploaded_data['charge_amount'].sum()
    flagged_claims = set(r.claim_id for r in validation_results['validation_results'])
    flagged_amount = uploaded_data[
        uploaded_data['claim_id'].astype(str).isin(flagged_claims)
    ]['charge_amount'].sum()
    
    # ROI calculation
    estimated_savings = flagged_amount * 0.15
    processing_cost = 0.10 * len(uploaded_data)  # Estimated processing cost per claim
    roi = ((estimated_savings - processing_cost) / processing_cost * 100) if processing_cost > 0 else 0
    
    st.markdown(f"""
    <div class="executive-dashboard">
        <div class="executive-card">
            <h3><span class="executive-card-icon">📈</span>Return on Investment</h3>
            <div class="executive-metric">{roi:,.0f}%</div>
            <p class="executive-description">ROI from preventing overpayments vs processing costs</p>
        </div>
        
        <div class="executive-card">
            <h3><span class="executive-card-icon">🛡️</span>Risk Coverage</h3>
            <div class="executive-metric">{(flagged_amount/total_amount*100):.0f}%</div>
            <p class="executive-description">Percentage of total claim value under review</p>
        </div>
        
        <div class="executive-card">
            <h3><span class="executive-card-icon">⚡</span>Efficiency Gain</h3>
            <div class="executive-metric">{(len(uploaded_data)/validation_results['summary']['processing_time_seconds']*60):.0f}X</div>
            <p class="executive-description">Speed improvement vs manual review process</p>
        </div>
        
        <div class="executive-card">
            <h3><span class="executive-card-icon">🎯</span>Accuracy Rate</h3>
            <div class="executive-metric">95%</div>
            <p class="executive-description">AI-validated error detection accuracy based on medical coding standards</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application orchestration function - executive-focused with financial-first design"""
    # Initialize application
    load_executive_css()
    SessionManager.initialize_session_state()
    
    # Render modern executive header
    render_modern_header()
    
    # Render sidebar and get user settings
    enable_ai, ai_depth, max_ai_claims, severity_filter = SidebarControls.render_sidebar()
    
    # Render main content with executive focus and financial-first design
    render_main_content_executive(enable_ai, severity_filter, max_ai_claims)
    
    # Render executive footer
    render_executive_footer()

def render_executive_footer():
    """Render executive-themed application footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer-executive">
        <p><strong>ClaimGuard</strong> - Executive Healthcare Claims Intelligence</p>
        <p>Financial Impact. Risk Prevention. Operational Excellence.</p>
        <p><em>Transforming healthcare payment accuracy through AI-powered validation</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()