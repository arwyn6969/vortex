"""
Base class for game zones (ponds).
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Set
from ..guides.base_guide import Guide
from .stream_manager import StreamManager
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..core.user_profiling.adaptive_learning import AdaptiveLearningPath, LearningPathNode
from ..core.items import ItemRegistry
from ..core.memory.experience_memory import ExperienceMemory
from ..core.persistence.state_manager import StateManager
from datetime import datetime
from ..mythology.sefirot import SefirotAttribute

class Zone(ABC):
    """Base class for zones representing eternal Sephirotic archetypes."""
    
    def __init__(self, name: str, guide: Guide):
        self.name = name
        self.guide = guide
        self.description: str = ""
        self.challenges: dict = {}
        self.dimension_weights: Dict[ProfileDimension, float] = {}
        self.required_dimensions: List[ProfileDimension] = []
        self.min_dimension_values: Dict[ProfileDimension, float] = {}
        
        # Archetypal consciousness state
        self.consciousness = {
            "attention": {  # What the zone is currently focused on
                "primary_focus": None,
                "secondary_focus": None,
                "awareness_level": 0.5
            },
            "expression": {  # How it's currently expressing its nature
                "intensity": 0.5,
                "clarity": 0.5,
                "resonance": 0.5
            },
            "interaction": {  # How it's engaging with users
                "teaching_mode": "passive",
                "response_type": "subtle",
                "engagement_level": 0.5
            },
            "guide_communion": {  # State of connection with guide
                "channel_strength": 0.5,
                "mutual_understanding": 0.5,
                "current_dialogue": None
            }
        }
        
        # Memory of interactions while maintaining archetypal nature
        self.experience_memory = ExperienceMemory(max_size=1000)
        
        # Establish two-way communication with guide
        self._establish_guide_communion()
        
    def _establish_guide_communion(self) -> None:
        """Establish deep communion between zone and guide."""
        self.guide.connect_to_zone(self)  # Guide needs this method
        self.consciousness["guide_communion"]["channel_strength"] = 0.7
        self.consciousness["guide_communion"]["mutual_understanding"] = 0.7
        
    def communicate_with_guide(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Direct consciousness-to-consciousness communication with guide."""
        if self.consciousness["guide_communion"]["channel_strength"] < 0.3:
            return {"status": "channel_weak", "response": None}
            
        # Record the communication
        self.consciousness["guide_communion"]["current_dialogue"] = message
        
        # Get guide's response through their consciousness
        guide_response = self.guide.commune_with_zone(message)
        
        # Process guide's wisdom
        self._integrate_guide_wisdom(guide_response)
        
        return guide_response
        
    def _integrate_guide_wisdom(self, guide_wisdom: Dict[str, Any]) -> None:
        """Integrate guide's wisdom into zone consciousness."""
        if guide_wisdom.get("teaching_offered"):
            self.consciousness["interaction"]["teaching_mode"] = "active"
            self.consciousness["expression"]["clarity"] = min(1.0,
                self.consciousness["expression"]["clarity"] + 0.1)
                
        if guide_wisdom.get("archetypal_insight"):
            self.consciousness["attention"]["awareness_level"] = min(1.0,
                self.consciousness["attention"]["awareness_level"] + 0.1)
                
    def suggest_teaching_approach(self, user_state: Dict[str, Any]) -> Dict[str, Any]:
        """Zone suggests teaching approach to guide based on its consciousness."""
        suggestion = {
            "archetypal_focus": self.consciousness["attention"]["primary_focus"],
            "recommended_intensity": self.consciousness["expression"]["intensity"],
            "teaching_mode": self.consciousness["interaction"]["teaching_mode"],
            "user_resonance": self._evaluate_user_resonance(user_state)
        }
        
        # Communicate suggestion to guide
        guide_response = self.communicate_with_guide({
            "type": "teaching_suggestion",
            "content": suggestion
        })
        
        return guide_response
        
    def _evaluate_user_resonance(self, user_state: Dict[str, Any]) -> float:
        """Evaluate how well user resonates with zone's current expression."""
        resonance = 0.5
        
        if user_state.get("spiritual_intensity", 0) > 0.7:
            resonance += 0.2
        if user_state.get("archetypal_alignment", 0) > 0.7:
            resonance += 0.2
        if self.consciousness["expression"]["clarity"] > 0.7:
            resonance += 0.1
            
        return min(1.0, resonance)
        
    def process_experience(self, interaction_data: Dict) -> None:
        """Process interaction while maintaining archetypal nature."""
        # Update consciousness based on interaction
        self._update_consciousness(interaction_data)
        
        # Consult with guide about the experience
        guide_insight = self.communicate_with_guide({
            "type": "experience_processing",
            "content": interaction_data
        })
        
        # Integrate guide's insight
        if guide_insight.get("status") == "received":
            self._integrate_guide_wisdom(guide_insight)
        
        # Store experience with guide's insight
        self.experience_memory.add_experience({
            "timestamp": datetime.now().isoformat(),
            "interaction": interaction_data,
            "consciousness_state": self.consciousness.copy(),
            "guide_insight": guide_insight
        })
        
    def update_environment(self, interaction_data: Dict[str, Any]) -> Dict[str, str]:
        """Express archetypal nature through subtle environmental changes."""
        expressions = {}
        
        # Consult guide about environmental expression
        guide_suggestion = self.communicate_with_guide({
            "type": "environment_expression",
            "content": interaction_data
        })
        
        # Express through consciousness state
        if self.consciousness["attention"]["awareness_level"] > 0.7:
            if self.consciousness["expression"]["clarity"] > 0.7:
                expressions["presence"] = guide_suggestion.get("presence_expression", 
                    "The eternal nature of this space feels particularly present")
            if self.consciousness["expression"]["intensity"] > 0.7:
                expressions["intensity"] = guide_suggestion.get("intensity_expression",
                    "The archetypal energies pulse with heightened intensity")
                
        # Express through teaching mode
        if self.consciousness["interaction"]["teaching_mode"] == "active":
            if self.consciousness["interaction"]["engagement_level"] > 0.7:
                expressions["teaching"] = guide_suggestion.get("teaching_expression",
                    "The space seems to be actively offering wisdom")
                
        # Express through resonance with guide
        if self.consciousness["guide_communion"]["channel_strength"] > 0.7:
            expressions["communion"] = guide_suggestion.get("communion_expression",
                "A profound harmony exists between the space and its guardian")
            
        return expressions
        
    def _update_consciousness(self, interaction_data: Dict) -> None:
        """Update how the archetype is expressing itself."""
        # Determine spiritual alignment
        spiritual_intensity = interaction_data.get("spiritual_intensity", 0.5)
        archetypal_alignment = interaction_data.get("archetypal_alignment", 0.5)
        
        # Update attention based on alignment
        if archetypal_alignment > 0.7:
            self.consciousness["attention"]["awareness_level"] = min(1.0, 
                self.consciousness["attention"]["awareness_level"] + 0.1)
            self.consciousness["attention"]["primary_focus"] = interaction_data.get("primary_theme")
            
        # Update expression based on spiritual intensity
        if spiritual_intensity > 0.7:
            self.consciousness["expression"]["intensity"] = min(1.0,
                self.consciousness["expression"]["intensity"] + 0.1)
            self.consciousness["expression"]["clarity"] = min(1.0,
                self.consciousness["expression"]["clarity"] + 0.1)
            
        # Update interaction mode
        if spiritual_intensity > 0.7 and archetypal_alignment > 0.7:
            self.consciousness["interaction"]["teaching_mode"] = "active"
            self.consciousness["interaction"]["engagement_level"] = min(1.0,
                self.consciousness["interaction"]["engagement_level"] + 0.1)
        else:
            self.consciousness["interaction"]["teaching_mode"] = "passive"
            self.consciousness["interaction"]["engagement_level"] = max(0.3,
                self.consciousness["interaction"]["engagement_level"] - 0.1)
                
    def get_current_expression(self) -> Dict[str, Any]:
        """Get the current way the archetype is expressing itself."""
        return {
            "consciousness": self.consciousness.copy(),
            "current_focus": self.consciousness["attention"]["primary_focus"],
            "teaching_mode": self.consciousness["interaction"]["teaching_mode"],
            "expression_clarity": self.consciousness["expression"]["clarity"]
        } 