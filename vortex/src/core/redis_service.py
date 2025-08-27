"""Redis service for caching, message queuing, and real-time updates."""

import json
import logging
from typing import Any, Dict, List, Optional, Set, Union
from datetime import datetime
import redis
from redis.client import PubSub
from .redis_config import RedisConfig

logger = logging.getLogger(__name__)

class RedisService:
    """Handles Redis operations for caching, queuing, and real-time updates."""
    
    def __init__(self, config: Optional[RedisConfig] = None):
        """Initialize Redis service with optional configuration."""
        self.config = config or RedisConfig()
        self.redis = redis.Redis(
            host=self.config.host,
            port=self.config.port,
            db=self.config.db,
            password=self.config.password,
            ssl=self.config.ssl,
            decode_responses=True
        )
        self._pubsub: Optional[PubSub] = None
    
    # Cache operations
    def cache_set(
        self,
        key: str,
        value: Union[str, dict, list],
        ttl: Optional[int] = None
    ) -> bool:
        """Set a value in cache with optional TTL."""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self.redis.set(
                key,
                value,
                ex=ttl or self.config.default_cache_ttl
            )
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {str(e)}")
            return False
    
    def cache_get(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """Get a value from cache."""
        try:
            value = self.redis.get(key)
            if value is None:
                return default
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {str(e)}")
            return default
    
    def cache_delete(self, key: str) -> bool:
        """Delete a value from cache."""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {str(e)}")
            return False
    
    # Queue operations
    def queue_push(
        self,
        queue_name: str,
        data: Union[str, dict, list],
        ttl: Optional[int] = None
    ) -> bool:
        """Push data to a queue."""
        try:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            if self.redis.lpush(queue_name, data):
                if ttl or self.config.default_queue_ttl:
                    self.redis.expire(
                        queue_name,
                        ttl or self.config.default_queue_ttl
                    )
                return True
            return False
        except Exception as e:
            logger.error(f"Error pushing to queue {queue_name}: {str(e)}")
            return False
    
    def queue_pop(
        self,
        queue_name: str,
        timeout: int = 0
    ) -> Optional[Any]:
        """Pop data from a queue with optional timeout."""
        try:
            if timeout > 0:
                result = self.redis.brpop(queue_name, timeout)
                return result[1] if result else None
            else:
                result = self.redis.rpop(queue_name)
                return result
        except Exception as e:
            logger.error(f"Error popping from queue {queue_name}: {str(e)}")
            return None
    
    def queue_length(self, queue_name: str) -> int:
        """Get the length of a queue."""
        try:
            return self.redis.llen(queue_name)
        except Exception as e:
            logger.error(f"Error getting queue length for {queue_name}: {str(e)}")
            return 0
    
    # PubSub operations
    def publish(
        self,
        channel: str,
        message: Union[str, dict, list]
    ) -> int:
        """Publish a message to a channel."""
        try:
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            return self.redis.publish(channel, message)
        except Exception as e:
            logger.error(f"Error publishing to channel {channel}: {str(e)}")
            return 0
    
    def subscribe(self, *channels: str) -> PubSub:
        """Subscribe to one or more channels."""
        if not self._pubsub:
            self._pubsub = self.redis.pubsub()
        self._pubsub.subscribe(*channels)
        return self._pubsub
    
    def unsubscribe(self, *channels: str) -> None:
        """Unsubscribe from one or more channels."""
        if self._pubsub:
            self._pubsub.unsubscribe(*channels)
    
    def get_message(
        self,
        timeout: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """Get a message from subscribed channels."""
        if not self._pubsub:
            return None
        try:
            return self._pubsub.get_message(timeout=timeout)
        except Exception as e:
            logger.error(f"Error getting pubsub message: {str(e)}")
            return None
    
    # Utility methods
    def ping(self) -> bool:
        """Check Redis connection."""
        try:
            return bool(self.redis.ping())
        except Exception as e:
            logger.error(f"Redis ping failed: {str(e)}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all data (use with caution)."""
        try:
            return bool(self.redis.flushdb())
        except Exception as e:
            logger.error(f"Error clearing Redis data: {str(e)}")
            return False

# Instantiate a default RedisService instance for module-level access
_default_redis_service = RedisService()

def __getattr__(name: str):
    """Forward module-level attribute access to the default RedisService instance."""
    return getattr(_default_redis_service, name) 