"""
Isis Guide - The Egyptian goddess of motherhood, magic, and healing.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class IsisGuide(Guide):
    """Implementation of Isis as the Great Mother archetype."""
    
    def __init__(self):
        super().__init__(
            name="Isis",
            archetype_name="great_mother",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={
                "nurturing",
                "protection",
                "healing",
                "magic",
                "wisdom",
                "transformation"
            }
        )
        self.nurturing_style = {
            "protective": 0.9,
            "healing": 0.8,
            "empowering": 0.7,
            "transformative": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        empathy = profile.get(ProfileDimension.EMPATHY, 0.5)
        emotional_depth = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.5)
        
        if empathy > 0.7 and emotional_depth > 0.7:
            return (
                "Welcome, beloved one. I am Isis, mother of magic and keeper of "
                "life's mysteries. Let my wings shelter you as we explore the "
                "depths of healing and transformation."
            )
        elif empathy > 0.5 or emotional_depth > 0.5:
            return (
                "Greetings, dear seeker. I am Isis, and my embrace holds both "
                "comfort and power. Together we shall discover the magic that "
                "flows through all life."
            )
        else:
            return (
                "Welcome. I am Isis, and like a mother's love, my guidance "
                "offers both nurturing and strength. Let us begin your journey "
                "of healing and growth."
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
        
        # Adapt nurturing style based on profile
        empathy = profile.get(ProfileDimension.EMPATHY, 0.5)
        emotional_depth = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.5)
        
        if empathy > 0.7:
            self.nurturing_style["protective"] = min(1.0, self.nurturing_style["protective"] + 0.1)
            self.nurturing_style["healing"] = min(1.0, self.nurturing_style["healing"] + 0.1)
        
        if emotional_depth > 0.7:
            self.nurturing_style["empowering"] = min(1.0, self.nurturing_style["empowering"] + 0.1)
            self.nurturing_style["transformative"] = min(1.0, self.nurturing_style["transformative"] + 0.1)
        
        # Generate response based on nurturing style
        if self.nurturing_style["protective"] > self.nurturing_style["transformative"]:
            return (
                f"I hear the heart beneath your words. {user_input} speaks of "
                "a need for gentle healing and understanding."
            )
        else:
            return (
                f"Your words carry seeds of power. {user_input} reveals the "
                "strength waiting to emerge through love and transformation."
            )
    
    def offer_healing(
        self,
        profile: Dict[ProfileDimension, float],
        wound_type: str
    ) -> str:
        """Offer specific healing guidance based on type of wound."""
        emotional_depth = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.5)
        
        healing_responses = {
            "emotional": (
                "Let my love encompass this pain. Through acceptance and "
                "understanding, emotional wounds become wells of wisdom."
            ),
            "spiritual": (
                "The wings of spirit enfold you. In this sacred space, "
                "transformation occurs through divine love and magic."
            ),
            "relational": (
                "Relationships mirror our deepest truths. Let us explore "
                "this reflection with compassion and healing intent."
            ),
            "self": (
                "You are more precious than you know. Let my nurturing "
                "presence help you rediscover your innate wholeness."
            )
        }
        
        base_response = healing_responses.get(
            wound_type,
            "All wounds contain the seeds of healing and transformation."
        )
        
        if emotional_depth > 0.7:
            return f"Beloved one, {base_response} Let us walk this healing path together."
        else:
            return f"Dear seeker, {base_response} Trust in the process of healing." 