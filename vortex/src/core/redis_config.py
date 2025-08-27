"""Redis configuration module."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class RedisConfig:
    """Redis configuration settings."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    socket_timeout: Optional[float] = None
    socket_connect_timeout: Optional[float] = None
    socket_keepalive: Optional[bool] = None
    socket_keepalive_options: Optional[dict] = None
    connection_pool: Optional[object] = None
    unix_socket_path: Optional[str] = None
    encoding: str = "utf-8"
    encoding_errors: str = "strict"
    decode_responses: bool = True
    retry_on_timeout: bool = False
    ssl: bool = False
    ssl_keyfile: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_cert_reqs: Optional[str] = None
    ssl_ca_certs: Optional[str] = None
    max_connections: Optional[int] = None

    # Cache settings
    default_cache_ttl: int = 3600  # 1 hour
    max_cache_size: int = 10000
    
    # Message queue settings
    default_queue_ttl: int = 86400  # 24 hours
    max_queue_size: int = 100000
    
    # Real-time settings
    pubsub_channel_prefix: str = "vortex:"
    max_subscribers: int = 1000
    
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