"""
Sekhmet Guide - The Egyptian goddess of divine judgment and retribution.
"""
from typing import Dict, Optional
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension

class SekhmetGuide(Guide):
    def __init__(self):
        super().__init__(
            name="Sekhmet",
            title="Goddess of Divine Judgment",
            description=(
                "A powerful lioness-headed figure radiating fierce authority. "
                "Her eyes burn with the fire of divine justice, and her presence "
                "demands respect and discipline."
            )
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Get personalized welcome message based on profile."""
        judgment = profile.get(ProfileDimension.JUDGMENT, 0.0)
        discipline = profile.get(ProfileDimension.DISCIPLINE, 0.0)
        
        if judgment < 0.3 and discipline < 0.3:
            return (
                "You stand before the waters of severity, seeker. Here, you will "
                "learn that true strength lies in knowing when to use power, and "
                "when to withhold it."
            )
        elif judgment < 0.6 or discipline < 0.6:
            return (
                "Your spirit shows promise, but can you maintain discipline when "
                "faced with difficult choices? The waters await your judgment."
            )
        else:
            return (
                "A disciplined soul returns. The crimson waters stir with "
                "recognition, ready to test your judgment once more."
            )
            
    def get_guidance_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Get contextual guidance based on profile."""
        judgment = profile.get(ProfileDimension.JUDGMENT, 0.0)
        discipline = profile.get(ProfileDimension.DISCIPLINE, 0.0)
        discernment = profile.get(ProfileDimension.DISCERNMENT, 0.0)
        
        if judgment < discipline:
            return (
                "Power without judgment is chaos. Study the laws etched in "
                "obsidian, for they teach the wisdom of boundaries."
            )
        elif discernment < judgment:
            return (
                "You see the law clearly, but can you see beyond it? True "
                "justice requires understanding the spirit, not just the letter."
            )
        else:
            return (
                "Your judgment grows sharp as a blade. Now learn when to strike, "
                "and when to hold back - for this too is power."
            )
            
    def get_contextual_response(
        self,
        profile: Dict[ProfileDimension, float],
        context: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """Get response based on context and profile."""
        metadata = metadata or {}
        
        if context == "judge":
            return (
                "Yes, focus your mind on the principles of divine law. Let your "
                "judgment be as sharp as a lion's claw, but as precise as a "
                "surgeon's blade."
            )
            
        elif context == "purify":
            return (
                "The flames of purification burn away all that is false. Embrace "
                "their cleansing power, but remember - even fire must be controlled."
            )
            
        elif context == "challenge_start":
            return (
                "A test of judgment lies before you. Remember - mercy without "
                "justice is weakness, but justice without mercy is tyranny."
            )
            
        elif context == "challenge_complete":
            success = metadata.get("success", False)
            if success:
                return (
                    "Well judged. You show wisdom in balancing power with "
                    "restraint. This is the true path of divine justice."
                )
            else:
                return (
                    "Your judgment faltered, but even this serves a purpose. "
                    "Learn from this, for divine law is perfected through trial."
                )
                
        return (
            "Consider the weight of your choices. Each judgment shapes not only "
            "the judged, but the judge as well."
        )
        
    def get_challenge_hint(self, challenge_id: str) -> str:
        """Get hint for specific challenge."""
        hints = {
            "boundary_test": (
                "Some boundaries protect, while others constrain. Wisdom lies "
                "in knowing which serve divine order, and which prevent growth."
            ),
            "justice_trial": (
                "True justice sees beyond the immediate act to its roots and "
                "consequences. Consider the whole tapestry, not just one thread."
            ),
            "purification_ritual": (
                "The flames of purification are impartial - they burn both the "
                "rot and the flower. Choose carefully what you offer to the fire."
            )
        }
        return hints.get(
            challenge_id,
            "Let divine law guide your judgment, but remember that law serves life."
        ) 