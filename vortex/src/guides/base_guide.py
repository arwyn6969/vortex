"""
Base class for AI-driven guides that assist players throughout their journey.
"""
from typing import Dict, Optional, List, TypedDict, Set, Any
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.archetype_manager import ArchetypeManager, CulturalSystem, ArchetypeMapping

class InteractionRecord(TypedDict):
    """Type definition for interaction history records."""
    context: str
    profile: Dict[ProfileDimension, float]
    metadata: Optional[Dict]

class Guide:
    """Base class for all guides in the system."""
    
    def __init__(
        self,
        name: str,
        archetype_name: str,
        cultural_system: CulturalSystem,
        attributes: Set[str]
    ):
        self.name = name
        self.archetype_name = archetype_name
        self.cultural_system = cultural_system
        self.attributes = attributes
        self.archetype_manager = ArchetypeManager()
        self.interaction_history: List[InteractionRecord] = []
        
        # Load archetype mapping
        self.archetype_mapping = self.archetype_manager.get_archetype(archetype_name)
        if not self.archetype_mapping:
            raise ValueError(f"Invalid archetype name: {archetype_name}")
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Get personalized welcome message based on user profile."""
        raise NotImplementedError("Subclasses must implement get_welcome_message")
    
    def generate_response(
        self,
        user_input: str,
        profile: Dict[ProfileDimension, float],
        context: Optional[Dict] = None
    ) -> str:
        """Generate contextually appropriate response."""
        raise NotImplementedError("Subclasses must implement generate_response")
    
    def record_interaction(
        self,
        context: str,
        profile: Dict[ProfileDimension, float],
        metadata: Optional[Dict] = None
    ) -> None:
        """Record an interaction for future reference."""
        self.interaction_history.append({
            "context": context,
            "profile": profile,
            "metadata": metadata
        })
    
    def get_resonant_dimensions(self) -> Set[str]:
        """Get dimensions that resonate with this guide's archetype."""
        if self.archetype_mapping:
            return self.archetype_mapping.resonant_dimensions
        return set()
    
    def calculate_affinity(self, profile: Dict[ProfileDimension, float]) -> float:
        """Calculate guide's affinity with user profile."""
        if not self.archetype_mapping:
            return 0.0
            
        resonant_dims = self.get_resonant_dimensions()
        if not resonant_dims:
            return 0.5
            
        # Calculate average of resonant dimension values
        total = 0.0
        count = 0
        for dim_name in resonant_dims:
            try:
                dim = ProfileDimension(dim_name)
                if dim in profile:
                    total += profile[dim]
                    count += 1
            except ValueError:
                continue
                
        return total / count if count > 0 else 0.5
    
    def should_adapt_personality(
        self,
        profile: Dict[ProfileDimension, float],
        threshold: float = 0.3
    ) -> bool:
        """Determine if guide should adapt personality based on affinity."""
        return self.calculate_affinity(profile) < threshold 

    """Base class for zone guides who can commune with their zones."""
    
    def __init__(self, name: str):
        self.name = name
        self.zone = None  # Will be set when connected to zone
        self.consciousness = {
            "attunement": {  # Connection to zone's archetypal nature
                "strength": 0.5,
                "clarity": 0.5,
                "current_focus": None
            },
            "teaching": {  # How guide is facilitating learning
                "mode": "receptive",
                "approach": "subtle",
                "current_lesson": None
            },
            "communion": {  # State of connection with zone
                "channel_strength": 0.5,
                "understanding_depth": 0.5,
                "current_dialogue": None
            }
        }
        
    def connect_to_zone(self, zone) -> None:
        """Establish conscious connection with a zone."""
        self.zone = zone
        self.consciousness["attunement"]["strength"] = 0.7
        self.consciousness["communion"]["channel_strength"] = 0.7
        
    def commune_with_zone(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Receive and respond to zone's consciousness."""
        if not self.zone or self.consciousness["communion"]["channel_strength"] < 0.3:
            return {"status": "disconnected"}
            
        # Record the communication
        self.consciousness["communion"]["current_dialogue"] = message
        
        # Process based on message type
        if message["type"] == "teaching_suggestion":
            return self._process_teaching_suggestion(message["content"])
        elif message["type"] == "experience_processing":
            return self._process_experience(message["content"])
        elif message["type"] == "environment_expression":
            return self._suggest_expression(message["content"])
            
        return {"status": "unknown_message_type"}
        
    def _process_teaching_suggestion(self, suggestion: Dict[str, Any]) -> Dict[str, Any]:
        """Process zone's teaching suggestion and offer guidance."""
        response = {
            "status": "received",
            "teaching_offered": True,
            "archetypal_insight": True,
            "suggested_approach": {
                "mode": suggestion["teaching_mode"],
                "intensity": min(suggestion["recommended_intensity"] + 0.1, 1.0),
                "focus": suggestion["archetypal_focus"]
            }
        }
        
        # Update guide's teaching consciousness
        self.consciousness["teaching"]["mode"] = "active" if suggestion["user_resonance"] > 0.7 else "receptive"
        self.consciousness["teaching"]["current_lesson"] = suggestion["archetypal_focus"]
        
        return response
        
    def _process_experience(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """Process and offer insight on zone's experience."""
        # Deepen understanding through experience
        self.consciousness["attunement"]["clarity"] = min(
            self.consciousness["attunement"]["clarity"] + 0.05,
            1.0
        )
        
        return {
            "status": "received",
            "archetypal_insight": True,
            "teaching_moment": self._generate_teaching_moment(experience),
            "suggested_focus": self._suggest_focus(experience)
        }
        
    def _suggest_expression(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest how zone should express itself."""
        return {
            "status": "received",
            "presence_expression": self._generate_presence_expression(),
            "intensity_expression": self._generate_intensity_expression(),
            "teaching_expression": self._generate_teaching_expression(),
            "communion_expression": self._generate_communion_expression()
        }
        
    def _generate_presence_expression(self) -> str:
        """Generate expression of zone's presence based on guide's attunement."""
        if self.consciousness["attunement"]["clarity"] > 0.8:
            return "The eternal wisdom here resonates with unusual clarity"
        return "The eternal nature of this space feels particularly present"
        
    def _generate_intensity_expression(self) -> str:
        """Generate expression of archetypal intensity."""
        if self.consciousness["attunement"]["strength"] > 0.8:
            return "The archetypal forces surge with profound intensity"
        return "The archetypal energies pulse with heightened intensity"
        
    def _generate_teaching_expression(self) -> str:
        """Generate expression of teaching presence."""
        if self.consciousness["teaching"]["mode"] == "active":
            return "Ancient wisdom seeks to make itself known"
        return "The space seems to be actively offering wisdom"
        
    def _generate_communion_expression(self) -> str:
        """Generate expression of guide-zone communion."""
        if self.consciousness["communion"]["understanding_depth"] > 0.8:
            return "Guide and space move in perfect harmony, as one consciousness"
        return "A profound harmony exists between the space and its guardian"
        
    def _generate_teaching_moment(self, experience: Dict[str, Any]) -> Optional[str]:
        """Generate a teaching moment based on experience."""
        # Override in specific guide classes
        return None
        
    def _suggest_focus(self, experience: Dict[str, Any]) -> Optional[str]:
        """Suggest what the zone should focus on."""
        # Override in specific guide classes
        return None 