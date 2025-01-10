"""
The Comfy Cabin - A cozy sanctuary of warmth, kindness, and emotional understanding.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import CozyPepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class ComfyCabin(Zone):
    """The Comfy Cabin - Where warmth and kindness create the comfiest vibes."""
    
    def __init__(self):
        # Initialize with Cozy Pepe as the guide
        guide = CozyPepe()
        super().__init__("Comfy Cabin", guide)
        
        self.description = (
            "A warm, inviting cabin where a perpetual fire crackles in the hearth. "
            "Soft blankets float gently through the air, wrapping visitors in pure comf. "
            "The sweet aroma of hot chocolate and freshly baked cookies fills the space, "
            "while lofi beats play softly in the background."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.EMPATHY: 0.6,
            ProfileDimension.MORAL_ALIGNMENT: 0.4,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.3,
            ProfileDimension.COMPASSION: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.EMPATHY,
            ProfileDimension.MORAL_ALIGNMENT
        ]
        
        self.min_dimension_values = {
            ProfileDimension.EMPATHY: 0.3,
            ProfileDimension.MORAL_ALIGNMENT: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Water",
            "color": "Comfy Blue",
            "sefirot": SefirotAttribute.CHESED,
            "animal": "Sleepy Pepe",
            "mineral": "Moonstone"
        }
        
    def setup_challenges(self) -> None:
        """Initialize the cabin's challenge system."""
        self.challenges = {
            "blanket_fort": {
                "title": "The Cozy Construction",
                "description": "Build a sanctuary of comfort for those in need of warmth.",
                "stages": [
                    "Gather the softest blankets",
                    "Arrange perfect pillow support",
                    "Create optimal snuggle spaces",
                    "Share the comf with others"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.EMPATHY: 0.1,
                    ProfileDimension.COMPASSION: 0.1
                }
            },
            "feels_sharing": {
                "title": "The Emotion Exchange",
                "description": "Create a safe space for sharing and understanding feelings.",
                "difficulty": 0.7,
                "activities": [
                    "Prepare comfy conversation nooks",
                    "Brew understanding-enhancing tea",
                    "Practice active listening"
                ],
                "rewards": {
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                    ProfileDimension.EMPATHY: 0.2
                }
            },
            "maximum_comf": {
                "title": "The Ultimate Comfy Challenge",
                "description": "Achieve the highest state of cozy enlightenment.",
                "options": {
                    "nurture": {
                        "description": "Create the perfect environment for emotional healing",
                        "impact": {
                            ProfileDimension.EMPATHY: 0.3,
                            ProfileDimension.COMPASSION: 0.2
                        }
                    },
                    "harmony": {
                        "description": "Establish perfect comfy balance for all",
                        "impact": {
                            ProfileDimension.MORAL_ALIGNMENT: 0.2,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                            ProfileDimension.EMPATHY: 0.1
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
                    content_id="blanket_fort",
                    content="The Cozy Construction: Build a sanctuary of comfort for those in need of warmth.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.5,
                    creativity_required=0.4,
                    strategic_depth=0.2
                ),
                ContentItem(
                    content_id="feels_sharing",
                    content="The Emotion Exchange: Create a safe space for sharing and understanding feelings.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.8,
                    creativity_required=0.3,
                    strategic_depth=0.4
                ),
                ContentItem(
                    content_id="maximum_comf",
                    content="The Ultimate Comfy Challenge: Achieve the highest state of cozy enlightenment.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.9,
                    emotional_intensity=0.9,
                    creativity_required=0.5,
                    strategic_depth=0.3
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
            
            if interaction_type == "blanket_fort":
                # Validate fort metadata
                if not isinstance(metadata.get('comfort_level'), (int, float)):
                    raise ValueError("blanket_fort requires 'comfort_level' number")
                if not isinstance(metadata.get('sharing_factor', 0.5), (int, float)):
                    raise ValueError("sharing_factor must be a number")
                    
                comfort = max(0.0, min(1.0, metadata.get('comfort_level', 0.5)))
                sharing = max(0.0, min(1.0, metadata.get('sharing_factor', 0.5)))
                
                impacts[ProfileDimension.EMPATHY] = 0.1 * comfort * sharing
                impacts[ProfileDimension.COMPASSION] = 0.1 * sharing
                
            elif interaction_type == "feels_sharing":
                # Validate sharing metadata
                if not isinstance(metadata.get('openness', 0.5), (int, float)):
                    raise ValueError("openness must be a number")
                if not isinstance(metadata.get('understanding', 0.5), (int, float)):
                    raise ValueError("understanding must be a number")
                    
                openness = max(0.0, min(1.0, metadata.get('openness', 0.5)))
                understanding = max(0.0, min(1.0, metadata.get('understanding', 0.5)))
                
                impacts[ProfileDimension.EMOTIONAL_RESPONSE] = 0.1 * openness
                impacts[ProfileDimension.EMPATHY] = 0.1 * understanding
                
            elif interaction_type == "maximum_comf":
                # Validate comf metadata
                if not isinstance(metadata.get('coziness', 0.5), (int, float)):
                    raise ValueError("coziness must be a number")
                if not isinstance(metadata.get('harmony', 0.5), (int, float)):
                    raise ValueError("harmony must be a number")
                    
                coziness = max(0.0, min(1.0, metadata.get('coziness', 0.5)))
                harmony = max(0.0, min(1.0, metadata.get('harmony', 0.5)))
                
                impacts[ProfileDimension.EMPATHY] = 0.2 * coziness
                impacts[ProfileDimension.MORAL_ALIGNMENT] = 0.1 * harmony
                impacts[ProfileDimension.EMOTIONAL_RESPONSE] = 0.1 * (coziness + harmony) / 2
                
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
                "Welcome to the comfiest place in the Vortex, fren. "
                "Let's start by getting you nice and cozy."
            )
        elif progress < 0.6:
            return (
                "The comf is growing stronger in you! "
                "Your heart is warming up nicely to others."
            )
        elif progress < 0.9:
            return (
                "You're becoming a true master of comf, fren. "
                "Your presence brings warmth and peace to all."
            )
        else:
            return (
                "You have achieved peak comf, dear fren. "
                "Now help spread the cozy vibes to others who need them."
            ) 