"""Performance profiling utilities for the Vortex game engine."""

import cProfile
import pstats
import time
import logging
import functools
from typing import Any, Callable, Optional, TypeVar, cast
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

# Type variables for generic function types
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')

def profile_function(output_dir: Optional[str] = None) -> Callable[[F], F]:
    """
    Decorator for profiling function execution.
    
    Args:
        output_dir: Directory to save profiling results. If None, uses logging.
        
    Returns:
        Decorated function that includes profiling.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            profiler = cProfile.Profile()
            try:
                result = profiler.runcall(func, *args, **kwargs)
                
                stats = pstats.Stats(profiler)
                stats.sort_stats('cumulative')
                
                if output_dir:
                    # Save to file
                    output_path = Path(output_dir) / f"{func.__name__}_profile.txt"
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    stats.dump_stats(str(output_path))
                else:
                    # Log results
                    import io
                    stream = io.StringIO()
                    stats = pstats.Stats(profiler, stream=stream)
                    stats.sort_stats('cumulative').print_stats(20)
                    logger.debug(
                        f"Profile for {func.__name__}:\n{stream.getvalue()}"
                    )
                    
                return result
                
            except Exception as e:
                logger.error(
                    f"Error profiling {func.__name__}: {str(e)}"
                )
                return func(*args, **kwargs)  # Fallback to original function
                
        return cast(F, wrapper)
    return decorator

@contextmanager
def profile_block(name: str) -> None:
    """
    Context manager for profiling a block of code.
    
    Args:
        name: Name of the code block for identification
        
    Example:
        with profile_block("critical_section"):
            # Code to profile
            process_data()
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - start_time
        logger.debug(f"Block '{name}' took {duration:.4f} seconds")

class PerformanceMonitor:
    """Monitors and tracks performance metrics over time."""
    
    def __init__(self):
        self.metrics: dict[str, list[float]] = {}
        
    def record_metric(self, name: str, value: float) -> None:
        """Record a performance metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
        
    def get_average(self, name: str) -> float:
        """Get average value for a metric."""
        values = self.metrics.get(name, [])
        return sum(values) / len(values) if values else 0.0
        
    def get_summary(self) -> dict[str, dict[str, float]]:
        """Get summary statistics for all metrics."""
        summary = {}
        for name, values in self.metrics.items():
            if values:
                summary[name] = {
                    'avg': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
        return summary

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def monitor_performance(metric_name: str) -> Callable[[F], F]:
    """
    Decorator to monitor function performance.
    
    Args:
        metric_name: Name of the metric to track
        
    Returns:
        Decorated function that records performance metrics
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                performance_monitor.record_metric(metric_name, duration)
                return result
            except Exception as e:
                logger.error(
                    f"Error monitoring {func.__name__}: {str(e)}"
                )
                raise  # Re-raise the exception after logging
                
        return cast(F, wrapper)
    return decorator 