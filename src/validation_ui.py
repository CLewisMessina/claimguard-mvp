# src/validation_ui.py
"""
ClaimGuard - Validation Results UI Components - SHADCN INTEGRATION
Display validation results with modern shadcn/ui components
"""

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from ai_ui_components import AIUIComponents
from data_handlers import DataHandler

class ValidationUI:
    """UI components for displaying validation results with shadcn styling"""
    
    @staticmethod
    def render_validation_results(validation_results: Dict[str, Any], severity_filter: List[str], 
                                enable_ai: bool, max_ai_claims: int, ai_explanations: Dict[str, Any]):
        """Render detailed validation results with shadcn components"""
        if not validation_results:
            return
        
        st.markdown("### 🔍 Detailed Validation Results")
        
        # Filter results by severity
        filtered_results = [
            result for result in validation_results['validation_results']
            if result.severity in severity_filter
        ]
        
        if not filtered_results:
            st.info("No validation errors found matching your filter criteria. Try adjusting your severity filters.")
            return
        
        # Group results by claim ID
        results_by_claim = {}
        for result in filtered_results:
            claim_id = result.claim_id
            if claim_id not in results_by_claim:
                results_by_claim[claim_id] = []
            results_by_claim[claim_id].append(result)
        
        # Display results with enhanced AI analysis in shadcn cards
        for i, (claim_id, claim_results) in enumerate(results_by_claim.items()):
            
            # Limit AI analysis for demo performance
            show_ai_analysis = enable_ai and i < max_ai_claims
            
            # Determine the primary severity for styling
            severities = [result.severity for result in claim_results]
            primary_severity = "HIGH" if "HIGH" in severities else ("MEDIUM" if "MEDIUM" in severities else "LOW")
            
            # Choose card variant based on severity
            card_variant = "destructive" if primary_severity == "HIGH" else ("secondary" if primary_severity == "MEDIUM" else "default")
            
            with ui.card(key=f"claim_result_card_{claim_id}"):
                # Card header with severity indicator
                severity_icon = "🚨" if primary_severity == "HIGH" else ("⚠️" if primary_severity == "MEDIUM" else "ℹ️")
                ai_badge = " 🤖 AI ANALYSIS" if show_ai_analysis else ""
                
                st.markdown(f"#### {severity_icon} Claim {claim_id} - {len(claim_results)} Error(s){ai_badge}")
                
                # Render individual errors
                for result in claim_results:
                    ValidationUI._render_single_validation_error_shadcn(result)
                
                # Enhanced AI explanation display
                if show_ai_analysis and claim_id in ai_explanations:
                    ui.separator(key=f"ai_sep_{claim_id}")
                    ai_explanation = ai_explanations[claim_id]
                    AIUIComponents.render_enhanced_ai_explanation(ai_explanation)
                elif show_ai_analysis:
                    st.info("🤖 AI analysis would appear here with detailed medical reasoning and business impact assessment.")
    
    @staticmethod
    def _render_single_validation_error_shadcn(result):
        """Render a single validation error with custom styling"""
        # Determine styling based on severity
        if result.severity == "HIGH":
            css_class = "error-high"
            icon = "🚨"
        elif result.severity == "MEDIUM":
            css_class = "error-medium"
            icon = "⚠️"
        else:
            css_class = "error-low"
            icon = "ℹ️"
        
        st.markdown(f"""
        <div class="{css_class}">
            <h4>{icon} {result.error_type}</h4>
            <p><strong>Description:</strong> {result.description}</p>
            <p><strong>Recommendation:</strong> {result.recommendation}</p>
            <p><strong>Confidence:</strong> {result.confidence:.0%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_duplicate_errors(validation_results: Dict[str, Any]):
        """Render duplicate service errors with shadcn alerts"""
        if not validation_results or not validation_results['duplicate_errors']:
            return
        
        st.markdown("### 🔄 Duplicate Services Detected")
        
        for i, duplicate in enumerate(validation_results['duplicate_errors']):
            st.warning(f"⚠️ Duplicate Service: {duplicate['cpt_code']} billed {duplicate['count']} times for patient {duplicate['patient_id']} on {duplicate['service_date']}. Recommendation: {duplicate['recommendation']}")
    
    @staticmethod
    def render_export_options(validation_results: Dict[str, Any]):
        """Render data export options with shadcn buttons"""
        if not validation_results:
            return
        
        st.markdown("### 📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            summary_btn = ui.button(
                text="📊 Download Summary Report",
                variant="default",
                key="export_summary_shadcn"
            )
            
            if summary_btn:
                csv_data = DataHandler.export_summary_report(validation_results)
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"claimguard_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            detailed_btn = ui.button(
                text="📋 Download Detailed Results",
                variant="outline",
                key="export_detailed_shadcn"
            )
            
            if detailed_btn:
                csv_data = DataHandler.export_detailed_results(validation_results)
                if csv_data:
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"claimguard_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
    
    @staticmethod
    def render_welcome_screen():
        """Render welcome screen with shadcn components"""
        st.markdown("### 👋 Welcome to ClaimGuard")
        
        with ui.card(key="welcome_card"):
            st.markdown("""
            ClaimGuard helps healthcare organizations validate claims before payment using **advanced AI analysis**.
            
            **🚀 Enhanced AI Capabilities:**
            """)
            
            # Simple step display
            st.markdown("""
            **🚀 Enhanced AI Capabilities:**
            1. 📁 Upload your claims CSV file using the sidebar
            2. 🔍 Click "Validate Claims with AI Analysis" to run advanced validation  
            3. 🤖 Review AI-powered medical reasoning and business impact analysis
            4. 📊 Export comprehensive validation reports with actionable insights
            """)
            
            st.markdown("""
            **Or try our sample dataset** to see ClaimGuard's advanced AI in action!
            """)
        
        ValidationUI._render_csv_format_info_shadcn()
        ValidationUI._render_ai_features_info_shadcn()
    
    @staticmethod
    def _render_welcome_steps_shadcn():
        """Render welcome steps with shadcn components"""
        steps = [
            ("📁", "Upload your claims CSV file using the sidebar"),
            ("🔍", "Click \"Validate Claims with AI Analysis\" to run advanced validation"),
            ("🤖", "Review AI-powered medical reasoning and business impact analysis"),
            ("📊", "Export comprehensive validation reports with actionable insights")
        ]
        
        for i, (icon, description) in enumerate(steps, 1):
            ui.alert(
                text=f"{icon} {i}. {description}",
                description="Step-by-step workflow",
                variant="secondary",
                key=f"welcome_step_{i}"
            )
    
    @staticmethod
    def _render_csv_format_info_shadcn():
        """Render CSV format information with standard expander"""
        with st.expander("📋 Required CSV Format"):
            st.markdown("""
            Your CSV file should include these columns:
            - `claim_id`: Unique identifier for each claim
            - `patient_id`: Patient identifier  
            - `age`: Patient age
            - `gender`: Patient gender (M/F)
            - `cpt_code`: Procedure code (CPT)
            - `diagnosis_code`: Diagnosis code (ICD-10)
            - `service_date`: Date of service
            - `provider_id`: Provider identifier
            - `charge_amount`: Claim amount
            """)
    
    @staticmethod
    def _render_ai_features_info_shadcn():
        """Render AI capabilities information with standard expander"""
        with st.expander("🤖 AI Analysis Features"):
            st.markdown("""
            **Advanced AI provides:**
            - **Medical Reasoning**: Clinical explanations with specific medical knowledge
            - **Business Impact**: Operational consequences and workflow disruption analysis
            - **Financial Impact**: Specific dollar impact calculations and recovery costs
            - **Regulatory Concerns**: CMS compliance issues and audit risk factors
            - **Fraud Detection**: Risk indicators and suspicious pattern identification
            - **Actionable Next Steps**: Prioritized recommendations with timelines
            """)
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from ai_ui_components import AIUIComponents
from data_handlers import DataHandler

class ValidationUI:
    """UI components for displaying validation results with dark theme"""
    
    @staticmethod
    def render_validation_results(validation_results: Dict[str, Any], severity_filter: List[str], 
                                enable_ai: bool, max_ai_claims: int, ai_explanations: Dict[str, Any]):
        """Render detailed validation results with enhanced AI explanations"""
        if not validation_results:
            return
        
        st.markdown("### 🔍 Detailed Validation Results")
        
        # Filter results by severity
        filtered_results = [
            result for result in validation_results['validation_results']
            if result.severity in severity_filter
        ]
        
        if not filtered_results:
            st.info("No validation errors found matching your filter criteria.")
            return
        
        # Group results by claim ID
        results_by_claim = {}
        for result in filtered_results:
            claim_id = result.claim_id
            if claim_id not in results_by_claim:
                results_by_claim[claim_id] = []
            results_by_claim[claim_id].append(result)
        
        # Display results with enhanced AI analysis
        for i, (claim_id, claim_results) in enumerate(results_by_claim.items()):
            
            # Limit AI analysis for demo performance
            show_ai_analysis = enable_ai and i < max_ai_claims
            
            # Determine the primary severity for the expander
            severities = [result.severity for result in claim_results]
            primary_severity = "HIGH" if "HIGH" in severities else ("MEDIUM" if "MEDIUM" in severities else "LOW")
            
            # Icon based on severity
            severity_icon = "🚨" if primary_severity == "HIGH" else ("⚠️" if primary_severity == "MEDIUM" else "ℹ️")
            
            with st.expander(f"{severity_icon} Claim {claim_id} - {len(claim_results)} Error(s) {'🤖 AI ANALYSIS' if show_ai_analysis else ''}", expanded=show_ai_analysis):
                
                for result in claim_results:
                    ValidationUI._render_single_validation_error(result)
                    
                    # Enhanced AI explanation display
                    if show_ai_analysis and claim_id in ai_explanations:
                        ai_explanation = ai_explanations[claim_id]
                        AIUIComponents.render_enhanced_ai_explanation(ai_explanation)
                    
                    elif show_ai_analysis:
                        st.info("🤖 AI analysis would appear here with detailed medical reasoning and business impact assessment.")
    
    @staticmethod
    def _render_single_validation_error(result):
        """Render a single validation error with dark theme styling"""
        # Determine styling based on severity
        if result.severity == "HIGH":
            css_class = "error-high"
            icon = "🚨"
        elif result.severity == "MEDIUM":
            css_class = "error-medium"
            icon = "⚠️"
        else:
            css_class = "error-low"
            icon = "ℹ️"
        
        st.markdown(f"""
        <div class="{css_class}">
            <h4>{icon} {result.error_type}</h4>
            <p><strong>Description:</strong> {result.description}</p>
            <p><strong>Recommendation:</strong> {result.recommendation}</p>
            <p><strong>Confidence:</strong> {result.confidence:.0%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_duplicate_errors(validation_results: Dict[str, Any]):
        """Render duplicate service errors with dark theme"""
        if not validation_results or not validation_results['duplicate_errors']:
            return
        
        st.markdown("### 🔄 Duplicate Services Detected")
        
        for duplicate in validation_results['duplicate_errors']:
            st.markdown(f"""
            <div class="error-medium">
                <h4>⚠️ Duplicate Service</h4>
                <p><strong>Patient:</strong> {duplicate['patient_id']}</p>
                <p><strong>Procedure:</strong> {duplicate['cpt_code']} (billed {duplicate['count']} times)</p>
                <p><strong>Date:</strong> {duplicate['service_date']}</p>
                <p><strong>Recommendation:</strong> {duplicate['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_export_options(validation_results: Dict[str, Any]):
        """Render data export options with dark theme"""
        if not validation_results:
            return
        
        st.markdown("### 📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ValidationUI._render_summary_export(validation_results)
        
        with col2:
            ValidationUI._render_detailed_export(validation_results)
    
    @staticmethod
    def _render_summary_export(validation_results: Dict[str, Any]):
        """Render summary report export button"""
        if st.button("📊 Download Summary Report", type="primary"):
            csv_data = DataHandler.export_summary_report(validation_results)
            
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"claimguard_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    @staticmethod
    def _render_detailed_export(validation_results: Dict[str, Any]):
        """Render detailed results export button"""
        if st.button("📋 Download Detailed Results", type="secondary"):
            csv_data = DataHandler.export_detailed_results(validation_results)
            
            if csv_data:
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_data,
                    file_name=f"claimguard_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    @staticmethod
    def render_welcome_screen():
        """Render welcome screen when no data is loaded with dark theme"""
        st.markdown("### 👋 Welcome to ClaimGuard")
        st.markdown("""
        ClaimGuard helps healthcare organizations validate claims before payment using **advanced AI analysis**.
        
        **🚀 Enhanced AI Capabilities:**
        """)
        
        # Render steps with modern styling
        ValidationUI._render_welcome_steps()
        
        st.markdown("""
        **Or try our sample dataset** to see ClaimGuard's advanced AI in action!
        """)
        
        ValidationUI._render_csv_format_info()
        ValidationUI._render_ai_features_info()
    
    @staticmethod
    def _render_welcome_steps():
        """Render welcome steps with modern icon styling"""
        steps = [
            ("📁", "Upload your claims CSV file using the sidebar"),
            ("🔍", "Click \"Validate Claims with AI Analysis\" to run advanced validation"),
            ("🤖", "Review AI-powered medical reasoning and business impact analysis"),
            ("📊", "Export comprehensive validation reports with actionable insights")
        ]
        
        for i, (icon, description) in enumerate(steps, 1):
            st.markdown(f"""
            <div class="welcome-step">
                <span class="step-icon">{icon}</span>
                <span>{i}. {description}</span>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_csv_format_info():
        """Render CSV format information with dark theme"""
        with st.expander("📋 Required CSV Format"):
            st.markdown("""
            Your CSV file should include these columns:
            - `claim_id`: Unique identifier for each claim
            - `patient_id`: Patient identifier  
            - `age`: Patient age
            - `gender`: Patient gender (M/F)
            - `cpt_code`: Procedure code (CPT)
            - `diagnosis_code`: Diagnosis code (ICD-10)
            - `service_date`: Date of service
            - `provider_id`: Provider identifier
            - `charge_amount`: Claim amount
            """)
    
    @staticmethod
    def _render_ai_features_info():
        """Render AI capabilities information with dark theme"""
        with st.expander("🤖 AI Analysis Features"):
            st.markdown("""
            **Advanced AI provides:**
            - **Medical Reasoning**: Clinical explanations with specific medical knowledge
            - **Business Impact**: Operational consequences and workflow disruption analysis
            - **Financial Impact**: Specific dollar impact calculations and recovery costs
            - **Regulatory Concerns**: CMS compliance issues and audit risk factors
            - **Fraud Detection**: Risk indicators and suspicious pattern identification
            - **Actionable Next Steps**: Prioritized recommendations with timelines
            """)