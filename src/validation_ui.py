# src/validation_ui.py
"""
ClaimGuard - Validation Results UI Components - DARK THEME
Display validation results, duplicate errors, and export options
FIXED: Expanders collapsed by default, no empty AI sections
"""

import streamlit as st
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
        """Render detailed validation results with fixed expander behavior and conditional AI sections"""
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
        
        # Display results with optimized AI analysis
        for claim_id, claim_results in results_by_claim.items():
            
            # Determine the primary severity for the expander
            severities = [result.severity for result in claim_results]
            primary_severity = "HIGH" if "HIGH" in severities else ("MEDIUM" if "MEDIUM" in severities else "LOW")
            
            # Icon based on severity
            severity_icon = "🚨" if primary_severity == "HIGH" else ("⚠️" if primary_severity == "MEDIUM" else "ℹ️")
            
            # Check if we have actual AI analysis for this claim
            has_ai_analysis = enable_ai and claim_id in ai_explanations and ai_explanations[claim_id] is not None
            ai_indicator = "🤖 AI ANALYSIS" if has_ai_analysis else ""
            
            # FIXED: Always collapsed by default (expanded=False)
            with st.expander(f"{severity_icon} Claim {claim_id} - {len(claim_results)} Error(s) {ai_indicator}", expanded=False):
                
                for result in claim_results:
                    ValidationUI._render_single_validation_error(result)
                
                # FIXED: Only render AI sections when there's actual content
                if has_ai_analysis:
                    ai_explanation = ai_explanations[claim_id]
                    AIUIComponents.render_enhanced_ai_explanation(ai_explanation)
                
                # NO empty placeholder sections - cleaner presentation
    
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
        """Render welcome screen when no data is loaded with dark theme and parallel processing info"""
        st.markdown("### 👋 Welcome to ClaimGuard")
        st.markdown("""
        ClaimGuard helps healthcare organizations validate claims before payment using **advanced AI analysis with parallel processing**.
        
        **🚀 Enhanced AI Capabilities:**
        """)
        
        # Render steps with modern styling
        ValidationUI._render_welcome_steps()
        
        st.markdown("""
        **Or try our sample dataset** to see ClaimGuard's lightning-fast parallel AI in action!
        """)
        
        ValidationUI._render_csv_format_info()
        ValidationUI._render_enhanced_ai_features_info()
    
    @staticmethod
    def _render_welcome_steps():
        """Render welcome steps with modern icon styling and parallel processing emphasis"""
        steps = [
            ("📁", "Upload your claims CSV file using the sidebar"),
            ("🚀", "Click \"Validate Claims with Parallel AI\" for 5x faster processing"),
            ("🤖", "Review AI-powered medical reasoning with lightning-fast analysis"),
            ("📊", "Export comprehensive validation reports with full AI insights")
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
    def _render_enhanced_ai_features_info():
        """Render enhanced AI capabilities information with parallel processing details"""
        with st.expander("🤖 Enhanced AI Analysis Features"):
            st.markdown("""
            **Advanced AI provides:**
            - **Medical Reasoning**: Clinical explanations with specific medical knowledge
            - **Business Impact**: Operational consequences and workflow disruption analysis
            - **Financial Impact**: Specific dollar impact calculations and recovery costs
            - **Regulatory Concerns**: CMS compliance issues and audit risk factors
            - **Fraud Detection**: Risk indicators and suspicious pattern identification
            - **Actionable Next Steps**: Prioritized recommendations with timelines
            
            **⚡ Performance Enhancements:**
            - **Parallel Processing**: 5 simultaneous AI workers for maximum speed
            - **Smart Caching**: Instant responses for similar claim patterns
            - **Optimized Workflows**: 5x faster analysis compared to sequential processing
            - **Scalable Architecture**: Handles large datasets efficiently
            """)