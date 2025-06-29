# src/ai_ui_components.py - EXECUTIVE MUTED GREEN THEME
"""
ClaimGuard - AI UI Components with Executive Muted Green Theme
Focus on financial impact with sophisticated styling
"""

import streamlit as st
import plotly.express as px
from typing import Dict, Any
from ai_explainer import ExplanationResult

class AIUIComponents:
    """AI UI components optimized for executive muted green theme and financial focus"""
    
    @staticmethod
    def render_enhanced_ai_explanation(explanation: ExplanationResult):
        """Render AI explanation focused on executive business value with muted green theme"""
        
        # Executive AI-powered banner
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, var(--highlight-gold), var(--accent-beige));
            color: var(--primary-sage);
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 700;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">
            🤖 EXECUTIVE AI ASSESSMENT
        </div>
        """, unsafe_allow_html=True)
        
        # Main AI analysis container with executive styling
        st.markdown('<div style="background: linear-gradient(135deg, var(--secondary-charcoal) 0%, var(--primary-sage) 100%); border: 3px solid var(--highlight-gold); border-radius: 20px; padding: 2.5rem; margin: 2rem 0; color: var(--text-light); box-shadow: 0 20px 40px rgba(42, 45, 42, 0.3);">', unsafe_allow_html=True)
        
        # Risk level indicator with executive styling
        risk_class = f"risk-{explanation.risk_level.lower()}"
        st.markdown(f"""
        <div style="
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            background-color: var(--error-muted);
            color: white;
        ">
            🚨 RISK LEVEL: {explanation.risk_level}
        </div>
        """, unsafe_allow_html=True)
        
        # Core executive analysis sections
        AIUIComponents._render_executive_ai_section(
            "🏥 Medical Assessment", 
            explanation.medical_reasoning
        )
        
        AIUIComponents._render_executive_ai_section(
            "💼 Business Impact", 
            explanation.business_impact
        )
        
        AIUIComponents._render_executive_ai_section(
            "💰 Financial Implications", 
            explanation.financial_impact
        )
        
        AIUIComponents._render_executive_ai_section(
            "📋 Regulatory Considerations", 
            explanation.regulatory_concerns
        )
        
        AIUIComponents._render_executive_ai_section(
            "🎯 Executive Actions", 
            explanation.next_steps
        )
        
        # Fraud indicators (if any) with executive styling
        if explanation.fraud_indicators:
            AIUIComponents._render_executive_fraud_indicators(explanation.fraud_indicators)
        
        # Confidence badge with executive styling
        st.markdown(f"""
        <div style="
            background: var(--highlight-gold);
            color: var(--primary-sage);
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
            margin-top: 1rem;
            font-size: 0.9rem;
        ">
            🎯 AI Confidence: {explanation.confidence:.0%}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def _render_executive_ai_section(title: str, content: str):
        """Render individual AI analysis section with executive styling"""
        st.markdown(f"""
        <div style="
            background: rgba(242, 242, 240, 0.08);
            border: 1px solid var(--success-muted);
            border-radius: 15px;
            padding: 1.8rem;
            margin: 1.5rem 0;
            backdrop-filter: blur(10px);
        ">
            <h4 style="
                color: var(--highlight-gold);
                margin: 0 0 1rem 0;
                font-weight: 600;
                font-size: 1.2rem;
            ">{title}</h4>
            <p style="
                color: var(--text-light);
                line-height: 1.7;
                margin: 0;
            ">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_executive_fraud_indicators(fraud_indicators: list):
        """Render fraud risk indicators with executive muted green theme"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, var(--primary-sage), var(--secondary-charcoal));
            border: 2px solid var(--error-muted);
            color: var(--text-light);
            border-radius: 15px;
            padding: 1.8rem;
            margin: 1.5rem 0;
        ">
            <h5 style="
                color: var(--error-muted);
                margin-bottom: 1rem;
                font-weight: 600;
                font-size: 1.1rem;
            ">🔍 Executive Risk Indicators</h5>
            <ul style="margin: 0; padding-left: 1.5rem;">
        """, unsafe_allow_html=True)
        
        for indicator in fraud_indicators:
            st.markdown(f"<li style='margin: 0.5rem 0; color: var(--text-light);'>{indicator}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_summary_dashboard(ai_explanations: Dict[str, ExplanationResult]):
        """Render AI analysis summary focused on executive financial value"""
        if not ai_explanations:
            return
        
        st.markdown("### 🤖 Executive AI Intelligence Summary")
        
        # Calculate AI analysis metrics
        total_analyses = len(ai_explanations)
        risk_levels = [exp.risk_level for exp in ai_explanations.values()]
        avg_confidence = sum(exp.confidence for exp in ai_explanations.values()) / total_analyses
        
        risk_counts = {
            'HIGH': risk_levels.count('HIGH'),
            'MEDIUM': risk_levels.count('MEDIUM'),
            'LOW': risk_levels.count('LOW')
        }
        
        # Executive-focused metrics with financial emphasis
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🧠 AI Assessments",
                value=f"{total_analyses}",
                help="Number of comprehensive AI-powered financial and medical analyses"
            )
        
        with col2:
            st.metric(
                label="🚨 Critical Risk",
                value=f"{risk_counts['HIGH']}",
                delta=f"{(risk_counts['HIGH']/total_analyses*100):.0f}% of portfolio",
                delta_color="inverse",
                help="Claims requiring immediate executive attention and payment hold"
            )
        
        with col3:
            st.metric(
                label="🎯 AI Confidence",
                value=f"{avg_confidence:.0%}",
                help="Average AI confidence in financial and medical assessments"
            )
        
        with col4:
            fraud_indicators_count = sum(len(exp.fraud_indicators) for exp in ai_explanations.values())
            st.metric(
                label="🔍 Fraud Signals",
                value=f"{fraud_indicators_count}",
                help="Total fraud risk indicators identified across portfolio"
            )
        
        # Executive risk distribution chart
        if risk_counts:
            AIUIComponents._render_executive_risk_chart(risk_counts)
    
    @staticmethod
    def _render_executive_risk_chart(risk_counts: dict):
        """Render executive risk distribution chart with muted green theme"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Executive risk distribution with muted colors
            fig_risk = px.pie(
                values=list(risk_counts.values()),
                names=list(risk_counts.keys()),
                title="Executive Risk Portfolio Distribution",
                color=list(risk_counts.keys()),
                color_discrete_map={
                    'HIGH': '#A67B7B',     # Muted error red
                    'MEDIUM': '#C4A661',   # Muted warning
                    'LOW': '#6B8E6F'       # Muted success green
                }
            )
            
            # Executive dark theme styling
            fig_risk.update_layout(
                height=300, 
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#F2F2F0',
                title_font_color='#E8C547',
                title_font_size=14,
                title_font_family='Satoshi'
            )
            
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Executive risk summary with financial focus
            st.markdown("#### Executive Risk Assessment")
            for risk_level, count in risk_counts.items():
                percentage = (count / sum(risk_counts.values()) * 100)
                color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[risk_level]
                
                # Add financial impact context
                if risk_level == 'HIGH':
                    context = "Immediate payment hold required"
                elif risk_level == 'MEDIUM':
                    context = "Manual review before payment"
                else:
                    context = "Monitor for patterns"
                
                st.markdown(f"{color} **{risk_level}**: {count} claims ({percentage:.0f}%) - {context}")
    
    @staticmethod
    def render_simple_processing_status(current_claim: int, total_claims: int, claim_id: str):
        """Render simplified processing status with executive muted green theme"""
        progress = current_claim / total_claims if total_claims > 0 else 0
        
        st.markdown(f"""
        <div style="
            margin: 1rem 0; 
            text-align: center;
            background: linear-gradient(135deg, var(--primary-sage), var(--surface-elevated));
            border: 2px solid var(--highlight-gold);
            border-radius: 15px;
            padding: 2rem;
            color: var(--text-light);
        ">
            <h4>🤖 Executive AI Analysis in Progress</h4>
            <p>Processing claim {claim_id} ({current_claim} of {total_claims})</p>
            <div style="
                background-color: var(--secondary-charcoal); 
                border-radius: 10px; 
                height: 20px; 
                overflow: hidden;
                margin: 1rem 0;
                border: 1px solid var(--success-muted);
            ">
                <div style="
                    background: linear-gradient(90deg, var(--highlight-gold), var(--accent-beige)); 
                    height: 100%; 
                    width: {progress * 100}%; 
                    transition: width 0.3s ease;
                "></div>
            </div>
            <p style="color: var(--accent-beige);">{progress:.0%} complete</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_ai_unavailable_message():
        """Render message when AI analysis is unavailable with executive theme"""
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, var(--warning-muted), var(--accent-beige));
            color: var(--primary-sage);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            text-align: center;
            border: 2px solid var(--highlight-gold);
        ">
            <h4>⚠️ Executive AI Analysis Temporarily Unavailable</h4>
            <p>Advanced financial and medical AI assessments are currently unavailable. Core validation results remain accessible.</p>
            <p><strong>💡 Executive Note:</strong> Verify AI service configuration to enable comprehensive business impact analysis.</p>
        </div>
        """, unsafe_allow_html=True)