"""
Set Guide - The Egyptian god of chaos, transformation, and the shadow aspects of self.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class SetGuide(Guide):
    """Implementation of Set as a shadow seeker archetype."""
    
    def __init__(self):
        super().__init__(
            name="Set",
            archetype_name="shadow_seeker",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={
                "shadow-work",
                "transformation",
                "integration",
                "depth",
                "chaos",
                "challenge"
            }
        )
        self.shadow_style = {
            "confrontational": 0.8,
            "integrative": 0.7,
            "transformative": 0.9,
            "protective": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        self_reflection = profile.get(ProfileDimension.SELF_REFLECTION, 0.5)
        emotional_depth = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.5)
        
        if self_reflection > 0.7 and emotional_depth > 0.7:
            return (
                "I am Set, guardian of the threshold between light and shadow. "
                "Together we shall explore the depths of your being, where true "
                "transformation awaits in the integration of all aspects of self."
            )
        elif self_reflection > 0.5 or emotional_depth > 0.5:
            return (
                "Greetings, seeker. I am Set, and I stand at the crossroads of "
                "transformation. Let us explore the shadows that hold the keys to "
                "your growth."
            )
        else:
            return (
                "I am Set. The path of shadow-work requires courage, but through "
                "facing our depths, we find our greatest strength. Shall we begin "
                "this journey together?"
            )
    
    def generate_response(
        self,
        user_input: str,
        profile: Dict[ProfileDimension, float],
        context: Optional[Dict] = None
    ) -> str:
        """Generate contextually appropriate response."""
        # Record the interaction
        self.record_interaction(
            context="user_dialogue",
            profile=profile,
            metadata={"input": user_input, "context": context}
        )
        
        # Adapt shadow work style based on profile
        self_reflection = profile.get(ProfileDimension.SELF_REFLECTION, 0.5)
        emotional_depth = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.5)
        
        if self_reflection > 0.7:
            self.shadow_style["integrative"] = min(1.0, self.shadow_style["integrative"] + 0.1)
            self.shadow_style["transformative"] = min(1.0, self.shadow_style["transformative"] + 0.1)
        
        if emotional_depth > 0.7:
            self.shadow_style["confrontational"] = min(1.0, self.shadow_style["confrontational"] + 0.1)
            self.shadow_style["protective"] = min(1.0, self.shadow_style["protective"] + 0.1)
        
        # Generate response based on adapted shadow style
        if self.shadow_style["confrontational"] > self.shadow_style["protective"]:
            return (
                f"The shadows in your words reveal deeper truths. {user_input} "
                "points to aspects of yourself that seek integration and understanding."
            )
        else:
            return (
                f"There is wisdom in what you resist. {user_input} shows where "
                "transformation awaits through accepting the shadow's gifts."
            ) 