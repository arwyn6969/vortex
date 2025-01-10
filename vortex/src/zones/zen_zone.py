"""
The Zen Zone - A tranquil space for deep understanding and mindful reflection.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import MonkPepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class ZenZone(Zone):
    """The Zen Zone - Where understanding blooms in the garden of mindfulness."""
    
    def __init__(self):
        # Initialize with Monk Pepe as the guide
        guide = MonkPepe()
        super().__init__("Zen Zone", guide)
        
        self.description = (
            "A serene garden where digital cherry blossoms float eternally in the air. "
            "Stone paths wind between quantum meditation pools, their surfaces perfectly "
            "still yet swirling with infinite possibilities. The gentle sound of "
            "a bamboo fountain keeps time with the universe's heartbeat."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.UNDERSTANDING: 0.6,
            ProfileDimension.MINDFULNESS: 0.5,
            ProfileDimension.WISDOM: 0.4,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.UNDERSTANDING,
            ProfileDimension.MINDFULNESS
        ]
        
        self.min_dimension_values = {
            ProfileDimension.UNDERSTANDING: 0.3,
            ProfileDimension.MINDFULNESS: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Void",
            "color": "Zen Purple",
            "sefirot": SefirotAttribute.BINAH,
            "animal": "Monk Pepe",
            "mineral": "Amethyst"
        }
        
    def setup_challenges(self) -> None:
        """Initialize the zone's challenge system."""
        self.challenges = {
            "mindful_path": {
                "title": "The Path of Presence",
                "description": "Learn to walk the path of mindful awareness.",
                "practices": [
                    "Breath awareness meditation",
                    "Walking meditation",
                    "Mindful observation",
                    "Present moment anchoring"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.MINDFULNESS: 0.1,
                    ProfileDimension.UNDERSTANDING: 0.1
                }
            },
            "wisdom_pool": {
                "title": "The Pool of Reflection",
                "description": "Dive deep into the waters of understanding.",
                "difficulty": 0.7,
                "practices": [
                    "Question contemplation",
                    "Insight cultivation",
                    "Wisdom integration"
                ],
                "rewards": {
                    ProfileDimension.WISDOM: 0.2,
                    ProfileDimension.UNDERSTANDING: 0.2
                }
            },
            "enlightenment_quest": {
                "title": "The Ultimate Understanding",
                "description": "Seek the highest state of clarity and wisdom.",
                "options": {
                    "insight": {
                        "description": "Direct perception of reality's nature",
                        "impact": {
                            ProfileDimension.UNDERSTANDING: 0.3,
                            ProfileDimension.WISDOM: 0.2
                        }
                    },
                    "integration": {
                        "description": "Harmonious union of wisdom and daily life",
                        "impact": {
                            ProfileDimension.MINDFULNESS: 0.2,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                            ProfileDimension.UNDERSTANDING: 0.1
                        }
                    }
                },
                "difficulty": 0.9
            }
        }
        
    def get_available_challenges(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> List[ContentItem]:
        """Get challenges appropriate for the user's profile."""
        try:
            if not isinstance(profile, dict):
                raise ValueError("Profile must be a dictionary")
                
            difficulty = self.get_challenge_difficulty(profile)
            
            challenges = [
                ContentItem(
                    content_id="mindful_path",
                    content="The Path of Presence: Learn to walk the path of mindful awareness.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.3,
                    creativity_required=0.2,
                    strategic_depth=0.4
                ),
                ContentItem(
                    content_id="wisdom_pool",
                    content="The Pool of Reflection: Dive deep into the waters of understanding.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.5,
                    creativity_required=0.4,
                    strategic_depth=0.7
                ),
                ContentItem(
                    content_id="enlightenment_quest",
                    content="The Ultimate Understanding: Seek the highest state of clarity and wisdom.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.9,
                    emotional_intensity=0.8,
                    creativity_required=0.6,
                    strategic_depth=0.9
                )
            ]
            
            # Filter challenges based on difficulty
            return [c for c in challenges if abs(c.difficulty_level - difficulty) < 0.3]
            
        except Exception as e:
            self.guide.speak(f"Error getting challenges: {str(e)}")
            return []
            
    def process_interaction(
        self,
        interaction_type: str,
        context: str,
        duration: float,
        metadata: Optional[Dict] = None
    ) -> Dict[ProfileDimension, float]:
        """Process user interaction and return dimension impacts."""
        try:
            metadata = metadata or {}
            impacts = {}
            
            if interaction_type == "mindful_path":
                # Validate mindfulness metadata
                if not isinstance(metadata.get('presence_level'), (int, float)):
                    raise ValueError("mindful_path requires 'presence_level' number")
                if not isinstance(metadata.get('awareness_score', 0.5), (int, float)):
                    raise ValueError("awareness_score must be a number")
                    
                presence = max(0.0, min(1.0, metadata.get('presence_level', 0.5)))
                awareness = max(0.0, min(1.0, metadata.get('awareness_score', 0.5)))
                
                impacts[ProfileDimension.MINDFULNESS] = 0.1 * presence * awareness
                impacts[ProfileDimension.UNDERSTANDING] = 0.1 * awareness
                
            elif interaction_type == "wisdom_pool":
                # Validate wisdom metadata
                if not isinstance(metadata.get('depth', 0.5), (int, float)):
                    raise ValueError("depth must be a number")
                if not isinstance(metadata.get('clarity', 0.5), (int, float)):
                    raise ValueError("clarity must be a number")
                    
                depth = max(0.0, min(1.0, metadata.get('depth', 0.5)))
                clarity = max(0.0, min(1.0, metadata.get('clarity', 0.5)))
                
                impacts[ProfileDimension.WISDOM] = 0.1 * depth
                impacts[ProfileDimension.UNDERSTANDING] = 0.1 * clarity
                
            elif interaction_type == "enlightenment_quest":
                # Validate enlightenment metadata
                if not isinstance(metadata.get('insight', 0.5), (int, float)):
                    raise ValueError("insight must be a number")
                if not isinstance(metadata.get('integration', 0.5), (int, float)):
                    raise ValueError("integration must be a number")
                    
                insight = max(0.0, min(1.0, metadata.get('insight', 0.5)))
                integration = max(0.0, min(1.0, metadata.get('integration', 0.5)))
                
                impacts[ProfileDimension.UNDERSTANDING] = 0.2 * insight
                impacts[ProfileDimension.WISDOM] = 0.1 * integration
                impacts[ProfileDimension.MINDFULNESS] = 0.1 * (insight + integration) / 2
                
            else:
                raise ValueError(f"Unknown interaction type: {interaction_type}")
                
            return impacts
            
        except Exception as e:
            self.guide.speak(f"Error processing interaction: {str(e)}")
            return {}
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        
        if progress < 0.3:
            return (
                "Welcome to the Zen Zone, mindful fren. "
                "Let us begin by cultivating presence and awareness."
            )
        elif progress < 0.6:
            return (
                "Your mindfulness grows stronger each day! "
                "The waters of wisdom are becoming clearer."
            )
        elif progress < 0.9:
            return (
                "You're becoming one with the present moment, fren. "
                "Your understanding illuminates the path for others."
            )
        else:
            return (
                "You have touched the face of wisdom, dear fren. "
                "Now help others find their way to understanding."
            ) 