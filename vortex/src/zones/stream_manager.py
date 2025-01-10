"""
Manages the sacred streams connecting the ponds.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from ..mythology.sefirot import PATHS, get_connected_paths, get_direct_connections
from ..redis_config import RedisConfig
from .. import redis_service
import json

# Configure logging
logger = logging.getLogger(__name__)

# Map Sefirot to new pond names
SEFIROT_TO_POND = {
    "keter": "Vibe Temple",      # Crown -> Ultimate harmony and vibe
    "chokhmah": "Brain Galaxy",  # Wisdom -> Big brain energy
    "binah": "Zen Zone",         # Understanding -> Disciplined mind
    "chesed": "Comfy Cabin",     # Mercy -> Cozy and nurturing
    "gevurah": "Gains Grotto",   # Severity -> Mental strength
    "tiferet": "Meme Studio",    # Beauty -> Creative expression
}

class StreamManager:
    """Manages connections between ponds and their energy flows."""
    
    def __init__(self):
        self.active_streams = {}
        self.energy_flows = {}
        self._stream_connections = {}
        
        # Initialize stream connections based on Sefirot paths
        self._initialize_stream_connections()
        
        # Subscribe to pond updates
        self._subscribe_to_updates()
    
    def _initialize_stream_connections(self) -> None:
        """Initialize all possible stream connections based on Sefirot paths."""
        for path in PATHS.values():
            from_sefirah = path["from"]
            to_sefirah = path["to"]
            
            from_pond = SEFIROT_TO_POND[from_sefirah]
            to_pond = SEFIROT_TO_POND[to_sefirah]
            
            # Add bidirectional connections
            if from_pond not in self._stream_connections:
                self._stream_connections[from_pond] = set()
            if to_pond not in self._stream_connections:
                self._stream_connections[to_pond] = set()
                
            self._stream_connections[from_pond].add(to_pond)
            self._stream_connections[to_pond].add(from_pond)
            
        logger.info(f"Initialized stream connections between {len(self._stream_connections)} ponds")
    
    def are_connected(self, pond1: str, pond2: str) -> bool:
        """Check if two ponds are directly connected.
        
        Args:
            pond1: Name of the first pond
            pond2: Name of the second pond
            
        Returns:
            bool: True if the ponds are directly connected, False otherwise
        """
        if pond1 not in self._stream_connections:
            return False
        return pond2 in self._stream_connections[pond1]
    
    def _subscribe_to_updates(self) -> None:
        """Subscribe to pond update channels with error handling."""
        try:
            redis_service.subscribe(RedisConfig.POND_UPDATES)
            logger.info("Successfully subscribed to pond updates channel")
        except Exception as e:
            logger.error(f"Failed to subscribe to pond updates: {str(e)}")
            raise RuntimeError("Failed to initialize stream manager: Redis subscription failed") from e
    
    def _validate_message_data(self, data: Any) -> Optional[Dict]:
        """Validate and parse message data.
        
        Args:
            data: Raw message data to validate
            
        Returns:
            Optional[Dict]: Validated message data or None if invalid
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse message data as JSON: {str(e)}")
                return None
                
        if not isinstance(data, dict):
            logger.warning(f"Message data is not a dictionary: {type(data)}")
            return None
            
        if "type" not in data:
            logger.warning("Message data missing required 'type' field")
            return None
            
        return data
    
    def _process_updates(self) -> None:
        """Process any pending pond updates with improved error handling."""
        try:
            message = redis_service.get_message(timeout=0.1)
            if not message:
                return
                
            if message.get("type") != "message":
                return
                
            data = self._validate_message_data(message.get("data"))
            if not data:
                return
                
            message_type = data.get("type")
            if message_type == "energy_flow":
                try:
                    self._update_energy_flow(data)
                except Exception as e:
                    logger.error(f"Failed to process energy flow update: {str(e)}")
            elif message_type == "stream_state":
                try:
                    self._update_stream_state(data)
                except Exception as e:
                    logger.error(f"Failed to process stream state update: {str(e)}")
            else:
                logger.warning(f"Unknown message type received: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing pond updates: {str(e)}")
    
    def get_connected_ponds(self, pond_name: str) -> List[str]:
        """Get all ponds connected to the given pond."""
        return list(self._stream_connections.get(pond_name, set()))
    
    def update_energy_flow(
        self,
        from_pond: str,
        to_pond: str,
        energy_level: float
    ) -> None:
        """Update energy flow between ponds with enhanced error handling."""
        try:
            if not self.are_connected(from_pond, to_pond):
                logger.warning(f"Attempted to update energy flow between unconnected ponds: {from_pond} -> {to_pond}")
                return
                
            flow_key = f"{from_pond}:{to_pond}"
            self.energy_flows[flow_key] = energy_level
            
            # Prepare update data
            update_data = {
                "from_pond": from_pond,
                "to_pond": to_pond,
                "energy_level": energy_level,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Cache the energy flow
            cache_key = f"{RedisConfig.CACHE_PREFIX}energy_flow:{flow_key}"
            try:
                redis_service.cache_set(cache_key, update_data)
            except Exception as e:
                logger.error(f"Failed to cache energy flow update: {str(e)}")
                # Continue execution to attempt publish
            
            # Publish update
            try:
                redis_service.publish(
                    RedisConfig.POND_UPDATES,
                    {
                        "type": "energy_flow",
                        **update_data
                    }
                )
            except Exception as e:
                logger.error(f"Failed to publish energy flow update: {str(e)}")
                # Consider the update partially successful since local state was updated
                
            logger.debug(f"Updated energy flow {from_pond} -> {to_pond}: {energy_level}")
            
        except Exception as e:
            logger.error(f"Critical error in update_energy_flow: {str(e)}")
            raise RuntimeError(f"Failed to update energy flow between {from_pond} and {to_pond}") from e
    
    def get_energy_flow(self, from_pond: str, to_pond: str) -> float:
        """Get current energy flow between ponds."""
        flow_key = f"{from_pond}:{to_pond}"
        
        # Try cache first
        cache_key = f"{RedisConfig.CACHE_PREFIX}energy_flow:{flow_key}"
        cached_flow = redis_service.cache_get(cache_key)
        
        if cached_flow:
            return cached_flow["energy_level"]
        
        # Fall back to memory
        return self.energy_flows.get(flow_key, 0.0)
    
    def activate_stream(self, from_pond: str, to_pond: str) -> bool:
        """Activate a stream between ponds."""
        if not self.are_connected(from_pond, to_pond):
            return False
            
        stream_key = f"{from_pond}:{to_pond}"
        self.active_streams[stream_key] = True
        
        # Cache stream state
        cache_key = f"{RedisConfig.CACHE_PREFIX}stream_state:{stream_key}"
        redis_service.cache_set(
            cache_key,
            {
                "from_pond": from_pond,
                "to_pond": to_pond,
                "active": True,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Publish update
        redis_service.publish(
            RedisConfig.POND_UPDATES,
            {
                "type": "stream_state",
                "from_pond": from_pond,
                "to_pond": to_pond,
                "active": True,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return True
    
    def deactivate_stream(self, from_pond: str, to_pond: str) -> bool:
        """Deactivate a stream between ponds."""
        stream_key = f"{from_pond}:{to_pond}"
        if stream_key not in self.active_streams:
            return False
            
        del self.active_streams[stream_key]
        
        # Update cache
        cache_key = f"{RedisConfig.CACHE_PREFIX}stream_state:{stream_key}"
        redis_service.cache_set(
            cache_key,
            {
                "from_pond": from_pond,
                "to_pond": to_pond,
                "active": False,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Publish update
        redis_service.publish(
            RedisConfig.POND_UPDATES,
            {
                "type": "stream_state",
                "from_pond": from_pond,
                "to_pond": to_pond,
                "active": False,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return True
    
    def is_stream_active(self, from_pond: str, to_pond: str) -> bool:
        """Check if a stream is active."""
        stream_key = f"{from_pond}:{to_pond}"
        
        # Try cache first
        cache_key = f"{RedisConfig.CACHE_PREFIX}stream_state:{stream_key}"
        cached_state = redis_service.cache_get(cache_key)
        
        if cached_state is not None:
            return cached_state["active"]
        
        # Fall back to memory
        return stream_key in self.active_streams 