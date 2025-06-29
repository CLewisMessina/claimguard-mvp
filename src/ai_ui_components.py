# src/ai_ui_components.py - STREAMLINED VERSION
"""
ClaimGuard - Streamlined AI UI Components
Focus on business value, remove performance monitoring clutter
"""

import streamlit as st
import plotly.express as px
from typing import Dict, Any
from ai_explainer import ExplanationResult

class AIUIComponents:
    """Streamlined UI components for displaying AI analysis results"""
    
    @staticmethod
    def render_enhanced_ai_explanation(explanation: ExplanationResult):
        """Render AI explanation focused on business value"""
        
        # AI-powered banner
        st.markdown("""
        <div class="ai-powered-banner">
            <strong>🤖 AI HEALTHCARE EXPERT ANALYSIS</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Main AI analysis container
        st.markdown('<div class="ai-analysis-container">', unsafe_allow_html=True)
        
        # Risk level indicator
        risk_class = f"risk-{explanation.risk_level.lower()}"
        st.markdown(f"""
        <div class="risk-indicator {risk_class}">
            🚨 RISK LEVEL: {explanation.risk_level}
        </div>
        """, unsafe_allow_html=True)
        
        # Core business analysis sections
        AIUIComponents._render_ai_section(
            "🏥 Medical Reasoning", 
            explanation.medical_reasoning
        )
        
        AIUIComponents._render_ai_section(
            "💼 Business Impact", 
            explanation.business_impact
        )
        
        AIUIComponents._render_ai_section(
            "💰 Financial Impact", 
            explanation.financial_impact
        )
        
        AIUIComponents._render_ai_section(
            "📋 Regulatory Concerns", 
            explanation.regulatory_concerns
        )
        
        AIUIComponents._render_ai_section(
            "🎯 Recommended Actions", 
            explanation.next_steps
        )
        
        # Fraud indicators (if any)
        if explanation.fraud_indicators:
            AIUIComponents._render_fraud_indicators(explanation.fraud_indicators)
        
        # Confidence badge
        st.markdown(f"""
        <div class="confidence-badge">
            🎯 AI Confidence: {explanation.confidence:.0%}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def _render_ai_section(title: str, content: str):
        """Render individual AI analysis section"""
        st.markdown('<div class="ai-section">', unsafe_allow_html=True)
        st.markdown(f"#### {title}")
        st.markdown(f"<p>{content}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def _render_fraud_indicators(fraud_indicators: list):
        """Render fraud risk indicators"""
        st.markdown("""
        <div class="fraud-indicators">
            <h5>🔍 Fraud Risk Indicators</h5>
            <ul>
        """, unsafe_allow_html=True)
        
        for indicator in fraud_indicators:
            st.markdown(f"<li>{indicator}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_summary_dashboard(ai_explanations: Dict[str, ExplanationResult]):
        """Render streamlined AI analysis summary focused on business value"""
        if not ai_explanations:
            return
        
        st.markdown("### 🤖 AI Analysis Summary")
        
        # Calculate AI analysis metrics
        total_analyses = len(ai_explanations)
        risk_levels = [exp.risk_level for exp in ai_explanations.values()]
        avg_confidence = sum(exp.confidence for exp in ai_explanations.values()) / total_analyses
        
        risk_counts = {
            'HIGH': risk_levels.count('HIGH'),
            'MEDIUM': risk_levels.count('MEDIUM'),
            'LOW': risk_levels.count('LOW')
        }
        
        # Streamlined business-focused metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🧠 AI Analyses",
                value=f"{total_analyses}",
                help="Number of AI-powered explanations generated"
            )
        
        with col2:
            st.metric(
                label="🚨 High Risk",
                value=f"{risk_counts['HIGH']}",
                delta=f"{(risk_counts['HIGH']/total_analyses*100):.0f}% of total",
                delta_color="inverse",
                help="Claims requiring immediate attention"
            )
        
        with col3:
            st.metric(
                label="🎯 Avg Confidence",
                value=f"{avg_confidence:.0%}",
                help="Average AI confidence across all analyses"
            )
        
        with col4:
            fraud_indicators_count = sum(len(exp.fraud_indicators) for exp in ai_explanations.values())
            st.metric(
                label="🔍 Fraud Flags",
                value=f"{fraud_indicators_count}",
                help="Total fraud risk indicators identified"
            )
        
        # Simple risk distribution chart (removed complex analytics)
        if risk_counts:
            AIUIComponents._render_simple_risk_chart(risk_counts)
    
    @staticmethod
    def _render_simple_risk_chart(risk_counts: dict):
        """Render simplified risk distribution chart"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Simple risk distribution pie chart
            fig_risk = px.pie(
                values=list(risk_counts.values()),
                names=list(risk_counts.keys()),
                title="Risk Assessment Distribution",
                color=list(risk_counts.keys()),
                color_discrete_map={'HIGH': '#dc2626', 'MEDIUM': '#d97706', 'LOW': '#10b981'}
            )
            fig_risk.update_layout(height=300, showlegend=True)
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Simple risk summary
            st.markdown("#### Risk Summary")
            for risk_level, count in risk_counts.items():
                percentage = (count / sum(risk_counts.values()) * 100)
                color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[risk_level]
                st.markdown(f"{color} **{risk_level}**: {count} claims ({percentage:.0f}%)")
    
    @staticmethod
    def render_simple_processing_status(current_claim: int, total_claims: int, claim_id: str):
        """Render simplified processing status"""
        progress = current_claim / total_claims if total_claims > 0 else 0
        
        st.markdown(f"""
        <div style="margin: 1rem 0; text-align: center;">
            <h4>🤖 Generating AI Analysis</h4>
            <p>Processing claim {claim_id} ({current_claim} of {total_claims})</p>
            <div style="
                background-color: #e5e7eb; 
                border-radius: 10px; 
                height: 20px; 
                overflow: hidden;
                margin: 1rem 0;
            ">
                <div style="
                    background: linear-gradient(90deg, #7ed321, #6bb91a); 
                    height: 100%; 
                    width: {progress * 100}%; 
                    transition: width 0.3s ease;
                "></div>
            </div>
            <p style="color: #667085;">{progress:.0%} complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_unavailable_message():
        """Render message when AI analysis is unavailable"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
        ">
            <h4>⚠️ AI Analysis Temporarily Unavailable</h4>
            <p>Advanced AI explanations are currently unavailable. Validation results are still available.</p>
            <p><strong>💡 Tip:</strong> Check your OpenAI API key configuration to enable AI-powered explanations.</p>
        </div>
        """, unsafe_allow_html=True)