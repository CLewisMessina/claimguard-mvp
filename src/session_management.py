# src/session_management.py
"""
ClaimGuard - Session State Management
Centralized session state handling for the Streamlit application
"""

import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd

class SessionManager:
    """Centralized session state management for ClaimGuard"""
    
    @staticmethod
    def initialize_session_state():
        """Initialize all session state variables"""
        if 'validation_results' not in st.session_state:
            st.session_state.validation_results = None
        if 'uploaded_data' not in st.session_state:
            st.session_state.uploaded_data = None
        if 'ai_explanations' not in st.session_state:
            st.session_state.ai_explanations = {}
        if 'processing_complete' not in st.session_state:
            st.session_state.processing_complete = False
        if 'ai_analysis_enabled' not in st.session_state:
            st.session_state.ai_analysis_enabled = True
    
    @staticmethod
    def set_uploaded_data(data: pd.DataFrame):
        """Set uploaded claims data"""
        st.session_state.uploaded_data = data
        st.session_state.processing_complete = False
        st.session_state.validation_results = None
        st.session_state.ai_explanations = {}
    
    @staticmethod
    def get_uploaded_data() -> Optional[pd.DataFrame]:
        """Get uploaded claims data"""
        return st.session_state.uploaded_data
    
    @staticmethod
    def set_validation_results(results: Dict[str, Any]):
        """Set validation results"""
        st.session_state.validation_results = results
    
    @staticmethod
    def get_validation_results() -> Optional[Dict[str, Any]]:
        """Get validation results"""
        return st.session_state.validation_results
    
    @staticmethod
    def set_ai_explanations(explanations: Dict[str, Any]):
        """Set AI explanations"""
        st.session_state.ai_explanations = explanations
    
    @staticmethod
    def get_ai_explanations() -> Dict[str, Any]:
        """Get AI explanations"""
        return st.session_state.ai_explanations
    
    @staticmethod
    def mark_processing_complete():
        """Mark processing as complete"""
        st.session_state.processing_complete = True
    
    @staticmethod
    def is_processing_complete() -> bool:
        """Check if processing is complete"""
        return st.session_state.processing_complete
    
    @staticmethod
    def has_data() -> bool:
        """Check if data is available"""
        return st.session_state.uploaded_data is not None
    
    @staticmethod
    def has_results() -> bool:
        """Check if validation results are available"""
        return st.session_state.validation_results is not None
    
    @staticmethod
    def has_ai_explanations() -> bool:
        """Check if AI explanations are available"""
        return bool(st.session_state.ai_explanations)
    
    @staticmethod
    def clear_all():
        """Clear all session data"""
        st.session_state.validation_results = None
        st.session_state.uploaded_data = None
        st.session_state.ai_explanations = {}
        st.session_state.processing_complete = False