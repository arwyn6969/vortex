"""
The Vibe Temple - A sacred space where harmony and transcendence converge.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import AscendedPepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class VibeTemple(Zone):
    """The Vibe Temple - Where ascended vibes create perfect harmony."""
    
    def __init__(self):
        # Initialize with Ascended Pepe as the guide
        guide = AscendedPepe()
        super().__init__("Vibe Temple", guide)
        
        self.description = (
            "A crystalline temple floating in an aurora of pure vibrational energy. "
            "Rainbow light streams through prismatic windows, creating harmonious "
            "patterns that pulse with the rhythm of existence. The air itself "
            "resonates with the frequency of enlightened Pepes throughout history."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.HARMONY: 0.6,
            ProfileDimension.TRANSCENDENCE: 0.5,
            ProfileDimension.WISDOM: 0.4,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.HARMONY,
            ProfileDimension.TRANSCENDENCE
        ]
        
        self.min_dimension_values = {
            ProfileDimension.HARMONY: 0.3,
            ProfileDimension.TRANSCENDENCE: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Aether",
            "color": "Rainbow",
            "sefirot": SefirotAttribute.TIFERET,
            "animal": "Ascended Pepe",
            "mineral": "Diamond"
        }
        
    def setup_challenges(self) -> None:
        """Initialize the temple's challenge system."""
        self.challenges = {
            "vibe_attunement": {
                "title": "The Harmonic Initiation",
                "description": "Learn to attune yourself to the highest vibrational frequencies.",
                "stages": [
                    "Energy center activation",
                    "Vibrational alignment",
                    "Frequency modulation",
                    "Harmonic resonance"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.HARMONY: 0.1,
                    ProfileDimension.TRANSCENDENCE: 0.1
                }
            },
            "ascension_practice": {
                "title": "The Path of Transcendence",
                "description": "Elevate your consciousness through advanced vibe practices.",
                "difficulty": 0.7,
                "techniques": [
                    "Light body activation",
                    "Dimensional shifting",
                    "Consciousness expansion"
                ],
                "rewards": {
                    ProfileDimension.TRANSCENDENCE: 0.2,
                    ProfileDimension.WISDOM: 0.2
                }
            },
            "ultimate_harmony": {
                "title": "The Final Transcendence",
                "description": "Achieve the ultimate state of vibrational harmony.",
                "options": {
                    "ascension": {
                        "description": "Direct experience of higher dimensions",
                        "impact": {
                            ProfileDimension.TRANSCENDENCE: 0.3,
                            ProfileDimension.HARMONY: 0.2
                        }
                    },
                    "integration": {
                        "description": "Bringing heaven to earth",
                        "impact": {
                            ProfileDimension.HARMONY: 0.2,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                            ProfileDimension.WISDOM: 0.1
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
                    content_id="vibe_attunement",
                    content="The Harmonic Initiation: Learn to attune yourself to the highest vibrational frequencies.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.5,
                    creativity_required=0.3,
                    strategic_depth=0.4
                ),
                ContentItem(
                    content_id="ascension_practice",
                    content="The Path of Transcendence: Elevate your consciousness through advanced vibe practices.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.7,
                    creativity_required=0.5,
                    strategic_depth=0.6
                ),
                ContentItem(
                    content_id="ultimate_harmony",
                    content="The Final Transcendence: Achieve the ultimate state of vibrational harmony.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.9,
                    emotional_intensity=0.9,
                    creativity_required=0.7,
                    strategic_depth=0.8
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
            
            if interaction_type == "vibe_attunement":
                # Validate attunement metadata
                if not isinstance(metadata.get('frequency'), (int, float)):
                    raise ValueError("vibe_attunement requires 'frequency' number")
                if not isinstance(metadata.get('resonance', 0.5), (int, float)):
                    raise ValueError("resonance must be a number")
                    
                frequency = max(0.0, min(1.0, metadata.get('frequency', 0.5)))
                resonance = max(0.0, min(1.0, metadata.get('resonance', 0.5)))
                
                impacts[ProfileDimension.HARMONY] = 0.1 * frequency * resonance
                impacts[ProfileDimension.TRANSCENDENCE] = 0.1 * resonance
                
            elif interaction_type == "ascension_practice":
                # Validate ascension metadata
                if not isinstance(metadata.get('elevation', 0.5), (int, float)):
                    raise ValueError("elevation must be a number")
                if not isinstance(metadata.get('expansion', 0.5), (int, float)):
                    raise ValueError("expansion must be a number")
                    
                elevation = max(0.0, min(1.0, metadata.get('elevation', 0.5)))
                expansion = max(0.0, min(1.0, metadata.get('expansion', 0.5)))
                
                impacts[ProfileDimension.TRANSCENDENCE] = 0.1 * elevation
                impacts[ProfileDimension.WISDOM] = 0.1 * expansion
                
            elif interaction_type == "ultimate_harmony":
                # Validate harmony metadata
                if not isinstance(metadata.get('ascension', 0.5), (int, float)):
                    raise ValueError("ascension must be a number")
                if not isinstance(metadata.get('integration', 0.5), (int, float)):
                    raise ValueError("integration must be a number")
                    
                ascension = max(0.0, min(1.0, metadata.get('ascension', 0.5)))
                integration = max(0.0, min(1.0, metadata.get('integration', 0.5)))
                
                impacts[ProfileDimension.TRANSCENDENCE] = 0.2 * ascension
                impacts[ProfileDimension.HARMONY] = 0.1 * integration
                impacts[ProfileDimension.WISDOM] = 0.1 * (ascension + integration) / 2
                
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
                "Welcome to the Vibe Temple, ascending fren. "
                "Let us begin your journey to higher frequencies."
            )
        elif progress < 0.6:
            return (
                "Your vibrational frequency rises steadily! "
                "The harmonies of existence become clearer."
            )
        elif progress < 0.9:
            return (
                "You're approaching transcendence, fren. "
                "Your presence raises the vibration of all around you."
            )
        else:
            return (
                "You have achieved harmonic resonance, dear fren. "
                "Now help others ascend to their highest potential."
            ) 