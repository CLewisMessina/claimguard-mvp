# src/data_handlers.py
"""
ClaimGuard - Data Processing and File Handling
Centralized data upload, validation, and processing logic
"""

import streamlit as st
import pandas as pd
import os
from typing import Optional, Tuple
from session_management import SessionManager

class DataHandler:
    """Handles data upload, validation, and processing for ClaimGuard"""
    
    @staticmethod
    def handle_file_upload() -> Optional[pd.DataFrame]:
        """Handle CSV file upload with validation"""
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with healthcare claims data"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                if DataHandler.validate_csv_structure(df):
                    SessionManager.set_uploaded_data(df)
                    st.success(f"✅ Loaded {len(df)} claims")
                    
                    # Show data preview
                    with st.expander("📊 Data Preview"):
                        st.dataframe(df.head(3))
                    
                    return df
                else:
                    st.error("❌ Invalid CSV structure. Please check required columns.")
                    return None
                    
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                return None
        
        return None
    
    @staticmethod
    def load_sample_dataset() -> Optional[pd.DataFrame]:
        """Load sample dataset for demonstration"""
        try:
            sample_path = "data/synthetic_claims_dataset.csv"
            if os.path.exists(sample_path):
                df = pd.read_csv(sample_path)
                SessionManager.set_uploaded_data(df)
                st.success(f"✅ Loaded {len(df)} sample claims")
                return df
            else:
                st.error("Sample dataset not found. Run generate_dataset.py first.")
                return None
        except Exception as e:
            st.error(f"❌ Error loading sample data: {str(e)}")
            return None
    
    @staticmethod
    def validate_csv_structure(df: pd.DataFrame) -> bool:
        """Validate that CSV has required columns"""
        required_columns = [
            'claim_id', 'patient_id', 'age', 'gender', 'cpt_code',
            'diagnosis_code', 'service_date', 'provider_id', 'charge_amount'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            return False
        
        return True
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> dict:
        """Get summary statistics for uploaded data"""
        return {
            'total_claims': len(df),
            'unique_patients': df['patient_id'].nunique(),
            'date_range': (df['service_date'].min(), df['service_date'].max()),
            'total_amount': df['charge_amount'].sum(),
            'avg_amount': df['charge_amount'].mean(),
            'gender_distribution': df['gender'].value_counts().to_dict(),
            'age_range': (df['age'].min(), df['age'].max())
        }
    
    @staticmethod
    def export_summary_report(validation_results: dict) -> str:
        """Create summary report CSV data"""
        summary_data = {
            'Metric': ['Total Claims', 'Claims with Errors', 'Error Rate (%)', 'Processing Time (s)'],
            'Value': [
                validation_results['summary']['total_claims'],
                validation_results['summary']['claims_with_errors'],
                validation_results['summary']['error_rate_percent'],
                validation_results['summary']['processing_time_seconds']
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        return summary_df.to_csv(index=False)
    
    @staticmethod
    def export_detailed_results(validation_results: dict) -> str:
        """Create detailed results CSV data"""
        detailed_data = []
        for result in validation_results['validation_results']:
            detailed_data.append({
                'Claim_ID': result.claim_id,
                'Error_Type': result.error_type,
                'Severity': result.severity,
                'Description': result.description,
                'Recommendation': result.recommendation,
                'Confidence': result.confidence
            })
        
        if detailed_data:
            detailed_df = pd.DataFrame(detailed_data)
            return detailed_df.to_csv(index=False)
        return ""