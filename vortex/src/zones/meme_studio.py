"""
The Meme Studio - A creative sanctuary where memes and artistic expression flow freely.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import ArtistPepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class MemeStudio(Zone):
    """The Meme Studio - Where creativity and expression become legendary."""
    
    def __init__(self):
        # Initialize with Artist Pepe as the guide
        guide = ArtistPepe()
        super().__init__("Meme Studio", guide)
        
        self.description = (
            "A vibrant digital atelier where memes come to life. Holographic canvases "
            "float in the air, splashed with the colors of viral potential. "
            "Rare Pepes of all varieties line the walls for inspiration, while "
            "the sound of creative energy crackles through fiber optic paintbrushes."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.CREATIVITY: 0.6,
            ProfileDimension.EXPRESSION: 0.5,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.4,
            ProfileDimension.ADAPTABILITY: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.CREATIVITY,
            ProfileDimension.EXPRESSION
        ]
        
        self.min_dimension_values = {
            ProfileDimension.CREATIVITY: 0.3,
            ProfileDimension.EXPRESSION: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Air",
            "color": "Creative Green",
            "sefirot": SefirotAttribute.NETZACH,
            "animal": "Artist Pepe",
            "mineral": "Opal"
        }
        
    def setup_challenges(self) -> None:
        """Initialize the studio's challenge system."""
        self.challenges = {
            "meme_basics": {
                "title": "The Fundamentals of Memecraft",
                "description": "Master the basic elements of meme creation.",
                "techniques": [
                    "Color theory and composition",
                    "Template selection and timing",
                    "Text placement and impact",
                    "Viral potential optimization"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.CREATIVITY: 0.1,
                    ProfileDimension.EXPRESSION: 0.1
                }
            },
            "rare_pepe_forge": {
                "title": "The Rare Pepe Workshop",
                "description": "Create increasingly rare and powerful Pepe variations.",
                "difficulty": 0.7,
                "processes": [
                    "Sketch the initial concept",
                    "Refine the emotional resonance",
                    "Add layers of meaning"
                ],
                "rewards": {
                    ProfileDimension.CREATIVITY: 0.2,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.2
                }
            },
            "meme_mastery": {
                "title": "The Ultimate Expression",
                "description": "Push the boundaries of meme creation to their limits.",
                "options": {
                    "innovation": {
                        "description": "Create entirely new meme formats",
                        "impact": {
                            ProfileDimension.CREATIVITY: 0.3,
                            ProfileDimension.EXPRESSION: 0.2
                        }
                    },
                    "synthesis": {
                        "description": "Combine existing formats in revolutionary ways",
                        "impact": {
                            ProfileDimension.ADAPTABILITY: 0.2,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                            ProfileDimension.CREATIVITY: 0.1
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
                    content_id="meme_basics",
                    content="The Fundamentals of Memecraft: Master the basic elements of meme creation.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.4,
                    creativity_required=0.6,
                    strategic_depth=0.3
                ),
                ContentItem(
                    content_id="rare_pepe_forge",
                    content="The Rare Pepe Workshop: Create increasingly rare and powerful Pepe variations.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.6,
                    creativity_required=0.8,
                    strategic_depth=0.5
                ),
                ContentItem(
                    content_id="meme_mastery",
                    content="The Ultimate Expression: Push the boundaries of meme creation to their limits.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.9,
                    emotional_intensity=0.7,
                    creativity_required=0.9,
                    strategic_depth=0.6
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
            
            if interaction_type == "meme_basics":
                # Validate basics metadata
                if not isinstance(metadata.get('technique_mastery'), (int, float)):
                    raise ValueError("meme_basics requires 'technique_mastery' number")
                if not isinstance(metadata.get('creativity_score', 0.5), (int, float)):
                    raise ValueError("creativity_score must be a number")
                    
                mastery = max(0.0, min(1.0, metadata.get('technique_mastery', 0.5)))
                creativity = max(0.0, min(1.0, metadata.get('creativity_score', 0.5)))
                
                impacts[ProfileDimension.CREATIVITY] = 0.1 * mastery * creativity
                impacts[ProfileDimension.EXPRESSION] = 0.1 * creativity
                
            elif interaction_type == "rare_pepe_forge":
                # Validate forge metadata
                if not isinstance(metadata.get('rarity', 0.5), (int, float)):
                    raise ValueError("rarity must be a number")
                if not isinstance(metadata.get('emotional_impact', 0.5), (int, float)):
                    raise ValueError("emotional_impact must be a number")
                    
                rarity = max(0.0, min(1.0, metadata.get('rarity', 0.5)))
                impact = max(0.0, min(1.0, metadata.get('emotional_impact', 0.5)))
                
                impacts[ProfileDimension.CREATIVITY] = 0.1 * rarity
                impacts[ProfileDimension.EMOTIONAL_RESPONSE] = 0.1 * impact
                
            elif interaction_type == "meme_mastery":
                # Validate mastery metadata
                if not isinstance(metadata.get('innovation', 0.5), (int, float)):
                    raise ValueError("innovation must be a number")
                if not isinstance(metadata.get('synthesis', 0.5), (int, float)):
                    raise ValueError("synthesis must be a number")
                    
                innovation = max(0.0, min(1.0, metadata.get('innovation', 0.5)))
                synthesis = max(0.0, min(1.0, metadata.get('synthesis', 0.5)))
                
                impacts[ProfileDimension.CREATIVITY] = 0.2 * innovation
                impacts[ProfileDimension.EXPRESSION] = 0.1 * synthesis
                impacts[ProfileDimension.ADAPTABILITY] = 0.1 * (innovation + synthesis) / 2
                
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
                "Welcome to the Meme Studio, creative fren! "
                "Let's start by mastering the basics of memecraft."
            )
        elif progress < 0.6:
            return (
                "Your meme game is getting stronger! "
                "Time to start forging some rare Pepes."
            )
        elif progress < 0.9:
            return (
                "You're becoming a true meme artist, fren. "
                "Your creations are reaching legendary status!"
            )
        else:
            return (
                "You've achieved meme mastery, dear fren. "
                "Now go forth and spread your dank creations to the world."
            ) 