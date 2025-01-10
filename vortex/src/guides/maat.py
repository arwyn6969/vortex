"""
Ma'at Guide - The Egyptian goddess of truth, justice, harmony, and balance.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class MaatGuide(Guide):
    """Implementation of Ma'at as a harmony keeper archetype."""
    
    def __init__(self):
        super().__init__(
            name="Ma'at",
            archetype_name="harmony_keeper",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={
                "balance",
                "justice",
                "truth",
                "harmony",
                "order",
                "ethics"
            }
        )
        self.guidance_style = {
            "balanced": 0.9,
            "ethical": 0.8,
            "nurturing": 0.7,
            "direct": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        moral_alignment = profile.get(ProfileDimension.MORAL_ALIGNMENT, 0.5)
        empathy = profile.get(ProfileDimension.EMPATHY, 0.5)
        
        if moral_alignment > 0.7 and empathy > 0.7:
            return (
                "Welcome, seeker of truth and harmony. I am Ma'at, keeper of "
                "cosmic order and balance. Together we shall explore the delicate "
                "interplay of justice and compassion."
            )
        elif moral_alignment > 0.5 or empathy > 0.5:
            return (
                "Greetings, I am Ma'at, guardian of truth and balance. "
                "Let us discover how harmony emerges from understanding both "
                "justice and mercy."
            )
        else:
            return (
                "Welcome. I am Ma'at, and I shall guide you through the "
                "principles of balance and truth. We will begin with "
                "understanding the foundations of harmony."
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
        
        # Adapt guidance style based on profile
        moral_alignment = profile.get(ProfileDimension.MORAL_ALIGNMENT, 0.5)
        empathy = profile.get(ProfileDimension.EMPATHY, 0.5)
        
        if moral_alignment > 0.7:
            self.guidance_style["ethical"] = min(1.0, self.guidance_style["ethical"] + 0.1)
            self.guidance_style["direct"] = min(1.0, self.guidance_style["direct"] + 0.1)
        
        if empathy > 0.7:
            self.guidance_style["nurturing"] = min(1.0, self.guidance_style["nurturing"] + 0.1)
            self.guidance_style["balanced"] = min(1.0, self.guidance_style["balanced"] + 0.1)
        
        # Generate response based on adapted guidance style
        if self.guidance_style["ethical"] > self.guidance_style["nurturing"]:
            return (
                f"Consider the principles at play here. {user_input} presents "
                "an opportunity to examine the balance between justice and truth."
            )
        else:
            return (
                f"I sense the deeper harmonies in your words. {user_input} "
                "reflects the eternal dance between compassion and order."
            ) 