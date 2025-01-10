"""Redis configuration and connection settings."""

from typing import Optional
import os
from dataclasses import dataclass

@dataclass
class RedisConfig:
    """Redis connection configuration."""
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    db: int = int(os.getenv("REDIS_DB", "0"))
    password: Optional[str] = os.getenv("REDIS_PASSWORD")
    ssl: bool = os.getenv("REDIS_SSL", "false").lower() == "true"
    
    # Cache settings
    default_cache_ttl: int = int(os.getenv("REDIS_CACHE_TTL", "3600"))  # 1 hour
    max_cache_size: int = int(os.getenv("REDIS_MAX_CACHE_SIZE", "10000"))
    
    # Message queue settings
    default_queue_ttl: int = int(os.getenv("REDIS_QUEUE_TTL", "86400"))  # 24 hours
    max_queue_size: int = int(os.getenv("REDIS_MAX_QUEUE_SIZE", "100000"))
    
    # Real-time settings
    pubsub_channel_prefix: str = os.getenv("REDIS_PUBSUB_PREFIX", "vortex:")
    max_subscribers: int = int(os.getenv("REDIS_MAX_SUBSCRIBERS", "1000"))
    
    # Key prefixes
    CACHE_PREFIX: str = "vortex:cache:"
    QUEUE_PREFIX: str = "vortex:queue:"
    PUBSUB_PREFIX: str = "vortex:pubsub:"
    
    # Specific cache keys
    USER_PROFILE_CACHE: str = CACHE_PREFIX + "user_profile:{user_id}"
    ASSET_CACHE: str = CACHE_PREFIX + "asset:{asset_id}"
    MESSAGE_CACHE: str = CACHE_PREFIX + "message:{message_id}"
    POND_STATE_CACHE: str = CACHE_PREFIX + "pond:{pond_id}"
    
    # Queue names
    TASK_QUEUE: str = QUEUE_PREFIX + "tasks"
    MESSAGE_QUEUE: str = QUEUE_PREFIX + "messages"
    ANALYTICS_QUEUE: str = QUEUE_PREFIX + "analytics"
    
    # PubSub channels
    POND_UPDATES: str = PUBSUB_PREFIX + "pond_updates"
    USER_UPDATES: str = PUBSUB_PREFIX + "user_updates"
    SYSTEM_UPDATES: str = PUBSUB_PREFIX + "system_updates" 