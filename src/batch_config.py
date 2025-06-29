# src/batch_config.py
"""
ClaimGuard - Batch Processing Configuration
Optimized settings for different dataset sizes and performance requirements
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BatchConfig:
    """Configuration for batch processing optimization"""
    batch_size: int
    cache_size: int
    cache_ttl_hours: int
    max_concurrent_requests: int
    progress_update_interval: int
    performance_monitoring: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'batch_size': self.batch_size,
            'cache_size': self.cache_size,
            'cache_ttl_hours': self.cache_ttl_hours,
            'max_concurrent_requests': self.max_concurrent_requests,
            'progress_update_interval': self.progress_update_interval,
            'performance_monitoring': self.performance_monitoring
        }

class BatchConfigManager:
    """Manages batch processing configurations for different scenarios"""
    
    # Predefined configurations for different use cases
    CONFIGS = {
        'demo': BatchConfig(
            batch_size=5,
            cache_size=50,
            cache_ttl_hours=2,
            max_concurrent_requests=3,
            progress_update_interval=1,
            performance_monitoring=True
        ),
        
        'small': BatchConfig(
            batch_size=10,
            cache_size=100,
            cache_ttl_hours=6,
            max_concurrent_requests=5,
            progress_update_interval=2,
            performance_monitoring=True
        ),
        
        'medium': BatchConfig(
            batch_size=20,
            cache_size=200,
            cache_ttl_hours=12,
            max_concurrent_requests=8,
            progress_update_interval=5,
            performance_monitoring=True
        ),
        
        'large': BatchConfig(
            batch_size=50,
            cache_size=500,
            cache_ttl_hours=24,
            max_concurrent_requests=10,
            progress_update_interval=10,
            performance_monitoring=True
        ),
        
        'enterprise': BatchConfig(
            batch_size=100,
            cache_size=1000,
            cache_ttl_hours=48,
            max_concurrent_requests=15,
            progress_update_interval=20,
            performance_monitoring=True
        )
    }
    
    @classmethod
    def get_config(cls, config_name: str) -> BatchConfig:
        """Get configuration by name"""
        return cls.CONFIGS.get(config_name, cls.CONFIGS['demo'])
    
    @classmethod
    def get_optimal_config(cls, dataset_size: int) -> BatchConfig:
        """Get optimal configuration based on dataset size"""
        if dataset_size <= 25:
            return cls.CONFIGS['demo']
        elif dataset_size <= 100:
            return cls.CONFIGS['small']
        elif dataset_size <= 500:
            return cls.CONFIGS['medium']
        elif dataset_size <= 2000:
            return cls.CONFIGS['large']
        else:
            return cls.CONFIGS['enterprise']
    
    @classmethod
    def get_config_recommendations(cls, dataset_size: int) -> Dict[str, Any]:
        """Get configuration recommendations with explanations"""
        optimal_config = cls.get_optimal_config(dataset_size)
        
        recommendations = {
            'recommended_config': optimal_config.to_dict(),
            'reasoning': cls._get_config_reasoning(dataset_size),
            'performance_expectations': cls._get_performance_expectations(dataset_size),
            'alternative_configs': cls._get_alternative_configs(dataset_size)
        }
        
        return recommendations
    
    @classmethod
    def _get_config_reasoning(cls, dataset_size: int) -> str:
        """Get reasoning for configuration choice"""
        if dataset_size <= 25:
            return "Demo configuration optimized for interactive demonstrations with real-time feedback and maximum responsiveness."
        elif dataset_size <= 100:
            return "Small batch configuration balances performance with resource usage for typical validation scenarios."
        elif dataset_size <= 500:
            return "Medium batch configuration optimized for regular production workloads with good cache efficiency."
        elif dataset_size <= 2000:
            return "Large batch configuration designed for high-volume processing with maximum cache utilization."
        else:
            return "Enterprise configuration for maximum throughput with extensive caching and parallel processing."
    
    @classmethod
    def _get_performance_expectations(cls, dataset_size: int) -> Dict[str, str]:
        """Get performance expectations for dataset size"""
        if dataset_size <= 25:
            return {
                'processing_time': '30-60 seconds',
                'cache_efficiency': '40-60%',
                'throughput': '5-10 claims/second',
                'memory_usage': 'Low'
            }
        elif dataset_size <= 100:
            return {
                'processing_time': '2-4 minutes',
                'cache_efficiency': '50-70%',
                'throughput': '8-15 claims/second',
                'memory_usage': 'Low-Medium'
            }
        elif dataset_size <= 500:
            return {
                'processing_time': '8-15 minutes',
                'cache_efficiency': '60-80%',
                'throughput': '12-20 claims/second',
                'memory_usage': 'Medium'
            }
        elif dataset_size <= 2000:
            return {
                'processing_time': '25-45 minutes',
                'cache_efficiency': '70-85%',
                'throughput': '15-25 claims/second',
                'memory_usage': 'Medium-High'
            }
        else:
            return {
                'processing_time': '1-3 hours',
                'cache_efficiency': '80-90%',
                'throughput': '20-30 claims/second',
                'memory_usage': 'High'
            }
    
    @classmethod
    def _get_alternative_configs(cls, dataset_size: int) -> Dict[str, str]:
        """Get alternative configuration suggestions"""
        alternatives = {}
        
        if dataset_size <= 25:
            alternatives['speed_optimized'] = "Use 'small' config for faster processing if memory allows"
        elif dataset_size <= 100:
            alternatives['memory_optimized'] = "Use 'demo' config if memory is limited"
            alternatives['speed_optimized'] = "Use 'medium' config for faster processing"
        elif dataset_size <= 500:
            alternatives['memory_optimized'] = "Use 'small' config if memory is limited"
            alternatives['speed_optimized'] = "Use 'large' config for maximum speed"
        elif dataset_size <= 2000:
            alternatives['memory_optimized'] = "Use 'medium' config if memory is limited"
            alternatives['speed_optimized'] = "Use 'enterprise' config for maximum throughput"
        else:
            alternatives['memory_optimized'] = "Use 'large' config if memory is limited"
            alternatives['custom'] = "Consider custom configuration for very large datasets"
        
        return alternatives

# Performance optimization utilities
class PerformanceOptimizer:
    """Utilities for runtime performance optimization"""
    
    @staticmethod
    def estimate_processing_time(dataset_size: int, config: BatchConfig, cache_hit_rate: float = 0.0) -> float:
        """Estimate processing time based on configuration and cache efficiency"""
        
        # Base processing time per claim (seconds)
        base_time_per_claim = 0.5  # With AI call
        cached_time_per_claim = 0.05  # From cache
        
        # Calculate effective processing time
        ai_calls_needed = dataset_size * (1 - cache_hit_rate)
        cached_calls = dataset_size * cache_hit_rate
        
        total_time = (ai_calls_needed * base_time_per_claim) + (cached_calls * cached_time_per_claim)
        
        # Apply batch efficiency factor
        batch_efficiency = min(1.0, config.batch_size / 10)  # Larger batches are more efficient
        total_time *= (1 - batch_efficiency * 0.1)  # Up to 10% improvement
        
        return total_time
    
    @staticmethod
    def estimate_memory_usage(dataset_size: int, config: BatchConfig) -> Dict[str, float]:
        """Estimate memory usage for processing"""
        
        # Memory per cached result (KB)
        memory_per_cache_entry = 2.0  # Approximate
        
        # Memory for dataset
        memory_per_claim = 0.5  # KB
        
        estimated_usage = {
            'cache_memory_kb': config.cache_size * memory_per_cache_entry,
            'dataset_memory_kb': dataset_size * memory_per_claim,
            'processing_memory_kb': config.batch_size * memory_per_claim * 2,  # Working memory
        }
        
        estimated_usage['total_memory_mb'] = sum(estimated_usage.values()) / 1024
        
        return estimated_usage
    
    @staticmethod
    def get_optimization_recommendations(current_performance: Dict[str, Any]) -> Dict[str, str]:
        """Get optimization recommendations based on current performance"""
        recommendations = {}
        
        hit_rate = current_performance.get('cache_hit_rate', 0)
        processing_speed = current_performance.get('processing_speed', 0)
        memory_usage = current_performance.get('memory_usage_percent', 0)
        
        # Cache hit rate recommendations
        if hit_rate < 30:
            recommendations['cache'] = "Consider processing similar claim types together to improve cache efficiency"
        elif hit_rate > 90:
            recommendations['cache'] = "Excellent cache performance! Consider reducing cache size to save memory"
        
        # Processing speed recommendations
        if processing_speed < 5:
            recommendations['speed'] = "Consider increasing batch size or reducing AI analysis depth"
        elif processing_speed > 25:
            recommendations['speed'] = "Excellent processing speed! System is well-optimized"
        
        # Memory usage recommendations
        if memory_usage > 80:
            recommendations['memory'] = "High memory usage detected. Consider reducing cache size or batch size"
        elif memory_usage < 20:
            recommendations['memory'] = "Low memory usage. Consider increasing cache size for better performance"
        
        return recommendations

# Export configuration functions for easy import
def get_demo_config() -> BatchConfig:
    """Get demo configuration for presentations"""
    return BatchConfigManager.get_config('demo')

def get_production_config(dataset_size: int) -> BatchConfig:
    """Get production configuration based on dataset size"""
    return BatchConfigManager.get_optimal_config(dataset_size)

def estimate_performance(dataset_size: int, config_name: str = 'auto') -> Dict[str, Any]:
    """Estimate performance for given dataset size and configuration"""
    if config_name == 'auto':
        config = BatchConfigManager.get_optimal_config(dataset_size)
    else:
        config = BatchConfigManager.get_config(config_name)
    
    return {
        'config': config.to_dict(),
        'estimated_time': PerformanceOptimizer.estimate_processing_time(dataset_size, config),
        'estimated_memory': PerformanceOptimizer.estimate_memory_usage(dataset_size, config),
        'recommendations': BatchConfigManager.get_config_recommendations(dataset_size)
    }

if __name__ == "__main__":
    # Test the configuration system
    print("🔧 Testing ClaimGuard Batch Configuration System...")
    
    test_sizes = [25, 100, 500, 1000, 5000]
    
    for size in test_sizes:
        print(f"\n📊 Dataset Size: {size} claims")
        config = BatchConfigManager.get_optimal_config(size)
        print(f"   Recommended Config: batch_size={config.batch_size}, cache_size={config.cache_size}")
        
        estimated_time = PerformanceOptimizer.estimate_processing_time(size, config, 0.6)
        print(f"   Estimated Processing Time: {estimated_time:.1f} seconds")
        
        memory = PerformanceOptimizer.estimate_memory_usage(size, config)
        print(f"   Estimated Memory Usage: {memory['total_memory_mb']:.1f} MB")
    
    print("\n✅ Batch configuration system operational!")