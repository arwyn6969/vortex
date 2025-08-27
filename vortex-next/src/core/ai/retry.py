"""Retry utilities for MCP transport layer."""

import asyncio
import logging
from typing import TypeVar, Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')

class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 10.0,
        backoff_factor: float = 2.0,
        retry_exceptions: tuple = (Exception,)
    ):
        """Initialize retry configuration.
        
        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
            backoff_factor: Multiplicative factor for backoff
            retry_exceptions: Tuple of exceptions to retry on
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.retry_exceptions = retry_exceptions

def with_retry(config: Optional[RetryConfig] = None):
    """Decorator for adding retry behavior to async functions.
    
    Args:
        config: Optional retry configuration
    """
    if config is None:
        config = RetryConfig()
        
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            delay = config.initial_delay
            
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except config.retry_exceptions as e:
                    last_exception = e
                    
                    if attempt == config.max_retries:
                        logger.error(
                            f"Failed after {config.max_retries} retries: {str(e)}"
                        )
                        raise
                        
                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.1f}s: {str(e)}"
                    )
                    
                    await asyncio.sleep(delay)
                    delay = min(delay * config.backoff_factor, config.max_delay)
                    
            raise last_exception  # Should never reach here
            
        return wrapper
    return decorator 