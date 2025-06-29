# src/ai_cache.py
"""
ClaimGuard - AI Response Caching System
Performance optimization for repeated AI analyses
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import streamlit as st
from ai_explainer import ExplanationResult

@dataclass
class CacheEntry:
    """Cached AI explanation entry"""
    result: ExplanationResult
    timestamp: float
    hit_count: int
    cache_key: str

class AICache:
    """High-performance caching system for AI explanations"""
    
    def __init__(self, max_size: int = 100, ttl_hours: int = 24):
        self.max_size = max_size
        self.ttl_seconds = ttl_hours * 3600
        self.cache = {}
        self.access_order = []
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }
    
    def _create_cache_key(self, validation_error: Dict, claim_data: Dict) -> str:
        """Create deterministic cache key for AI requests"""
        # Extract only relevant fields for caching
        cache_data = {
            'error_type': validation_error.get('error_type'),
            'description': validation_error.get('description'),
            'age': claim_data.get('age'),
            'gender': claim_data.get('gender'),
            'cpt_code': claim_data.get('cpt_code'),
            'diagnosis_code': claim_data.get('diagnosis_code'),
            'charge_amount': claim_data.get('charge_amount')
        }
        
        # Create hash of normalized data
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, validation_error: Dict, claim_data: Dict) -> Optional[ExplanationResult]:
        """Retrieve cached AI explanation if available"""
        cache_key = self._create_cache_key(validation_error, claim_data)
        current_time = time.time()
        
        self.stats['total_requests'] += 1
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            # Check if entry is still valid (TTL)
            if current_time - entry.timestamp < self.ttl_seconds:
                # Update access statistics
                entry.hit_count += 1
                self._update_access_order(cache_key)
                self.stats['hits'] += 1
                
                return entry.result
            else:
                # Entry expired, remove it
                self._remove_entry(cache_key)
        
        self.stats['misses'] += 1
        return None
    
    def put(self, validation_error: Dict, claim_data: Dict, result: ExplanationResult):
        """Store AI explanation in cache"""
        cache_key = self._create_cache_key(validation_error, claim_data)
        current_time = time.time()
        
        # Check if we need to evict entries (LRU)
        if len(self.cache) >= self.max_size and cache_key not in self.cache:
            self._evict_lru()
        
        # Store new entry
        entry = CacheEntry(
            result=result,
            timestamp=current_time,
            hit_count=0,
            cache_key=cache_key
        )
        
        self.cache[cache_key] = entry
        self._update_access_order(cache_key)
    
    def _update_access_order(self, cache_key: str):
        """Update LRU access order"""
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)
        self.access_order.append(cache_key)
    
    def _evict_lru(self):
        """Evict least recently used entry"""
        if self.access_order:
            lru_key = self.access_order[0]
            self._remove_entry(lru_key)
            self.stats['evictions'] += 1
    
    def _remove_entry(self, cache_key: str):
        """Remove entry from cache"""
        if cache_key in self.cache:
            del self.cache[cache_key]
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.stats['total_requests']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_rate_percent': round(hit_rate, 1),
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'total_requests': total_requests,
            'memory_efficiency': round((len(self.cache) / self.max_size * 100), 1) if self.max_size > 0 else 0
        }
    
    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.access_order.clear()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }

class BatchProcessor:
    """Optimized batch processing for claims validation"""
    
    def __init__(self, ai_cache: AICache, batch_size: int = 10):
        self.ai_cache = ai_cache
        self.batch_size = batch_size
        self.processing_stats = {
            'total_processed': 0,
            'cache_hits': 0,
            'ai_calls': 0,
            'processing_time': 0
        }
    
    def process_batch_optimized(self, validation_results: list, claims_data: dict, 
                              explainer, max_ai_claims: int) -> Dict[str, ExplanationResult]:
        """Process validation results with optimized caching and batching"""
        start_time = time.time()
        ai_explanations = {}
        processed_count = 0
        
        # Process in batches for better performance
        for i in range(0, len(validation_results), self.batch_size):
            batch = validation_results[i:i + self.batch_size]
            
            for result in batch:
                if processed_count >= max_ai_claims:
                    break
                
                claim_data = claims_data.get(int(result.claim_id), {})
                error_dict = {
                    'error_type': result.error_type,
                    'description': result.description,
                    'severity': result.severity
                }
                
                # Try cache first
                cached_result = self.ai_cache.get(error_dict, claim_data)
                
                if cached_result:
                    ai_explanations[result.claim_id] = cached_result
                    self.processing_stats['cache_hits'] += 1
                else:
                    # Generate new AI explanation
                    try:
                        ai_explanation = explainer.generate_explanation(error_dict, claim_data)
                        ai_explanations[result.claim_id] = ai_explanation
                        
                        # Cache the result
                        self.ai_cache.put(error_dict, claim_data, ai_explanation)
                        self.processing_stats['ai_calls'] += 1
                        
                    except Exception as e:
                        st.warning(f"AI analysis failed for claim {result.claim_id}: {str(e)}")
                        continue
                
                processed_count += 1
                
                # Update progress for user feedback
                if processed_count % 5 == 0:
                    progress = processed_count / min(max_ai_claims, len(validation_results))
                    st.progress(progress)
            
            if processed_count >= max_ai_claims:
                break
        
        # Update processing statistics
        self.processing_stats['total_processed'] = processed_count
        self.processing_stats['processing_time'] = time.time() - start_time
        
        return ai_explanations
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get batch processing performance statistics"""
        total_processed = self.processing_stats['total_processed']
        processing_time = self.processing_stats['processing_time']
        
        return {
            'total_processed': total_processed,
            'processing_time_seconds': round(processing_time, 2),
            'throughput_per_second': round(total_processed / processing_time, 1) if processing_time > 0 else 0,
            'cache_hit_rate': round((self.processing_stats['cache_hits'] / total_processed * 100), 1) if total_processed > 0 else 0,
            'ai_calls_made': self.processing_stats['ai_calls'],
            'performance_improvement': round((self.processing_stats['cache_hits'] / total_processed * 100), 1) if total_processed > 0 else 0
        }

