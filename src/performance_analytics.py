# src/performance_analytics.py
"""
ClaimGuard - Advanced Performance Analytics and Monitoring
Real-time performance tracking, bottleneck detection, and optimization insights
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import statistics
import streamlit as st

@dataclass
class PerformanceMetric:
    """Individual performance metric data point"""
    timestamp: datetime
    metric_name: str
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProcessingSession:
    """Complete processing session analytics"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_claims: int = 0
    processed_claims: int = 0
    ai_calls_made: int = 0
    cache_hits: int = 0
    errors: int = 0
    performance_metrics: List[PerformanceMetric] = field(default_factory=list)
    
    @property
    def duration_seconds(self) -> float:
        """Get session duration in seconds"""
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate for session"""
        total_requests = self.ai_calls_made + self.cache_hits
        return (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
    
    @property
    def processing_speed(self) -> float:
        """Calculate claims processed per second"""
        return self.processed_claims / self.duration_seconds if self.duration_seconds > 0 else 0

class PerformanceMonitor:
    """Advanced performance monitoring and analytics system"""
    
    def __init__(self):
        self.current_session: Optional[ProcessingSession] = None
        self.historical_sessions: List[ProcessingSession] = []
        self.real_time_metrics: Dict[str, List[PerformanceMetric]] = {}
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Performance thresholds for alerting
        self.thresholds = {
            'cache_hit_rate_min': 50.0,  # Minimum acceptable cache hit rate
            'processing_speed_min': 3.0,  # Minimum claims per second
            'error_rate_max': 5.0,        # Maximum error rate percentage
            'response_time_max': 2.0      # Maximum AI response time (seconds)
        }
    
    def start_session(self, session_id: str, total_claims: int) -> ProcessingSession:
        """Start a new performance monitoring session"""
        self.current_session = ProcessingSession(
            session_id=session_id,
            start_time=datetime.now(),
            total_claims=total_claims
        )
        
        self._start_real_time_monitoring()
        return self.current_session
    
    def end_session(self) -> Optional[ProcessingSession]:
        """End current monitoring session"""
        if self.current_session:
            self.current_session.end_time = datetime.now()
            self.historical_sessions.append(self.current_session)
            
            # Stop real-time monitoring
            self._stop_real_time_monitoring()
            
            completed_session = self.current_session
            self.current_session = None
            return completed_session
        
        return None
    
    def record_metric(self, metric_name: str, value: float, metadata: Dict[str, Any] = None):
        """Record a performance metric"""
        if metadata is None:
            metadata = {}
        
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            metadata=metadata
        )
        
        # Add to real-time metrics
        if metric_name not in self.real_time_metrics:
            self.real_time_metrics[metric_name] = []
        
        self.real_time_metrics[metric_name].append(metric)
        
        # Add to current session if active
        if self.current_session:
            self.current_session.performance_metrics.append(metric)
            
            # Update session counters based on metric type
            if metric_name == 'ai_call_completed':
                self.current_session.ai_calls_made += 1
            elif metric_name == 'cache_hit':
                self.current_session.cache_hits += 1
            elif metric_name == 'claim_processed':
                self.current_session.processed_claims += 1
            elif metric_name == 'processing_error':
                self.current_session.errors += 1
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """Get current real-time performance statistics"""
        if not self.current_session:
            return {}
        
        session = self.current_session
        
        # Calculate recent performance metrics
        recent_metrics = self._get_recent_metrics(minutes=5)
        
        return {
            'session_id': session.session_id,
            'duration_seconds': session.duration_seconds,
            'progress_percent': (session.processed_claims / session.total_claims * 100) if session.total_claims > 0 else 0,
            'cache_hit_rate': session.cache_hit_rate,
            'processing_speed': session.processing_speed,
            'total_claims': session.total_claims,
            'processed_claims': session.processed_claims,
            'ai_calls_made': session.ai_calls_made,
            'cache_hits': session.cache_hits,
            'errors': session.errors,
            'recent_response_time': self._get_average_response_time(recent_metrics),
            'memory_usage': self._estimate_memory_usage(),
            'performance_alerts': self._check_performance_alerts()
        }
    
    def get_session_analytics(self, session_id: str = None) -> Dict[str, Any]:
        """Get comprehensive analytics for a specific session"""
        target_session = self.current_session
        
        if session_id:
            target_session = next(
                (s for s in self.historical_sessions if s.session_id == session_id),
                None
            )
        
        if not target_session:
            return {}
        
        return {
            'session_summary': {
                'session_id': target_session.session_id,
                'start_time': target_session.start_time.isoformat(),
                'end_time': target_session.end_time.isoformat() if target_session.end_time else None,
                'duration_seconds': target_session.duration_seconds,
                'total_claims': target_session.total_claims,
                'processed_claims': target_session.processed_claims,
                'completion_rate': (target_session.processed_claims / target_session.total_claims * 100) if target_session.total_claims > 0 else 0
            },
            'performance_summary': {
                'cache_hit_rate': target_session.cache_hit_rate,
                'processing_speed': target_session.processing_speed,
                'ai_calls_made': target_session.ai_calls_made,
                'cache_hits': target_session.cache_hits,
                'error_count': target_session.errors,
                'error_rate': (target_session.errors / target_session.processed_claims * 100) if target_session.processed_claims > 0 else 0
            },
            'detailed_metrics': self._analyze_session_metrics(target_session),
            'performance_insights': self._generate_session_insights(target_session),
            'optimization_recommendations': self._get_optimization_recommendations(target_session)
        }
    
    def get_historical_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get historical performance trends"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = [
            s for s in self.historical_sessions 
            if s.start_time >= cutoff_date and s.end_time is not None
        ]
        
        if not recent_sessions:
            return {'message': 'No historical data available'}
        
        return {
            'summary': {
                'total_sessions': len(recent_sessions),
                'total_claims_processed': sum(s.processed_claims for s in recent_sessions),
                'average_processing_speed': statistics.mean([s.processing_speed for s in recent_sessions]),
                'average_cache_hit_rate': statistics.mean([s.cache_hit_rate for s in recent_sessions]),
                'total_ai_calls': sum(s.ai_calls_made for s in recent_sessions),
                'total_cache_hits': sum(s.cache_hits for s in recent_sessions)
            },
            'trends': {
                'processing_speed_trend': self._calculate_trend([s.processing_speed for s in recent_sessions]),
                'cache_efficiency_trend': self._calculate_trend([s.cache_hit_rate for s in recent_sessions]),
                'session_duration_trend': self._calculate_trend([s.duration_seconds for s in recent_sessions])
            },
            'performance_comparison': self._compare_sessions(recent_sessions),
            'best_performing_session': max(recent_sessions, key=lambda s: s.processing_speed).session_id,
            'optimization_opportunities': self._identify_optimization_opportunities(recent_sessions)
        }
    
    def _start_real_time_monitoring(self):
        """Start real-time performance monitoring thread"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
    
    def _stop_real_time_monitoring(self):
        """Stop real-time performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
    
    def _monitoring_loop(self):
        """Real-time monitoring loop"""
        while self.monitoring_active:
            try:
                # Record system performance metrics
                self.record_metric('system_timestamp', time.time())
                
                # Check for performance alerts
                alerts = self._check_performance_alerts()
                if alerts:
                    self.record_metric('performance_alert', len(alerts), {'alerts': alerts})
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _get_recent_metrics(self, minutes: int = 5) -> List[PerformanceMetric]:
        """Get metrics from the last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = []
        
        for metric_list in self.real_time_metrics.values():
            recent_metrics.extend([m for m in metric_list if m.timestamp >= cutoff_time])
        
        return sorted(recent_metrics, key=lambda m: m.timestamp)
    
    def _get_average_response_time(self, metrics: List[PerformanceMetric]) -> float:
        """Calculate average AI response time from metrics"""
        response_times = [
            m.value for m in metrics 
            if m.metric_name == 'ai_response_time'
        ]
        
        return statistics.mean(response_times) if response_times else 0.0
    
    def _estimate_memory_usage(self) -> Dict[str, float]:
        """Estimate current memory usage"""
        # Simplified memory usage estimation
        cache_entries = sum(len(metrics) for metrics in self.real_time_metrics.values())
        estimated_mb = cache_entries * 0.002  # Rough estimate
        
        return {
            'estimated_mb': estimated_mb,
            'cache_entries': cache_entries,
            'usage_level': 'low' if estimated_mb < 50 else 'medium' if estimated_mb < 200 else 'high'
        }
    
    def _check_performance_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance threshold violations"""
        alerts = []
        
        if not self.current_session:
            return alerts
        
        session = self.current_session
        
        # Cache hit rate alert
        if session.cache_hit_rate < self.thresholds['cache_hit_rate_min']:
            alerts.append({
                'type': 'cache_efficiency',
                'severity': 'warning',
                'message': f'Cache hit rate ({session.cache_hit_rate:.1f}%) below minimum threshold ({self.thresholds["cache_hit_rate_min"]}%)',
                'recommendation': 'Consider processing similar claim types together to improve cache efficiency'
            })
        
        # Processing speed alert
        if session.processing_speed < self.thresholds['processing_speed_min']:
            alerts.append({
                'type': 'processing_speed',
                'severity': 'warning',
                'message': f'Processing speed ({session.processing_speed:.1f}/sec) below minimum threshold ({self.thresholds["processing_speed_min"]}/sec)',
                'recommendation': 'Consider increasing batch size or optimizing AI response configuration'
            })
        
        # Error rate alert
        if session.processed_claims > 0:
            error_rate = (session.errors / session.processed_claims * 100)
            if error_rate > self.thresholds['error_rate_max']:
                alerts.append({
                    'type': 'error_rate',
                    'severity': 'error',
                    'message': f'Error rate ({error_rate:.1f}%) exceeds maximum threshold ({self.thresholds["error_rate_max"]}%)',
                    'recommendation': 'Review error logs and consider adjusting validation parameters'
                })
        
        return alerts
    
    def _analyze_session_metrics(self, session: ProcessingSession) -> Dict[str, Any]:
        """Analyze detailed metrics for a session"""
        metrics_by_type = {}
        
        for metric in session.performance_metrics:
            if metric.metric_name not in metrics_by_type:
                metrics_by_type[metric.metric_name] = []
            metrics_by_type[metric.metric_name].append(metric.value)
        
        analysis = {}
        for metric_name, values in metrics_by_type.items():
            if values:
                analysis[metric_name] = {
                    'count': len(values),
                    'average': statistics.mean(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0
                }
        
        return analysis
    
    def _generate_session_insights(self, session: ProcessingSession) -> List[str]:
        """Generate insights for a session"""
        insights = []
        
        # Cache efficiency insights
        if session.cache_hit_rate > 80:
            insights.append(f"Excellent cache efficiency ({session.cache_hit_rate:.1f}%) - optimal performance achieved")
        elif session.cache_hit_rate > 60:
            insights.append(f"Good cache efficiency ({session.cache_hit_rate:.1f}%) - room for minor improvements")
        else:
            insights.append(f"Cache efficiency ({session.cache_hit_rate:.1f}%) needs improvement - consider batching similar claims")
        
        # Processing speed insights
        if session.processing_speed > 15:
            insights.append(f"High processing speed ({session.processing_speed:.1f}/sec) - excellent system performance")
        elif session.processing_speed > 8:
            insights.append(f"Good processing speed ({session.processing_speed:.1f}/sec) - satisfactory performance")
        else:
            insights.append(f"Processing speed ({session.processing_speed:.1f}/sec) could be improved with optimization")
        
        # Session duration insights
        if session.duration_seconds < 60:
            insights.append("Quick processing session - ideal for interactive demonstrations")
        elif session.duration_seconds < 300:
            insights.append("Standard processing duration - good balance of speed and thoroughness")
        else:
            insights.append("Extended processing session - consider optimization for large datasets")
        
        return insights
    
    def _get_optimization_recommendations(self, session: ProcessingSession) -> List[str]:
        """Get optimization recommendations for a session"""
        recommendations = []
        
        # Based on cache performance
        if session.cache_hit_rate < 50:
            recommendations.append("Improve cache efficiency by processing similar claim types in sequence")
            recommendations.append("Consider increasing cache size to retain more responses")
        
        # Based on processing speed
        if session.processing_speed < 5:
            recommendations.append("Increase batch size to improve processing throughput")
            recommendations.append("Consider reducing AI analysis depth for faster processing")
        
        # Based on error rate
        if session.processed_claims > 0:
            error_rate = (session.errors / session.processed_claims * 100)
            if error_rate > 5:
                recommendations.append("Review data quality to reduce processing errors")
                recommendations.append("Implement additional data validation before processing")
        
        # Based on duration
        if session.duration_seconds > 300 and session.total_claims < 100:
            recommendations.append("Processing taking longer than expected - check network connectivity")
            recommendations.append("Consider using smaller batch sizes for better responsiveness")
        
        return recommendations
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear trend calculation
        x = list(range(len(values)))
        n = len(values)
        
        slope = (n * sum(x[i] * values[i] for i in range(n)) - sum(x) * sum(values)) / (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
        
        if slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _compare_sessions(self, sessions: List[ProcessingSession]) -> Dict[str, Any]:
        """Compare performance across multiple sessions"""
        if len(sessions) < 2:
            return {}
        
        speeds = [s.processing_speed for s in sessions]
        cache_rates = [s.cache_hit_rate for s in sessions]
        
        return {
            'speed_improvement': ((speeds[-1] - speeds[0]) / speeds[0] * 100) if speeds[0] > 0 else 0,
            'cache_efficiency_change': cache_rates[-1] - cache_rates[0],
            'consistency_score': 100 - (statistics.stdev(speeds) / statistics.mean(speeds) * 100) if speeds else 0,
            'best_session_speed': max(speeds),
            'worst_session_speed': min(speeds)
        }
    
    def _identify_optimization_opportunities(self, sessions: List[ProcessingSession]) -> List[str]:
        """Identify optimization opportunities from historical data"""
        opportunities = []
        
        speeds = [s.processing_speed for s in sessions]
        cache_rates = [s.cache_hit_rate for s in sessions]
        
        # Speed optimization opportunities
        if max(speeds) > min(speeds) * 1.5:
            opportunities.append("Significant performance variation detected - investigate optimal configurations")
        
        # Cache optimization opportunities
        avg_cache_rate = statistics.mean(cache_rates)
        if avg_cache_rate < 70:
            opportunities.append("Overall cache efficiency below optimal - consider workflow improvements")
        
        # Consistency opportunities
        if len(speeds) > 3:
            speed_std = statistics.stdev(speeds)
            speed_mean = statistics.mean(speeds)
            if speed_std / speed_mean > 0.3:
                opportunities.append("Performance consistency issues - standardize processing parameters")
        
        return opportunities

# Streamlit integration for performance analytics UI
def render_advanced_performance_analytics():
    """Render advanced performance analytics dashboard"""
    st.markdown("### 📈 Advanced Performance Analytics")
    
    # Get performance monitor instance from session state
    if 'performance_monitor' not in st.session_state:
        st.session_state.performance_monitor = PerformanceMonitor()
    
    monitor = st.session_state.performance_monitor
    
    # Current session analytics
    if monitor.current_session:
        render_real_time_analytics(monitor)
    
    # Historical analytics
    render_historical_analytics(monitor)
    
    # Performance insights
    render_performance_insights(monitor)

def render_real_time_analytics(monitor: PerformanceMonitor):
    """Render real-time performance analytics"""
    st.markdown("#### ⚡ Real-Time Session Analytics")
    
    stats = monitor.get_real_time_stats()
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Progress", f"{stats['progress_percent']:.1f}%")
        with col2:
            st.metric("⚡ Speed", f"{stats['processing_speed']:.1f}/sec")
        with col3:
            st.metric("🎯 Cache Rate", f"{stats['cache_hit_rate']:.1f}%")
        with col4:
            st.metric("⏱️ Duration", f"{stats['duration_seconds']:.0f}s")
        
        # Performance alerts
        alerts = stats.get('performance_alerts', [])
        if alerts:
            st.markdown("**⚠️ Performance Alerts:**")
            for alert in alerts:
                severity_color = {'warning': '🟡', 'error': '🔴', 'info': '🔵'}.get(alert['severity'], '🔵')
                st.warning(f"{severity_color} {alert['message']}")

def render_historical_analytics(monitor: PerformanceMonitor):
    """Render historical performance analytics"""
    if not monitor.historical_sessions:
        st.info("📊 Historical analytics will appear after completing processing sessions")
        return
    
    st.markdown("#### 📈 Historical Performance Trends")
    
    trends = monitor.get_historical_trends()
    
    if 'summary' in trends:
        summary = trends['summary']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🏁 Sessions", summary['total_sessions'])
        with col2:
            st.metric("📋 Claims Processed", f"{summary['total_claims_processed']:,}")
        with col3:
            st.metric("⚡ Avg Speed", f"{summary['average_processing_speed']:.1f}/sec")

def render_performance_insights(monitor: PerformanceMonitor):
    """Render performance insights and recommendations"""
    if monitor.historical_sessions:
        latest_session = monitor.historical_sessions[-1]
        analytics = monitor.get_session_analytics(latest_session.session_id)
        
        if 'performance_insights' in analytics:
            st.markdown("#### 💡 Performance Insights")
            for insight in analytics['performance_insights']:
                st.info(f"💡 {insight}")
        
        if 'optimization_recommendations' in analytics:
            st.markdown("#### 🎯 Optimization Recommendations")
            for rec in analytics['optimization_recommendations']:
                st.success(f"🎯 {rec}")

if __name__ == "__main__":
    print("📈 Testing ClaimGuard Advanced Performance Analytics...")
    
    # Test the performance monitoring system
    monitor = PerformanceMonitor()
    
    # Simulate a processing session
    session = monitor.start_session("test_session_001", 50)
    
    # Simulate some metrics
    for i in range(10):
        monitor.record_metric('claim_processed', 1)
        if i % 3 == 0:
            monitor.record_metric('cache_hit', 1)
        else:
            monitor.record_metric('ai_call_completed', 1, {'response_time': 0.5 + i * 0.1})
        time.sleep(0.1)
    
    # End session and get analytics
    completed_session = monitor.end_session()
    analytics = monitor.get_session_analytics(completed_session.session_id)
    
    print("✅ Performance analytics system operational!")
    print(f"📊 Session Analytics: {analytics['session_summary']}")
    print(f"⚡ Performance Summary: {analytics['performance_summary']}")
    print(f"💡 Insights: {analytics['performance_insights']}")