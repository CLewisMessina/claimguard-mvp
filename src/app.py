# src/app.py
"""
ClaimGuard MVP - Performance Optimized Streamlit Application
Healthcare Claims Validation with Advanced AI-Powered Explanations + Performance Optimization
Enhanced with AI caching, batch processing, and real-time performance monitoring
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

# Import performance optimization components
from ai_cache import PerformanceManager
from performance_ui import PerformanceUI

# Page configuration
st.set_page_config(
    page_title="ClaimGuard - Healthcare Claims Validation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS styling (enhanced with performance indicators)
def load_custom_css():
    """Load custom CSS for professional healthcare styling with performance indicators"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1e3a8a;
            text-align: center;
            padding: 1rem 0;
            border-bottom: 3px solid #3b82f6;
            margin-bottom: 2rem;
        }
        
        .performance-badge {
            background: linear-gradient(45deg, #10b981, #059669);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.8rem;
            display: inline-block;
            margin-left: 1rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .performance-metric-card {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            border: 2px solid rgba(16, 185, 129, 0.3);
        }
        
        .error-high {
            background-color: #fee2e2;
            border-left: 4px solid #dc2626;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        
        .error-medium {
            background-color: #fef3c7;
            border-left: 4px solid #d97706;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        
        .error-low {
            background-color: #dbeafe;
            border-left: 4px solid #2563eb;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        
        .success-card {
            background-color: #d1fae5;
            border-left: 4px solid #10b981;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
        }
        
        .sidebar-info {
            background-color: #f8fafc;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin: 1rem 0;
        }
        
        .ai-analysis-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .ai-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }
        
        .ai-section h4 {
            color: #ffffff;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        .ai-section p {
            color: #f1f5f9;
            line-height: 1.6;
            margin-bottom: 0;
        }
        
        .risk-indicator {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .risk-high {
            background-color: #dc2626;
            color: white;
        }
        
        .risk-medium {
            background-color: #d97706;
            color: white;
        }
        
        .risk-low {
            background-color: #10b981;
            color: white;
        }
        
        .fraud-indicators {
            background: rgba(220, 38, 38, 0.1);
            border: 1px solid rgba(220, 38, 38, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .fraud-indicators h5 {
            color: #dc2626;
            margin-bottom: 0.5rem;
        }
        
        .fraud-indicators ul {
            margin: 0;
            padding-left: 1.5rem;
        }
        
        .fraud-indicators li {
            color: #7f1d1d;
            margin-bottom: 0.3rem;
        }
        
        .confidence-badge {
            background: linear-gradient(45deg, #10b981, #059669);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-top: 1rem;
        }
        
        .ai-powered-banner {
            background: linear-gradient(90deg, #8b5cf6, #3b82f6);
            color: white;
            padding: 0.5rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .processing-progress-enhanced {
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border: 2px solid #0ea5e9;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header with performance badge"""
    render_demo_mode_banner()
    st.markdown("""
    <h1 class="main-header">
        🏥 ClaimGuard
        <span class="performance-badge">⚡ PERFORMANCE OPTIMIZED</span>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #64748b;">Pre-payment healthcare claims validation powered by advanced AI with enterprise-grade performance optimization</p>', unsafe_allow_html=True)

def process_claims_validation_optimized(enable_ai: bool, max_ai_claims: int):
    """Process claims validation with advanced performance optimization"""
    
    # Initialize performance monitoring
    start_time = time.time()
    
    with st.spinner("🔄 Validating claims with performance-optimized AI analysis..."):
        try:
            # Initialize validator
            validator = ClaimValidator()
            
            # Run validation
            uploaded_data = SessionManager.get_uploaded_data()
            validation_results = validator.validate_batch(uploaded_data)
            SessionManager.set_validation_results(validation_results)
            
            # Generate enhanced AI explanations with performance optimization
            if enable_ai and validation_results['validation_results']:
                ai_explanations = generate_ai_explanations_optimized(validation_results, uploaded_data, max_ai_claims)
                SessionManager.set_ai_explanations(ai_explanations)
            
            # Update performance statistics
            processing_time = time.time() - start_time
            performance_stats = {
                'total_processing_time': processing_time,
                'validation_speed': len(uploaded_data) / processing_time,
                'optimization_active': True
            }
            PerformanceManager.update_performance_stats(performance_stats)
            
            SessionManager.mark_processing_complete()
            
            # Show success with performance metrics
            cache_stats = PerformanceManager.get_ai_cache().get_stats()
            st.success(f"✅ Claims validation completed in {processing_time:.2f}s! Cache hit rate: {cache_stats['hit_rate_percent']}%")
            
        except Exception as e:
            st.error(f"❌ Validation failed: {str(e)}")

def generate_ai_explanations_optimized(validation_results: dict, uploaded_data, max_ai_claims: int):
    """Generate AI explanations using optimized batch processing and caching"""
    
    # Get optimized batch processor
    batch_processor = PerformanceManager.get_batch_processor()
    
    # Show enhanced progress indicator
    progress_container = st.empty()
    
    try:
        explainer = ClaimExplainer()
        
        # Get claim data for context
        claims_dict = uploaded_data.set_index('claim_id').to_dict('index')
        
        # Process with optimization
        ai_explanations = batch_processor.process_batch_optimized(
            validation_results['validation_results'],
            claims_dict,
            explainer,
            max_ai_claims
        )
        
        # Get performance statistics
        batch_stats = batch_processor.get_performance_stats()
        cache_stats = PerformanceManager.get_ai_cache().get_stats()
        
        # Clear progress indicator and show results
        progress_container.empty()
        
        # Show performance summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🤖 AI Analyses", len(ai_explanations))
        with col2:
            st.metric("⚡ Cache Hits", batch_stats.get('cache_hits', 0))
        with col3:
            st.metric("💰 API Calls Saved", cache_stats.get('hits', 0))
        
        return ai_explanations
        
    except Exception as e:
        progress_container.empty()
        st.warning(f"⚠️ AI explanations unavailable: {str(e)}")
        st.info("💡 Validation results still available with rule-based analysis")
        return {}

def render_main_content_optimized(enable_ai: bool, severity_filter: list, max_ai_claims: int):
    """Render main content area with performance monitoring"""
    
    if not SessionManager.has_data():
        # Show welcome screen
        ValidationUI.render_welcome_screen()
        return
    
    # Show performance header
    PerformanceUI.render_performance_header()
    
    # Show processing controls
    validate_button = SidebarControls.render_processing_controls()
    
    # Handle validation processing
    if validate_button:
        process_claims_validation_optimized(enable_ai, max_ai_claims)
    
    # Display results if available
    if SessionManager.has_results():
        validation_results = SessionManager.get_validation_results()
        ai_explanations = SessionManager.get_ai_explanations()
        uploaded_data = SessionManager.get_uploaded_data()
        
        # Show performance dashboard
        PerformanceUI.render_real_time_performance_dashboard()
        
        # Show AI summary dashboard if AI explanations were generated
        if ai_explanations:
            AIUIComponents.render_ai_summary_dashboard(ai_explanations)
        
        # Render comprehensive results
        render_kpi_dashboard(validation_results)
        render_business_impact_summary(validation_results, uploaded_data)
        render_error_trend_chart(validation_results)
        ValidationUI.render_validation_results(
            validation_results, severity_filter, enable_ai, max_ai_claims, ai_explanations
        )
        ValidationUI.render_duplicate_errors(validation_results)
        render_claim_details_table(uploaded_data, validation_results)
        render_action_recommendations(validation_results)
        
        # Performance monitoring section
        PerformanceUI.render_detailed_performance_stats()
        PerformanceUI.render_performance_controls()
        
        # Export options
        ValidationUI.render_export_options(validation_results)

def main():
    """Main application orchestration function with performance optimization"""
    # Initialize application and performance monitoring
    load_custom_css()
    SessionManager.initialize_session_state()
    PerformanceManager.initialize_performance_state()
    
    # Render header
    render_header()
    
    # Render sidebar and get user settings
    enable_ai, ai_depth, max_ai_claims, severity_filter = SidebarControls.render_sidebar()
    
    # Render main content with performance optimization
    render_main_content_optimized(enable_ai, severity_filter, max_ai_claims)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()