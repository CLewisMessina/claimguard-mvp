# src/sidebar_controls.py
"""
ClaimGuard - Streamlined Sidebar Controls - SHADCN INTEGRATION
Focus on core functionality with modern shadcn/ui components
"""

import streamlit as st
import streamlit_shadcn_ui as ui
from typing import Tuple
from data_handlers import DataHandler

class SidebarControls:
    """Manages streamlined sidebar controls with shadcn styling"""
    
    @staticmethod
    def render_sidebar() -> Tuple[bool, list, str, int]:
        """Render streamlined sidebar with shadcn components"""
        with st.sidebar:
            st.markdown("### 📋 ClaimGuard Controls")
            
            # File upload section
            SidebarControls._render_file_upload_section()
            
            # Sample data section
            SidebarControls._render_sample_data_section()
            
            # AI analysis settings (simplified)
            ai_settings = SidebarControls._render_simplified_ai_settings()
            
            # Validation filters
            severity_filter = SidebarControls._render_validation_filters()
            
            # Information panels (streamlined)
            SidebarControls._render_streamlined_info_panels()
            
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
    def _render_simplified_ai_settings() -> Tuple[bool, str, int]:
        """Render simplified AI analysis settings"""
        st.markdown("#### ⚙️ AI Analysis Settings")
        
        # Use standard Streamlit checkbox for reliability
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
            help="Limit AI analysis for demo performance"
        )
        
        return enable_ai_explanations, ai_analysis_depth, max_ai_claims
    
    @staticmethod
    def _render_validation_filters() -> list:
        """Render validation filter controls"""
        st.markdown("#### 🔍 Display Filters")
        
        severity_filter = st.multiselect(
            "Show Error Severities",
            ["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM", "LOW"],
            help="Filter results by error severity level"
        )
        
        return severity_filter
    
    @staticmethod
    def _render_streamlined_info_panels():
        """Render streamlined information panels with shadcn cards"""
        
        # Core value proposition panel
        with ui.card(key="sidebar_value_card"):
            st.markdown("### 🎯 Core Value")
            st.markdown("""
            **ClaimGuard prevents:**
            - Gender-procedure mismatches
            - Age-inappropriate procedures  
            - Anatomical logic errors
            - Duplicate billing
            - Severity mismatches
            """)
        
        # AI capabilities panel
        with ui.card(key="sidebar_ai_card"):
            st.markdown("### 🤖 AI Features")
            st.markdown("""
            **AI-Powered Analysis:**
            - Medical reasoning
            - Financial impact
            - Regulatory concerns
            - Actionable next steps
            - Fraud risk assessment
            """)
        
        # Healthcare platform panel
        with ui.card(key="sidebar_platform_card"):
            st.markdown("### 🏥 Platform Benefits")
            st.markdown("""
            **Enterprise Healthcare AI:**
            - Pre-payment validation
            - Real-time error detection
            - Compliance monitoring
            - Cost savings optimization
            - Workflow automation
            """)
    
    @staticmethod
    def render_processing_controls():
        """Render processing control buttons with reliable styling"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            validate_button = st.button(
                "🔍 Validate Claims with AI",
                type="primary",
                key="validate_claims_btn",
                help="Run comprehensive claims validation with AI analysis"
            )
        
        with col2:
            reset_button = st.button(
                "🔄 Reset",
                type="secondary",
                key="reset_btn",
                help="Clear all data and results"
            )
            
            if reset_button:
                from session_management import SessionManager
                SessionManager.clear_all()
                st.rerun()
        
        return validate_button