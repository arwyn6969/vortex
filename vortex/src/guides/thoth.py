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
    
    # Removed hardcoded welcome message - now uses LLM-powered welcome from base class
    
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
        wisdom = profile.get(ProfileDimension.WISDOM, 0.5)
        consciousness = profile.get(ProfileDimension.CONSCIOUSNESS_DEPTH, 0.5)
        
        if strategic > 0.7:
            self.teaching_style["analytical"] = min(1.0, self.teaching_style["analytical"] + 0.1)
            self.teaching_style["practical"] = min(1.0, self.teaching_style["practical"] + 0.1)
        
        if wisdom > 0.7:
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