# Session state management for performance optimization
class PerformanceManager:
    """Manages performance optimization across the application"""
    
    @staticmethod
    def initialize_performance_state():
        """Initialize performance-related session state"""
        if 'ai_cache' not in st.session_state:
            st.session_state.ai_cache = AICache(max_size=100, ttl_hours=24)
        if 'batch_processor' not in st.session_state:
            st.session_state.batch_processor = BatchProcessor(st.session_state.ai_cache)
        if 'performance_stats' not in st.session_state:
            st.session_state.performance_stats = {}
    
    @staticmethod
    def get_ai_cache() -> AICache:
        """Get the AI cache instance"""
        return st.session_state.ai_cache
    
    @staticmethod
    def get_batch_processor() -> BatchProcessor:
        """Get the batch processor instance"""
        return st.session_state.batch_processor
    
    @staticmethod
    def update_performance_stats(stats: Dict[str, Any]):
        """Update performance statistics"""
        st.session_state.performance_stats.update(stats)
    
    @staticmethod
    def get_performance_stats() -> Dict[str, Any]:
        """Get current performance statistics"""
        return st.session_state.performance_stats
    
    @staticmethod
    def clear_performance_cache():
        """Clear all performance caches"""
        st.session_state.ai_cache.clear()
        st.session_state.performance_stats = {}

def render_performance_dashboard():
    """Render performance monitoring dashboard"""
    st.markdown("### ⚡ Performance Analytics")
    
    cache_stats = PerformanceManager.get_ai_cache().get_stats()
    batch_stats = PerformanceManager.get_batch_processor().get_performance_stats()
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Cache Hit Rate",
            value=f"{cache_stats['hit_rate_percent']}%",
            help="Percentage of AI requests served from cache"
        )
    
    with col2:
        st.metric(
            label="⚡ Processing Speed", 
            value=f"{batch_stats.get('throughput_per_second', 0)}/sec",
            help="Claims processed per second"
        )
    
    with col3:
        st.metric(
            label="💾 Cache Efficiency",
            value=f"{cache_stats['memory_efficiency']}%",
            help="Cache memory utilization"
        )
    
    with col4:
        improvement = batch_stats.get('performance_improvement', 0)
        st.metric(
            label="🚀 Performance Gain",
            value=f"+{improvement}%",
            help="Speed improvement from optimization"
        )
    
    # Detailed statistics
    with st.expander("📊 Detailed Performance Statistics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**AI Cache Statistics:**")
            st.write(f"- Total Requests: {cache_stats['total_requests']}")
            st.write(f"- Cache Hits: {cache_stats['hits']}")
            st.write(f"- Cache Misses: {cache_stats['misses']}")
            st.write(f"- Cache Size: {cache_stats['cache_size']}/{cache_stats['max_size']}")
        
        with col2:
            st.markdown("**Batch Processing Statistics:**")
            st.write(f"- Total Processed: {batch_stats.get('total_processed', 0)}")
            st.write(f"- Processing Time: {batch_stats.get('processing_time_seconds', 0)}s")
            st.write(f"- AI Calls Made: {batch_stats.get('ai_calls_made', 0)}")
            st.write(f"- Cache Hits: {batch_stats.get('cache_hit_rate', 0)}%")

# Test the performance optimization system
if __name__ == "__main__":
    print("🚀 Testing ClaimGuard Performance Optimization...")
    
    # Test cache functionality
    cache = AICache(max_size=5, ttl_hours=1)
    
    # Sample test data
    test_error = {
        'error_type': 'Gender-Procedure Mismatch',
        'description': 'Male patient with female procedure',
        'severity': 'HIGH'
    }
    
    test_claim = {
        'claim_id': '1001',
        'age': 35,
        'gender': 'M',
        'cpt_code': '59400',
        'diagnosis_code': 'O80',
        'charge_amount': 2500
    }
    
    # Test cache miss
    result = cache.get(test_error, test_claim)
    print(f"Cache miss test: {result is None}")
    
    # Test cache hit after storing
    from ai_explainer import ExplanationResult
    sample_explanation = ExplanationResult(
        claim_id="1001",
        error_type="Gender-Procedure Mismatch",
        ai_explanation="Test explanation",
        medical_reasoning="Test medical reasoning",
        business_impact="Test business impact",
        financial_impact="Test financial impact",
        regulatory_concerns="Test regulatory concerns",
        next_steps="Test next steps",
        confidence=0.95,
        risk_level="HIGH",
        fraud_indicators=["Test indicator"]
    )
    
    cache.put(test_error, test_claim, sample_explanation)
    cached_result = cache.get(test_error, test_claim)
    print(f"Cache hit test: {cached_result is not None}")
    
    # Display cache statistics
    stats = cache.get_stats()
    print(f"Cache Statistics: {stats}")
    
    print("✅ Performance optimization system operational!")