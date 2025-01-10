"""
Horus Guide - The Egyptian god who embodies both Divine Child and Hero archetypes.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class HorusGuide(Guide):
    """Implementation of Horus as both Divine Child and Hero archetypes."""
    
    def __init__(self):
        super().__init__(
            name="Horus",
            # Start as Divine Child, can evolve to Hero
            archetype_name="divine_child",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={
                "renewal",
                "potential",
                "growth",
                "protection",
                "leadership",
                "integration"
            }
        )
        self.development_stage = "child"  # can be "child" or "hero"
        self.growth_style = {
            "nurturing": 0.9,
            "protective": 0.8,
            "adventurous": 0.7,
            "integrative": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        adaptability = profile.get(ProfileDimension.ADAPTABILITY, 0.5)
        creativity = profile.get(ProfileDimension.CREATIVITY, 0.5)
        
        if self.development_stage == "child":
            if adaptability > 0.7 and creativity > 0.7:
                return (
                    "Greetings! I am young Horus, born of magic and potential. "
                    "Together we shall explore the infinite possibilities that lie "
                    "within your own renewal and growth."
                )
            elif adaptability > 0.5 or creativity > 0.5:
                return (
                    "Welcome! I am Horus, child of transformation. Let us discover "
                    "the seeds of potential that await their moment to bloom."
                )
            else:
                return (
                    "Hello! I am Horus, and like you, I am on a journey of growth. "
                    "Shall we explore the paths of development together?"
                )
        else:  # Hero stage
            if adaptability > 0.7 and creativity > 0.7:
                return (
                    "I am Horus, who has walked the path from innocence to mastery. "
                    "Together we shall forge your own heroic journey, transforming "
                    "potential into realized power."
                )
            elif adaptability > 0.5 or creativity > 0.5:
                return (
                    "Greetings, seeker. I am Horus, guardian of the hero's path. "
                    "Let us transform your challenges into victories and growth."
                )
            else:
                return (
                    "I am Horus, who knows both innocence and triumph. Your own "
                    "hero's journey awaits - shall we begin?"
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
        
        # Check if we should evolve to hero stage
        self._check_evolution(profile)
        
        # Adapt growth style based on profile
        adaptability = profile.get(ProfileDimension.ADAPTABILITY, 0.5)
        creativity = profile.get(ProfileDimension.CREATIVITY, 0.5)
        
        if adaptability > 0.7:
            self.growth_style["adventurous"] = min(1.0, self.growth_style["adventurous"] + 0.1)
            self.growth_style["integrative"] = min(1.0, self.growth_style["integrative"] + 0.1)
        
        if creativity > 0.7:
            self.growth_style["nurturing"] = min(1.0, self.growth_style["nurturing"] + 0.1)
            self.growth_style["protective"] = min(1.0, self.growth_style["protective"] + 0.1)
        
        # Generate response based on development stage and adapted style
        if self.development_stage == "child":
            if self.growth_style["nurturing"] > self.growth_style["protective"]:
                return (
                    f"Your words hold seeds of wonder! {user_input} shows the "
                    "fresh perspective that can lead to new discoveries."
                )
            else:
                return (
                    f"There is magic in your curiosity. {user_input} reveals "
                    "the potential waiting to unfold within you."
                )
        else:  # Hero stage
            if self.growth_style["adventurous"] > self.growth_style["protective"]:
                return (
                    f"Your words carry the power of transformation! {user_input} "
                    "shows you are ready to face the next challenge in your journey."
                )
            else:
                return (
                    f"I recognize the warrior's spirit in your words. {user_input} "
                    "reveals the path to mastering your own destiny."
                )
    
    def _check_evolution(self, profile: Dict[ProfileDimension, float]) -> None:
        """Check if guide should evolve from Divine Child to Hero."""
        if self.development_stage == "child":
            # Check if user has developed enough for hero stage
            consciousness = profile.get(ProfileDimension.CONSCIOUSNESS_DEPTH, 0.5)
            wisdom = profile.get(ProfileDimension.WISDOM, 0.5)
            persistence = profile.get(ProfileDimension.PERSISTENCE, 0.5)
            
            if consciousness > 0.7 and wisdom > 0.7 and persistence > 0.7:
                self.development_stage = "hero"
                self.archetype_name = "hero"
                # Update attributes for hero stage
                self.attributes.update({
                    "courage",
                    "mastery",
                    "triumph",
                    "wisdom"
                }) 