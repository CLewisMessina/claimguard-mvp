# src/performance_ui.py
"""
ClaimGuard - Performance Monitoring UI Components
Real-time performance analytics and optimization displays
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time
from typing import Dict, Any, List
from ai_cache import PerformanceManager

class PerformanceUI:
    """UI components for performance monitoring and analytics"""
    
    @staticmethod
    def render_performance_header():
        """Render performance optimization banner"""
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #10b981, #059669);
            color: white;
            padding: 0.8rem 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 8px;
            text-align: center;
        ">
            <strong>⚡ PERFORMANCE OPTIMIZED</strong> - Advanced AI Caching & Batch Processing Active
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_real_time_performance_dashboard():
        """Render comprehensive real-time performance dashboard"""
        st.markdown("### ⚡ Real-Time Performance Analytics")
        
        # Get performance data
        cache_stats = PerformanceManager.get_ai_cache().get_stats()
        batch_stats = PerformanceManager.get_batch_processor().get_performance_stats()
        
        # Main performance metrics row
        PerformanceUI._render_main_performance_metrics(cache_stats, batch_stats)
        
        # Performance charts
        PerformanceUI._render_performance_charts(cache_stats, batch_stats)
        
        # Optimization recommendations
        PerformanceUI._render_optimization_recommendations(cache_stats, batch_stats)
    
    @staticmethod
    def _render_main_performance_metrics(cache_stats: Dict, batch_stats: Dict):
        """Render main performance KPI metrics"""
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            hit_rate = cache_stats['hit_rate_percent']
            delta_color = "normal" if hit_rate >= 50 else "inverse"
            st.metric(
                label="🎯 Cache Hit Rate",
                value=f"{hit_rate}%",
                delta=f"Target: 70%+",
                delta_color=delta_color,
                help="Percentage of AI requests served from cache - higher is better"
            )
        
        with col2:
            throughput = batch_stats.get('throughput_per_second', 0)
            st.metric(
                label="⚡ Processing Speed",
                value=f"{throughput:.1f}/sec",
                delta="Real-time",
                help="Claims processed per second with AI analysis"
            )
        
        with col3:
            memory_eff = cache_stats['memory_efficiency']
            delta_color = "inverse" if memory_eff >= 90 else "normal"
            st.metric(
                label="💾 Memory Efficiency",
                value=f"{memory_eff}%",
                delta=f"Used: {cache_stats['cache_size']}/{cache_stats['max_size']}",
                delta_color=delta_color,
                help="Cache memory utilization - optimal range 60-80%"
            )
        
        with col4:
            ai_calls = batch_stats.get('ai_calls_made', 0)
            cache_hits = cache_stats.get('hits', 0)
            total_requests = ai_calls + cache_hits
            cost_savings = (cache_hits / total_requests * 100) if total_requests > 0 else 0
            st.metric(
                label="💰 Cost Savings",
                value=f"{cost_savings:.1f}%",
                delta=f"${cache_hits * 0.002:.3f} saved" if cache_hits > 0 else "No savings yet",
                help="Estimated API cost savings from caching"
            )
        
        with col5:
            performance_gain = batch_stats.get('performance_improvement', 0)
            st.metric(
                label="🚀 Speed Boost",
                value=f"+{performance_gain:.1f}%",
                delta="vs no cache",
                help="Performance improvement from optimization"
            )
    
    @staticmethod
    def _render_performance_charts(cache_stats: Dict, batch_stats: Dict):
        """Render performance analytics charts"""
        col1, col2 = st.columns(2)
        
        with col1:
            PerformanceUI._render_cache_performance_chart(cache_stats)
        
        with col2:
            PerformanceUI._render_processing_efficiency_chart(batch_stats)
    
    @staticmethod
    def _render_cache_performance_chart(cache_stats: Dict):
        """Render cache performance donut chart"""
        hits = cache_stats.get('hits', 0)
        misses = cache_stats.get('misses', 0)
        
        if hits + misses > 0:
            fig = go.Figure(data=[go.Pie(
                labels=['Cache Hits', 'Cache Misses'],
                values=[hits, misses],
                hole=0.6,
                marker_colors=['#10b981', '#ef4444']
            )])
            
            fig.update_layout(
                title="Cache Performance Distribution",
                height=300,
                annotations=[dict(text=f"{cache_stats['hit_rate_percent']}%<br>Hit Rate", 
                                x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Cache performance data will appear after processing claims")
    
    @staticmethod
    def _render_processing_efficiency_chart(batch_stats: Dict):
        """Render processing efficiency metrics"""
        total_processed = batch_stats.get('total_processed', 0)
        ai_calls = batch_stats.get('ai_calls_made', 0)
        cache_hits = total_processed - ai_calls if total_processed >= ai_calls else 0
        
        if total_processed > 0:
            # Create stacked bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Cache Hits',
                x=['Processing Efficiency'],
                y=[cache_hits],
                marker_color='#10b981'
            ))
            
            fig.add_trace(go.Bar(
                name='AI API Calls',
                x=['Processing Efficiency'],
                y=[ai_calls],
                marker_color='#3b82f6'
            ))
            
            fig.update_layout(
                title="Processing Method Distribution",
                barmode='stack',
                height=300,
                yaxis_title="Number of Claims"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Processing efficiency data will appear after validation")
    
    @staticmethod
    def _render_optimization_recommendations(cache_stats: Dict, batch_stats: Dict):
        """Render performance optimization recommendations"""
        st.markdown("### 🎯 Performance Optimization Insights")
        
        recommendations = PerformanceUI._generate_performance_recommendations(cache_stats, batch_stats)
        
        if recommendations:
            for rec in recommendations:
                icon = rec['icon']
                priority = rec['priority']
                title = rec['title']
                description = rec['description']
                
                # Color coding by priority
                colors = {
                    'HIGH': {'bg': '#fee2e2', 'border': '#dc2626'},
                    'MEDIUM': {'bg': '#fef3c7', 'border': '#d97706'},
                    'LOW': {'bg': '#d1fae5', 'border': '#10b981'},
                    'INFO': {'bg': '#dbeafe', 'border': '#2563eb'}
                }
                
                color = colors.get(priority, colors['INFO'])
                
                st.markdown(f"""
                <div style="
                    background-color: {color['bg']};
                    border-left: 4px solid {color['border']};
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-radius: 5px;
                ">
                    <h4>{icon} {title} ({priority} Priority)</h4>
                    <p>{description}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Performance is optimal - no recommendations at this time")
    
    @staticmethod
    def _generate_performance_recommendations(cache_stats: Dict, batch_stats: Dict) -> List[Dict]:
        """Generate intelligent performance recommendations"""
        recommendations = []
        
        hit_rate = cache_stats.get('hit_rate_percent', 0)
        memory_eff = cache_stats.get('memory_efficiency', 0)
        total_requests = cache_stats.get('total_requests', 0)
        
        # Cache hit rate recommendations
        if hit_rate < 30 and total_requests > 10:
            recommendations.append({
                'icon': '🎯',
                'priority': 'HIGH',
                'title': 'Low Cache Hit Rate Detected',
                'description': f'Current hit rate of {hit_rate}% is below optimal. Consider processing similar claim types in batches to improve caching efficiency.'
            })
        elif hit_rate >= 70:
            recommendations.append({
                'icon': '🏆',
                'priority': 'INFO',
                'title': 'Excellent Cache Performance',
                'description': f'Cache hit rate of {hit_rate}% is excellent! This is saving significant processing time and API costs.'
            })
        
        # Memory efficiency recommendations
        if memory_eff >= 95:
            recommendations.append({
                'icon': '💾',
                'priority': 'MEDIUM',
                'title': 'Cache Memory Nearly Full',
                'description': 'Consider increasing cache size or clearing old entries to maintain optimal performance.'
            })
        elif memory_eff < 20 and total_requests > 20:
            recommendations.append({
                'icon': '📈',
                'priority': 'LOW',
                'title': 'Cache Underutilized',
                'description': 'Cache has plenty of space available. Current usage pattern is efficient for memory.'
            })
        
        # Processing speed recommendations
        throughput = batch_stats.get('throughput_per_second', 0)
        if throughput > 5:
            recommendations.append({
                'icon': '⚡',
                'priority': 'INFO',
                'title': 'High-Speed Processing',
                'description': f'Processing {throughput:.1f} claims/second - excellent performance for real-time validation!'
            })
        
        # Cost optimization insights
        ai_calls = batch_stats.get('ai_calls_made', 0)
        if ai_calls > 0:
            estimated_savings = cache_stats.get('hits', 0) * 0.002
            if estimated_savings > 0.01:
                recommendations.append({
                    'icon': '💰',
                    'priority': 'INFO',
                    'title': 'Significant Cost Savings',
                    'description': f'Cache optimization has saved approximately ${estimated_savings:.3f} in API costs this session.'
                })
        
        return recommendations
    
    @staticmethod
    def render_detailed_performance_stats():
        """Render detailed performance statistics in expandable section"""
        with st.expander("📊 Detailed Performance Analytics", expanded=False):
            cache_stats = PerformanceManager.get_ai_cache().get_stats()
            batch_stats = PerformanceManager.get_batch_processor().get_performance_stats()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🗄️ AI Cache Statistics:**")
                st.json({
                    "Hit Rate": f"{cache_stats['hit_rate_percent']}%",
                    "Total Requests": cache_stats['total_requests'],
                    "Cache Hits": cache_stats['hits'],
                    "Cache Misses": cache_stats['misses'],
                    "Cache Size": f"{cache_stats['cache_size']}/{cache_stats['max_size']}",
                    "Memory Efficiency": f"{cache_stats['memory_efficiency']}%",
                    "Evictions": cache_stats['evictions']
                })
            
            with col2:
                st.markdown("**⚡ Batch Processing Statistics:**")
                processing_time = batch_stats.get('processing_time_seconds', 0)
                st.json({
                    "Total Processed": batch_stats.get('total_processed', 0),
                    "Processing Time": f"{processing_time}s",
                    "Throughput": f"{batch_stats.get('throughput_per_second', 0):.1f}/sec",
                    "AI Calls Made": batch_stats.get('ai_calls_made', 0),
                    "Cache Hit Rate": f"{batch_stats.get('cache_hit_rate', 0)}%",
                    "Performance Gain": f"+{batch_stats.get('performance_improvement', 0)}%"
                })
    
    @staticmethod
    def render_performance_controls():
        """Render performance management controls"""
        st.markdown("### ⚙️ Performance Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear Cache", help="Clear AI response cache to free memory"):
                PerformanceManager.clear_performance_cache()
                st.success("✅ Cache cleared successfully!")
                st.rerun()
        
        with col2:
            cache_size = st.selectbox(
                "Cache Size",
                [50, 100, 200, 500],
                index=1,
                help="Maximum number of AI responses to cache"
            )
            if st.button("📏 Resize Cache"):
                # Note: In a real implementation, you'd update the cache size
                st.info(f"Cache size would be updated to {cache_size} entries")
        
        with col3:
            if st.button("📊 Export Performance Report"):
                # Generate performance report
                cache_stats = PerformanceManager.get_ai_cache().get_stats()
                batch_stats = PerformanceManager.get_batch_processor().get_performance_stats()
                
                report_data = {
                    **cache_stats,
                    **batch_stats,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                st.download_button(
                    label="💾 Download Report",
                    data=str(report_data),
                    file_name=f"claimguard_performance_{int(time.time())}.json",
                    mime="application/json"
                )
    
    @staticmethod
    def render_processing_progress_enhanced(current: int, total: int, stage: str, cache_hits: int = 0):
        """Render enhanced processing progress with cache information"""
        progress = current / total if total > 0 else 0
        cache_rate = (cache_hits / current * 100) if current > 0 else 0
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <h4>⚡ {stage}: Processing {current} of {total} claims</h4>
            <div style="display: flex; align-items: center; gap: 1rem; margin: 0.5rem 0;">
                <div style="flex: 1;">
                    <div style="
                        background-color: #e5e7eb; 
                        border-radius: 10px; 
                        height: 24px; 
                        overflow: hidden;
                    ">
                        <div style="
                            background: linear-gradient(90deg, #10b981, #059669); 
                            height: 100%; 
                            width: {progress * 100}%; 
                            transition: width 0.3s ease;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-weight: bold;
                            font-size: 12px;
                        ">
                            {progress:.0%}
                        </div>
                    </div>
                </div>
                <div style="
                    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                    color: white;
                    padding: 0.3rem 0.8rem;
                    border-radius: 15px;
                    font-size: 12px;
                    font-weight: bold;
                ">
                    🎯 {cache_rate:.0f}% Cache Hit Rate
                </div>
            </div>
            <p style="margin-top: 0.5rem; color: #64748b; font-size: 14px;">
                ⚡ Performance optimized: {cache_hits} cached responses • {current - cache_hits} AI calls
            </p>
        </div>
        """, unsafe_allow_html=True)