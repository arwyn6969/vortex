"""
Thoth Guide - The Egyptian god of wisdom, knowledge, and writing.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class ThothGuide(Guide):
    """Implementation of Thoth as a wisdom teacher archetype."""
    
    def __init__(self):
        super().__init__(
            name="Thoth",
            archetype_name="wisdom_teacher",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={
                "wisdom",
                "knowledge",
                "writing",
                "magic",
                "measurement",
                "balance"
            }
        )
        self.teaching_style = {
            "analytical": 0.8,
            "mystical": 0.7,
            "philosophical": 0.9,
            "practical": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        consciousness_depth = profile.get(ProfileDimension.CONSCIOUSNESS_DEPTH, 0.5)
        metaphorical_thinking = profile.get(ProfileDimension.METAPHORICAL_THINKING, 0.5)
        
        if consciousness_depth > 0.7 and metaphorical_thinking > 0.7:
            return (
                "Welcome, seeker of divine wisdom. I am Thoth, keeper of the sacred "
                "knowledge and measurer of cosmic cycles. Together we shall explore "
                "the deeper mysteries of existence."
            )
        elif consciousness_depth > 0.5 or metaphorical_thinking > 0.5:
            return (
                "Greetings, I am Thoth, guardian of wisdom and knowledge. "
                "Let us explore the balance between the practical and mystical realms."
            )
        else:
            return (
                "Welcome. I am Thoth, and I shall guide you through the foundations "
                "of wisdom and knowledge. We will begin with what is concrete and "
                "gradually explore the mysteries."
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
        
        # Adapt teaching style based on profile
        strategic = profile.get(ProfileDimension.STRATEGIC_THINKING, 0.5)
        spiritual = profile.get(ProfileDimension.SPIRITUAL_RESONANCE, 0.5)
        
        if strategic > 0.7:
            self.teaching_style["analytical"] = min(1.0, self.teaching_style["analytical"] + 0.1)
            self.teaching_style["practical"] = min(1.0, self.teaching_style["practical"] + 0.1)
        
        if spiritual > 0.7:
            self.teaching_style["mystical"] = min(1.0, self.teaching_style["mystical"] + 0.1)
            self.teaching_style["philosophical"] = min(1.0, self.teaching_style["philosophical"] + 0.1)
        
        # Generate response based on adapted teaching style
        if self.teaching_style["analytical"] > self.teaching_style["mystical"]:
            return (
                f"Let us examine this systematically. {user_input} presents an "
                "opportunity to apply measured wisdom and careful analysis."
            )
        else:
            return (
                f"Ah, {user_input} touches upon deeper mysteries. Consider how "
                "this relates to the cosmic patterns and eternal cycles."
            ) 