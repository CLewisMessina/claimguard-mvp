# src/ai_ui_components.py
"""
ClaimGuard - AI-Specific UI Components
Advanced AI explanation display and analysis components
"""

import streamlit as st
import plotly.express as px
from typing import Dict, Any
from ai_explainer import ExplanationResult

class AIUIComponents:
    """UI components for displaying AI analysis results"""
    
    @staticmethod
    def render_enhanced_ai_explanation(explanation: ExplanationResult):
        """Render enhanced AI explanation with professional healthcare styling"""
        
        # AI-powered banner
        st.markdown("""
        <div class="ai-powered-banner">
            <strong>🤖 AI HEALTHCARE EXPERT ANALYSIS</strong> - Advanced Medical & Business Intelligence
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
        
        # Medical reasoning section
        AIUIComponents._render_ai_section(
            "🏥 Medical Reasoning", 
            explanation.medical_reasoning
        )
        
        # Business impact section
        AIUIComponents._render_ai_section(
            "💼 Business Impact", 
            explanation.business_impact
        )
        
        # Financial impact section
        AIUIComponents._render_ai_section(
            "💰 Financial Impact", 
            explanation.financial_impact
        )
        
        # Regulatory concerns section
        AIUIComponents._render_ai_section(
            "📋 Regulatory Concerns", 
            explanation.regulatory_concerns
        )
        
        # Next steps section
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
        """Render summary dashboard of AI analysis results"""
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
        
        # AI metrics dashboard
        AIUIComponents._render_ai_metrics(total_analyses, risk_counts, avg_confidence, ai_explanations)
        
        # Risk distribution charts
        AIUIComponents._render_ai_charts(risk_counts, ai_explanations)
    
    @staticmethod
    def _render_ai_metrics(total_analyses: int, risk_counts: dict, avg_confidence: float, ai_explanations: dict):
        """Render AI metrics dashboard"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🤖 AI Analyses",
                value=f"{total_analyses}",
                help="Total number of AI-powered explanations generated"
            )
        
        with col2:
            st.metric(
                label="🚨 High Risk",
                value=f"{risk_counts['HIGH']}",
                delta=f"{(risk_counts['HIGH']/total_analyses*100):.0f}% of total",
                delta_color="inverse"
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
                label="🔍 Fraud Indicators",
                value=f"{fraud_indicators_count}",
                help="Total fraud risk indicators identified"
            )
    
    @staticmethod
    def _render_ai_charts(risk_counts: dict, ai_explanations: dict):
        """Render AI analysis charts"""
        if not risk_counts:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution pie chart
            fig_risk = px.pie(
                values=list(risk_counts.values()),
                names=list(risk_counts.keys()),
                title="AI Risk Assessment Distribution",
                color=list(risk_counts.keys()),
                color_discrete_map={'HIGH': '#dc2626', 'MEDIUM': '#d97706', 'LOW': '#10b981'}
            )
            fig_risk.update_layout(height=300)
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Confidence distribution histogram
            confidence_scores = [exp.confidence for exp in ai_explanations.values()]
            fig_confidence = px.histogram(
                x=confidence_scores,
                title="AI Confidence Score Distribution",
                nbins=5,
                color_discrete_sequence=['#3b82f6']
            )
            fig_confidence.update_layout(
                height=300,
                xaxis_title="Confidence Score",
                yaxis_title="Number of Analyses"
            )
            st.plotly_chart(fig_confidence, use_container_width=True)
    
    @staticmethod
    def render_ai_processing_status(current_claim: int, total_claims: int, claim_id: str):
        """Render AI processing status indicator"""
        progress = current_claim / total_claims if total_claims > 0 else 0
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <h4>🤖 Generating AI Analysis: Claim {claim_id}</h4>
            <div style="
                background-color: #e5e7eb; 
                border-radius: 10px; 
                height: 20px; 
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, #667eea, #764ba2); 
                    height: 100%; 
                    width: {progress * 100}%; 
                    transition: width 0.3s ease;
                "></div>
            </div>
            <p style="margin-top: 0.5rem; color: #64748b;">
                Processing {current_claim} of {total_claims} AI analyses ({progress:.0%} complete)
            </p>
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
            <p>Advanced AI explanations are currently unavailable. Validation results are still available with rule-based analysis.</p>
            <p><strong>💡 Tip:</strong> Check your OpenAI API key configuration to enable AI-powered explanations.</p>
        </div>
        """, unsafe_allow_html=True)