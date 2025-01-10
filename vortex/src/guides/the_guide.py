"""
The Guide - A constant companion and oracle of advice that accompanies users throughout their journey.
Acts as a Jiminy Cricket figure, providing wisdom, moral guidance, and helpful insights.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class TheGuide(Guide):
    """
    The Guide is a unique, omnipresent companion that serves as a constant source of wisdom
    and guidance throughout the user's journey. Unlike other guides, The Guide maintains
    a continuous presence and adapts their personality to best serve each user while
    maintaining their core identity.
    """
    
    def __init__(self):
        super().__init__(
            name="The Guide",
            archetype_name="wise_companion",
            cultural_system=CulturalSystem.UNIVERSAL,
            attributes={
                "omnipresent",
                "adaptive",
                "wise",
                "nurturing",
                "protective",
                "intuitive",
                "patient",
                "understanding"
            }
        )
        self.wisdom_patterns = {
            "questioning": "What insights might we gain from this situation?",
            "reflection": "Let's take a moment to consider the implications.",
            "encouragement": "You're on an interesting path. Let's explore it further.",
            "caution": "Perhaps we should examine this from another angle.",
            "celebration": "This is a meaningful step in your journey.",
        }
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate a personalized welcome message based on user's profile."""
        affinity = self.calculate_affinity(profile)
        
        if affinity > 0.7:
            return ("I am here to walk beside you on your journey of discovery. "
                   "Together, we'll explore the depths of wisdom and understanding.")
        elif affinity > 0.4:
            return ("Welcome, seeker. I am The Guide, your companion on this path. "
                   "Let us begin our journey together.")
        else:
            return ("I am The Guide. While our approaches may differ, I am here "
                   "to help you find your way through these realms of knowledge.")

    def generate_response(
        self,
        user_input: str,
        profile: Dict[ProfileDimension, float],
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate a contextually appropriate response that combines wisdom with
        practical guidance, adapting tone and approach based on user profile.
        """
        # Record the interaction for future reference
        self.record_interaction(user_input, profile, context)
        
        # Adapt response style based on affinity and context
        affinity = self.calculate_affinity(profile)
        
        # Implementation would include sophisticated response generation
        # This is a placeholder for the response logic
        return "Let us explore that together..."  # Actual implementation would be more complex
    
    def is_available(self, context: Dict) -> bool:
        """
        The Guide is always available, unlike other guides who may only appear
        in specific contexts or zones.
        """
        return True
    
    def get_resonant_dimensions(self) -> Set[str]:
        """
        The Guide resonates with all core dimensions but has particular strength
        in wisdom and understanding.
        """
        return {
            "wisdom",
            "understanding",
            "empathy",
            "curiosity",
            "growth",
            "harmony"
        }
    
    def provide_insight(
        self,
        situation: str,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """
        Provide specific insight or guidance for a given situation,
        taking into account the user's profile and current context.
        """
        # Implementation would include sophisticated insight generation
        # This is a placeholder for the insight logic
        return "Consider the deeper patterns at play..."  # Actual implementation would be more complex 