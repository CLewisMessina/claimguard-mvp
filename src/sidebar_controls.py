# src/sidebar_controls.py
"""
ClaimGuard - Sidebar Controls and Settings
Centralized sidebar management with user controls and settings
"""

import streamlit as st
from typing import Tuple
from data_handlers import DataHandler

class SidebarControls:
    """Manages sidebar controls and user settings"""
    
    @staticmethod
    def render_sidebar() -> Tuple[bool, list, str, int]:
        """Render complete sidebar with all controls"""
        with st.sidebar:
            st.markdown("### 📋 ClaimGuard Controls")
            
            # File upload section
            SidebarControls._render_file_upload_section()
            
            # Sample data section
            SidebarControls._render_sample_data_section()
            
            # AI analysis settings
            ai_settings = SidebarControls._render_ai_settings()
            
            # Validation filters
            severity_filter = SidebarControls._render_validation_filters()
            
            # Information panels
            SidebarControls._render_info_panels()
            
            return ai_settings + (severity_filter,)
    
    @staticmethod
    def _render_file_upload_section():
        """Render file upload section"""
        st.markdown("#### 📁 Upload Claims Data")
        DataHandler.handle_file_upload()
    
    @staticmethod
    def _render_sample_data_section():
        """Render sample data loading section"""
        st.markdown("#### 🧪 Or Use Sample Data")
        if st.button("📥 Load Sample Dataset", type="secondary"):
            DataHandler.load_sample_dataset()
    
    @staticmethod
    def _render_ai_settings() -> Tuple[bool, str, int]:
        """Render AI analysis settings"""
        st.markdown("#### ⚙️ AI Analysis Settings")
        
        enable_ai_explanations = st.checkbox(
            "🤖 Generate AI Explanations", 
            value=True,
            help="Use advanced AI to generate detailed medical and business analysis"
        )
        
        ai_analysis_depth = st.selectbox(
            "🎯 Analysis Depth",
            ["Standard", "Detailed", "Comprehensive"],
            index=1,
            help="Choose the depth of AI analysis for each claim error"
        )
        
        max_ai_claims = st.slider(
            "📊 Max AI Analyses",
            min_value=1,
            max_value=10,
            value=5,
            help="Limit AI analysis for demo performance (production: unlimited)"
        )
        
        return enable_ai_explanations, ai_analysis_depth, max_ai_claims
    
    @staticmethod
    def _render_validation_filters() -> list:
        """Render validation filter controls"""
        st.markdown("#### 🔍 Validation Filters")
        
        severity_filter = st.multiselect(
            "Show Error Severities",
            ["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM", "LOW"],
            help="Filter results by error severity level"
        )
        
        return severity_filter
    
    @staticmethod
    def _render_info_panels():
        """Render information panels"""
        # AI capabilities panel
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI-Powered Analysis")
        st.markdown("""
        **Enhanced AI Features:**
        - Medical reasoning with clinical context
        - Financial impact calculations
        - Regulatory compliance assessment
        - Fraud risk indicators
        - Actionable next steps
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # About ClaimGuard panel
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 📖 About ClaimGuard")
        st.markdown("""
        **ClaimGuard** validates healthcare claims before payment to prevent:
        - Gender-procedure mismatches
        - Age-inappropriate procedures  
        - Anatomical logic errors
        - Severity mismatches
        - Duplicate billing
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_processing_controls():
        """Render processing control buttons"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            validate_button = st.button(
                "🔍 Validate Claims with AI Analysis", 
                type="primary", 
                key="validate_button",
                help="Run comprehensive claims validation with AI analysis"
            )
        
        with col2:
            if st.button("🔄 Reset", type="secondary", help="Clear all data and results"):
                from session_management import SessionManager
                SessionManager.clear_all()
                st.rerun()
        
        return validate_button