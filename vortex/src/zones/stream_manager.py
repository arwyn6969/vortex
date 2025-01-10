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

# Map Sefirot to pond names
SEFIROT_TO_POND = {
    "keter": "Pond of Crown",      # The highest sphere
    "chokhmah": "Pond of Wisdom",  # Divine wisdom
    "binah": "Pond of Understanding", # Divine understanding
    "chesed": "Pond of Kindness",  # Divine mercy
    "gevurah": "Pond of Severity", # Divine judgment
    "tiferet": "Pond of Expression", # Divine beauty
    "netzach": "Pond of Victory",  # Divine endurance
    "hod": "Pond of Glory",        # Divine splendor
    "yesod": "Pond of Harmony",    # Divine foundation
    "malkhut": "Pond of Kingdom"   # Physical manifestation
}

# Define the three pillars of the Tree of Life
PILLARS = {
    "mercy": ["chokhmah", "chesed", "netzach"],     # Right pillar
    "severity": ["binah", "gevurah", "hod"],        # Left pillar
    "balance": ["keter", "tiferet", "yesod", "malkhut"]  # Middle pillar
}

# Path attributes (Hebrew letters and meanings)
PATH_ATTRIBUTES = {
    "aleph": {"element": "air", "planet": None, "meaning": "spiritual initiation"},
    "beth": {"element": "mercury", "planet": "mercury", "meaning": "duality and choice"},
    "gimel": {"element": "moon", "planet": "moon", "meaning": "unification"},
    "daleth": {"element": "venus", "planet": "venus", "meaning": "creativity"},
    "he": {"element": "aries", "planet": None, "meaning": "revelation"},
    "vav": {"element": "taurus", "planet": None, "meaning": "connection"},
    "zayin": {"element": "gemini", "planet": None, "meaning": "discrimination"},
    "cheth": {"element": "cancer", "planet": None, "meaning": "influence"},
    "teth": {"element": "leo", "planet": None, "meaning": "serpent power"},
    "yod": {"element": "virgo", "planet": None, "meaning": "manifestation"},
    "kaph": {"element": "jupiter", "planet": "jupiter", "meaning": "wheel of fortune"},
    "lamed": {"element": "libra", "planet": None, "meaning": "balance"},
    "mem": {"element": "water", "planet": None, "meaning": "transformation"},
    "nun": {"element": "scorpio", "planet": None, "meaning": "death and rebirth"},
    "samekh": {"element": "sagittarius", "planet": None, "meaning": "support"},
    "ayin": {"element": "capricorn", "planet": None, "meaning": "divine vision"},
    "peh": {"element": "mars", "planet": "mars", "meaning": "power"},
    "tzaddi": {"element": "aquarius", "planet": None, "meaning": "meditation"},
    "qoph": {"element": "pisces", "planet": None, "meaning": "sleep and dreams"},
    "resh": {"element": "sun", "planet": "sun", "meaning": "illumination"},
    "shin": {"element": "fire", "planet": None, "meaning": "spirit"},
    "tav": {"element": "saturn", "planet": "saturn", "meaning": "completion"}
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
        # Clear existing connections
        self._stream_connections = {}
        
        # Add connections based on the three pillars
        for pillar_paths in PILLARS.values():
            for i in range(len(pillar_paths) - 1):
                from_sefirah = pillar_paths[i]
                to_sefirah = pillar_paths[i + 1]
                
                from_pond = SEFIROT_TO_POND[from_sefirah]
                to_pond = SEFIROT_TO_POND[to_sefirah]
                
                # Add bidirectional connections
                if from_pond not in self._stream_connections:
                    self._stream_connections[from_pond] = set()
                if to_pond not in self._stream_connections:
                    self._stream_connections[to_pond] = set()
                    
                self._stream_connections[from_pond].add(to_pond)
                self._stream_connections[to_pond].add(from_pond)
        
        # Add cross-pillar connections from PATHS
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
    
    def get_path_attributes(self, from_pond: str, to_pond: str) -> Optional[Dict]:
        """Get the attributes of the path between two ponds."""
        # Convert pond names back to Sefirot names
        pond_to_sefirot = {v: k for k, v in SEFIROT_TO_POND.items()}
        from_sefirah = pond_to_sefirot.get(from_pond)
        to_sefirah = pond_to_sefirot.get(to_pond)
        
        if not from_sefirah or not to_sefirah:
            return None
        
        # Find the path in PATHS
        for path in PATHS.values():
            if (path["from"] == from_sefirah and path["to"] == to_sefirah) or \
               (path["from"] == to_sefirah and path["to"] == from_sefirah):
                letter = path["letter"]
                return {
                    "letter": letter,
                    "name": path["name"],
                    **PATH_ATTRIBUTES[letter]
                }
        
        return None
    
    def get_pillar(self, pond_name: str) -> Optional[str]:
        """Get the pillar that a pond belongs to."""
        pond_to_sefirot = {v: k for k, v in SEFIROT_TO_POND.items()}
        sefirah = pond_to_sefirot.get(pond_name)
        
        if not sefirah:
            return None
        
        for pillar_name, sefirot in PILLARS.items():
            if sefirah in sefirot:
                return pillar_name
        
        return None 
    
    def get_stream_visualization(
        self,
        from_pond: str,
        to_pond: str,
        energy_level: Optional[float] = None
    ) -> Dict:
        """Get visualization data for a stream between ponds.
        
        Args:
            from_pond: Source pond name
            to_pond: Destination pond name
            energy_level: Optional current energy level (0.0 to 1.0)
            
        Returns:
            Dict containing visualization parameters
        """
        if not self.are_connected(from_pond, to_pond):
            return {}
            
        # Get path attributes
        path_attrs = self.get_path_attributes(from_pond, to_pond)
        if not path_attrs:
            return {}
            
        # Get energy level if not provided
        if energy_level is None:
            energy_level = self.get_energy_flow(from_pond, to_pond)
            
        # Base color based on path element
        element_colors = {
            "fire": "#FF4400",
            "water": "#0088FF",
            "air": "#FFFFFF",
            "earth": "#884400",
            "mercury": "#88FFFF",
            "venus": "#FF88FF",
            "mars": "#FF0000",
            "jupiter": "#FF88AA",
            "saturn": "#000088",
            "sun": "#FFFF00",
            "moon": "#FFFFFF"
        }
        
        # Get pillar for additional effects
        pillar = self.get_pillar(from_pond)
        pillar_effects = {
            "mercy": {
                "glow": True,
                "particles": "light",
                "flow_pattern": "spiral"
            },
            "severity": {
                "glow": False,
                "particles": "dark",
                "flow_pattern": "zigzag"
            },
            "balance": {
                "glow": True,
                "particles": "balanced",
                "flow_pattern": "wave"
            }
        }
        
        # Combine all visualization parameters
        visualization = {
            "base_color": element_colors.get(path_attrs["element"], "#FFFFFF"),
            "intensity": energy_level,
            "letter": path_attrs["letter"],
            "name": path_attrs["name"],
            "meaning": path_attrs["meaning"],
            "active": self.is_stream_active(from_pond, to_pond),
            **pillar_effects.get(pillar, {
                "glow": False,
                "particles": "neutral",
                "flow_pattern": "linear"
            })
        }
        
        # Add planetary influences if present
        if path_attrs["planet"]:
            visualization["planetary_effect"] = {
                "planet": path_attrs["planet"],
                "orbit_speed": energy_level * 2.0,
                "resonance": True if energy_level > 0.7 else False
            }
            
        # Add special effects based on energy level
        if energy_level > 0.9:
            visualization["special_effects"] = ["rainbow", "pulse", "harmonic"]
        elif energy_level > 0.7:
            visualization["special_effects"] = ["pulse", "harmonic"]
        elif energy_level > 0.5:
            visualization["special_effects"] = ["pulse"]
        else:
            visualization["special_effects"] = []
            
        return visualization
    
    def update_stream_visualization(
        self,
        from_pond: str,
        to_pond: str,
        energy_level: float
    ) -> None:
        """Update the visualization of a stream based on new energy level.
        
        Args:
            from_pond: Source pond name
            to_pond: Destination pond name
            energy_level: New energy level (0.0 to 1.0)
        """
        if not self.are_connected(from_pond, to_pond):
            return
            
        visualization = self.get_stream_visualization(
            from_pond,
            to_pond,
            energy_level
        )
        
        # Publish visualization update
        try:
            redis_service.publish(
                RedisConfig.VISUALIZATION_UPDATES,
                {
                    "type": "stream_visualization",
                    "from_pond": from_pond,
                    "to_pond": to_pond,
                    "visualization": visualization,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            logger.error(f"Failed to publish visualization update: {str(e)}")
    
    def _update_energy_flow(self, data: Dict) -> None:
        """Process energy flow updates and update visualizations."""
        from_pond = data.get("from_pond")
        to_pond = data.get("to_pond")
        energy_level = data.get("energy_level", 0.0)
        
        if not from_pond or not to_pond:
            return
            
        # Update energy flow
        flow_key = f"{from_pond}:{to_pond}"
        self.energy_flows[flow_key] = energy_level
        
        # Update visualization
        self.update_stream_visualization(from_pond, to_pond, energy_level)
        
        # Cache the update
        cache_key = f"{RedisConfig.CACHE_PREFIX}energy_flow:{flow_key}"
        try:
            redis_service.cache_set(
                cache_key,
                {
                    "energy_level": energy_level,
                    "visualization": self.get_stream_visualization(
                        from_pond,
                        to_pond,
                        energy_level
                    ),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            logger.error(f"Failed to cache energy flow update: {str(e)}") 