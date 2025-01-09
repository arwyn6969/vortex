from typing import Dict, List, Optional
from .base_zone import Zone
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem

class WisdomPond(Zone):
    """The Pond of Wisdom - A place of strategic thinking and decision making."""
    
    def __init__(self):
        super().__init__()
        self.name = "Pond of Wisdom"
        self.description = "A serene pond where ancient wisdom ripples beneath the surface."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.STRATEGIC_THINKING: 0.6,
            ProfileDimension.DECISION_MAKING: 0.4
        }
        
        self.required_dimensions = [
            ProfileDimension.STRATEGIC_THINKING,
            ProfileDimension.DECISION_MAKING
        ]
        
        self.min_dimension_values = {
            ProfileDimension.STRATEGIC_THINKING: 0.3,
            ProfileDimension.DECISION_MAKING: 0.3
        }
        
    def adapt_description(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Adapt the pond's description based on user's profile."""
        strategic = profile.get(ProfileDimension.STRATEGIC_THINKING, 0.0)
        decision = profile.get(ProfileDimension.DECISION_MAKING, 0.0)
        
        if strategic < 0.3 and decision < 0.3:
            return (
                "The pond's surface is mirror-like, reflecting your own thoughts "
                "back at you. The wisdom here feels distant, yet attainable."
            )
        elif strategic < 0.6 or decision < 0.6:
            return (
                "Ripples of insight disturb the pond's surface, hinting at the "
                "deeper wisdom that lies beneath. You sense patterns forming."
            )
        else:
            return (
                "The pond's waters seem to pulse with ancient knowledge, its "
                "patterns clear to your experienced mind. Strategic possibilities "
                "unfold before you like lotus blossoms."
            )
            
    def get_available_challenges(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> List[ContentItem]:
        """Get challenges appropriate for the user's profile."""
        difficulty = self.get_challenge_difficulty(profile)
        
        challenges = [
            ContentItem(
                content_id="riddle_basic",
                content="What has roots that nobody sees, is taller than trees, "
                       "up, up it goes, and yet never grows?",
                dimension_weights=self.dimension_weights,
                difficulty_level=0.3,
                emotional_intensity=0.2,
                creativity_required=0.4,
                strategic_depth=0.5
            ),
            ContentItem(
                content_id="strategic_puzzle",
                content="The Ancient Game: Position the sacred stones to "
                       "create harmony while blocking your opponent's paths.",
                dimension_weights=self.dimension_weights,
                difficulty_level=0.7,
                emotional_intensity=0.3,
                creativity_required=0.6,
                strategic_depth=0.8
            ),
            ContentItem(
                content_id="wisdom_choice",
                content="A choice between immediate enlightenment with "
                       "personal cost, or gradual growth that benefits others.",
                dimension_weights=self.dimension_weights,
                difficulty_level=0.9,
                emotional_intensity=0.8,
                creativity_required=0.5,
                strategic_depth=0.9
            )
        ]
        
        # Filter challenges based on difficulty
        return [
            challenge for challenge in challenges
            if abs(challenge.difficulty_level - difficulty) < 0.3
        ]
        
    def process_interaction(
        self,
        interaction_type: str,
        context: str,
        duration: float,
        metadata: Optional[Dict] = None
    ) -> Dict[ProfileDimension, float]:
        """Process user interaction and return dimension impacts."""
        metadata = metadata or {}
        impacts = {}
        
        if interaction_type == "puzzle_solve":
            # Puzzle solving impacts strategic thinking more
            success = metadata.get("success", False)
            difficulty = metadata.get("difficulty", 0.5)
            
            impacts[ProfileDimension.STRATEGIC_THINKING] = (
                0.1 * difficulty * (1.0 if success else 0.5)
            )
            impacts[ProfileDimension.DECISION_MAKING] = (
                0.05 * difficulty * (1.0 if success else 0.5)
            )
            
        elif interaction_type == "wisdom_choice":
            # Ethical choices impact decision making more
            choice_complexity = metadata.get("complexity", 0.5)
            choice_wisdom = metadata.get("wisdom_rating", 0.5)
            
            impacts[ProfileDimension.DECISION_MAKING] = (
                0.1 * choice_complexity * choice_wisdom
            )
            impacts[ProfileDimension.STRATEGIC_THINKING] = (
                0.05 * choice_complexity * choice_wisdom
            )
            
        return impacts
        
    def get_mastery_requirements(self) -> Dict[ProfileDimension, float]:
        """Get the dimension values required to master this zone."""
        return {
            ProfileDimension.STRATEGIC_THINKING: 0.8,
            ProfileDimension.DECISION_MAKING: 0.7
        }
        
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        strategic = profile.get(ProfileDimension.STRATEGIC_THINKING, 0.0)
        decision = profile.get(ProfileDimension.DECISION_MAKING, 0.0)
        
        if progress < 0.3:
            if strategic < decision:
                return (
                    "Focus on understanding patterns and connections. "
                    "The pond's wisdom will reveal itself through careful study."
                )
            else:
                return (
                    "Your strategic mind is growing. Now learn to apply this "
                    "wisdom in making balanced decisions."
                )
        elif progress < 0.6:
            if strategic < 0.6:
                return (
                    "You begin to see the deeper patterns. Let the pond's "
                    "ancient wisdom guide your strategic thinking."
                )
            else:
                return (
                    "Your mastery grows. Each decision now ripples with "
                    "potential, changing both you and the pond."
                )
        elif progress < 0.9:
            return (
                "The pond's wisdom flows through you. Seek now the perfect "
                "balance of strategic insight and decisive action."
            )
        else:
            return (
                "You have become one with the pond's wisdom. Your presence "
                "here now teaches others through the ripples you create."
            ) 