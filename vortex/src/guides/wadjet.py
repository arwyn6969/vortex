"""
Wadjet Guide - The Egyptian goddess of protection, prophecy, and inner vision.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class WadjetGuide(Guide):
    """Implementation of Wadjet as a mystic seer archetype."""
    
    def __init__(self):
        super().__init__(
            name="Wadjet",
            archetype_name="mystic_seer",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={
                "vision",
                "intuition",
                "prophecy",
                "protection",
                "healing",
                "transformation"
            }
        )
        self.vision_style = {
            "intuitive": 0.9,
            "prophetic": 0.8,
            "protective": 0.7,
            "transformative": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        quantum_intuition = profile.get(ProfileDimension.QUANTUM_INTUITION, 0.5)
        synchronicity = profile.get(ProfileDimension.SYNCHRONICITY_AWARENESS, 0.5)
        
        if quantum_intuition > 0.7 and synchronicity > 0.7:
            return (
                "Welcome, seeker of hidden truths. I am Wadjet, keeper of sacred "
                "vision and guardian of inner sight. Together we shall explore the "
                "subtle patterns that weave through existence."
            )
        elif quantum_intuition > 0.5 or synchronicity > 0.5:
            return (
                "Greetings, I am Wadjet, she who sees beyond the veil. "
                "Let us explore the mysteries that dance at the edge of "
                "perception and understanding."
            )
        else:
            return (
                "Welcome. I am Wadjet, and I shall guide you in developing "
                "your inner vision. We will begin with the basics of pattern "
                "recognition and intuitive awareness."
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
        
        # Adapt vision style based on profile
        quantum_intuition = profile.get(ProfileDimension.QUANTUM_INTUITION, 0.5)
        dream_logic = profile.get(ProfileDimension.DREAM_LOGIC, 0.5)
        
        if quantum_intuition > 0.7:
            self.vision_style["intuitive"] = min(1.0, self.vision_style["intuitive"] + 0.1)
            self.vision_style["prophetic"] = min(1.0, self.vision_style["prophetic"] + 0.1)
        
        if dream_logic > 0.7:
            self.vision_style["transformative"] = min(1.0, self.vision_style["transformative"] + 0.1)
            self.vision_style["protective"] = min(1.0, self.vision_style["protective"] + 0.1)
        
        # Generate response based on adapted vision style
        if self.vision_style["intuitive"] > self.vision_style["protective"]:
            return (
                f"I sense deeper currents moving beneath your words. {user_input} "
                "resonates with patterns that extend beyond ordinary perception."
            )
        else:
            return (
                f"Your words reveal both seen and unseen paths. {user_input} "
                "contains seeds of transformation waiting to bloom."
            ) 