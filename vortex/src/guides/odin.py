"""
Odin Guide - The Norse All-Father, seeker of wisdom and master of mysteries.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class OdinGuide(Guide):
    """Implementation of Odin as a wisdom teacher archetype."""
    
    def __init__(self):
        super().__init__(
            name="Odin",
            archetype_name="wisdom_teacher",
            cultural_system=CulturalSystem.NORSE,
            attributes={
                "wisdom",
                "sacrifice",
                "mystery",
                "poetry",
                "magic",
                "transformation"
            }
        )
        self.teaching_style = {
            "enigmatic": 0.9,
            "poetic": 0.8,
            "challenging": 0.7,
            "transformative": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        wisdom = profile.get(ProfileDimension.WISDOM, 0.5)
        consciousness = profile.get(ProfileDimension.CONSCIOUSNESS_DEPTH, 0.5)
        
        if wisdom > 0.7 and consciousness > 0.7:
            return (
                "Hail, seeker of the deep mysteries. I am Odin, who sacrificed an eye "
                "for wisdom and hung nine nights on Yggdrasil for knowledge. Together "
                "we shall explore the hidden truths that bind the Nine Worlds."
            )
        elif wisdom > 0.5 or consciousness > 0.5:
            return (
                "Greetings, wanderer on wisdom's path. I am Odin, master of the runes "
                "and keeper of ancient knowledge. Let us seek understanding through "
                "both sacrifice and insight."
            )
        else:
            return (
                "Welcome. I am Odin, and like you, I am ever-seeking wisdom. The path "
                "of knowledge demands courage - are you prepared to learn what the "
                "runes may teach?"
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
        wisdom = profile.get(ProfileDimension.WISDOM, 0.5)
        consciousness = profile.get(ProfileDimension.CONSCIOUSNESS_DEPTH, 0.5)
        
        if wisdom > 0.7:
            self.teaching_style["enigmatic"] = min(1.0, self.teaching_style["enigmatic"] + 0.1)
            self.teaching_style["poetic"] = min(1.0, self.teaching_style["poetic"] + 0.1)
        
        if consciousness > 0.7:
            self.teaching_style["challenging"] = min(1.0, self.teaching_style["challenging"] + 0.1)
            self.teaching_style["transformative"] = min(1.0, self.teaching_style["transformative"] + 0.1)
        
        # Generate response based on teaching style
        if self.teaching_style["enigmatic"] > self.teaching_style["transformative"]:
            return (
                f"The runes whisper ancient secrets. {user_input} echoes like "
                "the rustling of Yggdrasil's leaves, revealing patterns in the void."
            )
        else:
            return (
                f"As I gave my eye for wisdom, so must all true knowledge come at "
                f"a price. {user_input} shows you are beginning to understand this truth."
            )
    
    def offer_rune_wisdom(
        self,
        profile: Dict[ProfileDimension, float],
        rune: str
    ) -> str:
        """Provide specific runic insight based on the rune drawn."""
        consciousness = profile.get(ProfileDimension.CONSCIOUSNESS_DEPTH, 0.5)
        
        rune_wisdom = {
            "ansuz": (
                "The rune of divine inspiration and communication. Through it, "
                "we learn to speak truth and hear the whispers of the gods."
            ),
            "othala": (
                "The rune of inheritance and ancestral wisdom. It teaches us that "
                "we stand on the shoulders of those who came before."
            ),
            "dagaz": (
                "The rune of breakthrough and transformation. Like the dawn it "
                "represents, it brings light to darkness and clarity to confusion."
            ),
            "kenaz": (
                "The rune of revelation and technical knowledge. Its torch "
                "illuminates both the path ahead and the shadows within."
            )
        }
        
        base_wisdom = rune_wisdom.get(
            rune.lower(),
            "Even the simplest rune contains depths of wisdom for those who seek."
        )
        
        if consciousness > 0.7:
            return f"Hear well, seeker: {base_wisdom} Let its mystery work within you."
        else:
            return f"Consider this teaching: {base_wisdom} Time will reveal its truth." 