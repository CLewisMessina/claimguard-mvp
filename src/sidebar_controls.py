# src/sidebar_controls.py
"""
ClaimGuard - Streamlined Sidebar Controls - DARK THEME
Focus on core functionality with modern dark theme styling and optimized AI limits
"""

import streamlit as st
from typing import Tuple
from data_handlers import DataHandler

class SidebarControls:
    """Manages streamlined sidebar controls focused on business functionality"""
    
    @staticmethod
    def render_sidebar() -> Tuple[bool, list, str, int]:
        """Render streamlined sidebar with core controls only"""
        with st.sidebar:
            st.markdown("### 📋 ClaimGuard Controls")
            
            # File upload section
            SidebarControls._render_file_upload_section()
            
            # Sample data section
            SidebarControls._render_sample_data_section()
            
            # AI analysis settings (optimized for parallel processing)
            ai_settings = SidebarControls._render_optimized_ai_settings()
            
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
    def _render_optimized_ai_settings() -> Tuple[bool, str, int]:
        """Render optimized AI analysis settings with parallel processing support"""
        st.markdown("#### ⚙️ AI Analysis Settings")
        st.markdown("*Powered by parallel processing for maximum speed*")
        
        enable_ai_explanations = st.checkbox(
            "🤖 Generate AI Explanations", 
            value=True,
            help="Use advanced AI to generate detailed medical and business analysis (now with 5x faster parallel processing)"
        )
        
        ai_analysis_depth = st.selectbox(
            "🎯 Analysis Depth",
            ["Standard", "Detailed", "Comprehensive"],
            index=1,
            help="Choose the depth of AI analysis for each claim error"
        )
        
        # Updated default limit for better performance
        max_ai_claims = st.slider(
            "📊 Max AI Analyses",
            min_value=1,
            max_value=100,
            value=50,  # Increased from 5 to 50 for full dataset coverage
            help="Maximum number of claims to analyze with AI (parallel processing handles large volumes efficiently)"
        )
        
        # Performance indicator
        if enable_ai_explanations:
            st.markdown("""
            <div style="
                background: linear-gradient(90deg, #10b981, #059669);
                color: white;
                padding: 0.5rem;
                border-radius: 5px;
                font-size: 0.8rem;
                text-align: center;
                margin-top: 0.5rem;
            ">
                ⚡ Parallel Processing: ~5x Faster AI Analysis
            </div>
            """, unsafe_allow_html=True)
        
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
        """Render streamlined information panels with dark theme"""
        # Core value proposition panel
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 🎯 Core Value")
        st.markdown("""
        **ClaimGuard prevents:**
        - Gender-procedure mismatches
        - Age-inappropriate procedures  
        - Anatomical logic errors
        - Duplicate billing
        - Severity mismatches
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # AI capabilities panel (enhanced with parallel processing info)
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Features")
        st.markdown("""
        **AI-Powered Analysis:**
        - Medical reasoning
        - Financial impact
        - Regulatory concerns
        - Actionable next steps
        - Fraud risk assessment
        
        **⚡ Performance:**
        - 5 parallel AI workers
        - 5x faster processing
        - Real-time analysis
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Healthcare platform panel
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 🏥 Platform Benefits")
        st.markdown("""
        **Enterprise Healthcare AI:**
        - Pre-payment validation
        - Real-time error detection
        - Compliance monitoring
        - Cost savings optimization
        - Workflow automation
        - Parallel processing speed
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_processing_controls():
        """Render optimized processing control buttons with parallel processing messaging"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            validate_button = st.button(
                "🚀 Validate Claims with Parallel AI", 
                type="primary", 
                key="validate_button",
                help="Run comprehensive claims validation with 5x faster parallel AI analysis"
            )
        
        with col2:
            if st.button("🔄 Reset", type="secondary", help="Clear all data and results"):
                from session_management import SessionManager
                SessionManager.clear_all()
                st.rerun()
        
        return validate_button