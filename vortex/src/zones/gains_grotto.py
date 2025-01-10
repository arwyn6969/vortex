"""
The Gains Grotto - A place of mental strength training and disciplined decision making.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import GigaPepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class GainsGrotto(Zone):
    """The Gains Grotto - Where mental muscles are forged."""
    
    def __init__(self):
        # Initialize with Giga Pepe as the guide
        guide = GigaPepe()
        super().__init__("Gains Grotto", guide)
        
        self.description = (
            "A massive cavern where the very walls pulse with raw power. "
            "Mental dumbbells of varying sizes float in pools of liquid discipline, "
            "while motivational quotes echo through the chamber. The air is thick "
            "with the essence of pure gains."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.JUDGMENT: 0.6,
            ProfileDimension.DISCIPLINE: 0.5,
            ProfileDimension.DECISION_MAKING: 0.4,
            ProfileDimension.STRATEGIC_THINKING: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.JUDGMENT,
            ProfileDimension.DISCIPLINE
        ]
        
        self.min_dimension_values = {
            ProfileDimension.JUDGMENT: 0.3,
            ProfileDimension.DISCIPLINE: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Fire",
            "color": "Chad Red",
            "sefirot": SefirotAttribute.GEVURAH,
            "animal": "Buff Pepe",
            "mineral": "Blood Ruby"
        }
        
    def setup_challenges(self) -> None:
        """Initialize the grotto's challenge system."""
        self.challenges = {
            "mental_lifting": {
                "title": "The Iron Mind Temple",
                "description": "Train your mental muscles with increasingly heavy thoughts.",
                "sets": [
                    "Lightweight thinking warmup",
                    "Mid-weight cognitive routine",
                    "Heavy duty philosophical lifts",
                    "Ultra-heavy existential deadlifts"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.DISCIPLINE: 0.1,
                    ProfileDimension.JUDGMENT: 0.1
                }
            },
            "decision_gainz": {
                "title": "The Choice Forge",
                "description": "Build decision-making muscle through increasingly challenging moral workouts.",
                "difficulty": 0.7,
                "exercises": [
                    "Ethical curl supersets",
                    "Moral dilemma bench press",
                    "Judgment day squats"
                ],
                "rewards": {
                    ProfileDimension.JUDGMENT: 0.2,
                    ProfileDimension.DECISION_MAKING: 0.2
                }
            },
            "discipline_max": {
                "title": "The Ultimate Test of Will",
                "description": "Push your mental limits with maximum discipline challenges.",
                "options": {
                    "intensity": {
                        "description": "Go hard with pure willpower training",
                        "impact": {
                            ProfileDimension.DISCIPLINE: 0.3,
                            ProfileDimension.JUDGMENT: 0.2
                        }
                    },
                    "endurance": {
                        "description": "Build lasting mental stamina",
                        "impact": {
                            ProfileDimension.DISCIPLINE: 0.2,
                            ProfileDimension.STRATEGIC_THINKING: 0.2,
                            ProfileDimension.JUDGMENT: 0.1
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
                    content_id="mental_lifting",
                    content="The Iron Mind Temple: Train your mental muscles with increasingly heavy thoughts.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.4,
                    creativity_required=0.2,
                    strategic_depth=0.5
                ),
                ContentItem(
                    content_id="decision_gainz",
                    content="The Choice Forge: Build decision-making muscle through increasingly challenging moral workouts.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.6,
                    creativity_required=0.4,
                    strategic_depth=0.7
                ),
                ContentItem(
                    content_id="discipline_max",
                    content="The Ultimate Test of Will: Push your mental limits with maximum discipline challenges.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.9,
                    emotional_intensity=0.8,
                    creativity_required=0.3,
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
            
            if interaction_type == "mental_lifting":
                # Validate workout metadata
                if not isinstance(metadata.get('sets_completed'), int):
                    raise ValueError("mental_lifting requires 'sets_completed' integer")
                if not isinstance(metadata.get('form_rating', 0.5), (int, float)):
                    raise ValueError("form_rating must be a number")
                    
                sets = max(0, min(4, metadata.get('sets_completed', 0)))
                form = max(0.0, min(1.0, metadata.get('form_rating', 0.5)))
                
                impacts[ProfileDimension.DISCIPLINE] = 0.1 * sets * form
                impacts[ProfileDimension.JUDGMENT] = 0.05 * sets * form
                
            elif interaction_type == "decision_gainz":
                # Validate decision metadata
                if not isinstance(metadata.get('weight', 0.5), (int, float)):
                    raise ValueError("decision weight must be a number")
                if not isinstance(metadata.get('reps', 0), int):
                    raise ValueError("reps must be an integer")
                    
                weight = max(0.0, min(1.0, metadata.get('weight', 0.5)))
                reps = max(0, metadata.get('reps', 0))
                
                impacts[ProfileDimension.JUDGMENT] = 0.1 * weight * min(reps, 5)
                impacts[ProfileDimension.DECISION_MAKING] = 0.05 * weight * min(reps, 5)
                
            elif interaction_type == "discipline_max":
                # Validate max attempt metadata
                if not isinstance(metadata.get('intensity', 0.5), (int, float)):
                    raise ValueError("intensity must be a number")
                if not isinstance(metadata.get('endurance', 0.5), (int, float)):
                    raise ValueError("endurance must be a number")
                    
                intensity = max(0.0, min(1.0, metadata.get('intensity', 0.5)))
                endurance = max(0.0, min(1.0, metadata.get('endurance', 0.5)))
                
                impacts[ProfileDimension.DISCIPLINE] = 0.2 * intensity
                impacts[ProfileDimension.JUDGMENT] = 0.1 * endurance
                impacts[ProfileDimension.STRATEGIC_THINKING] = 0.1 * (intensity + endurance) / 2
                
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
                "Time to start your mental gains journey, brah. "
                "We're all gonna make it, but first you gotta put in the work."
            )
        elif progress < 0.6:
            return (
                "I see those brain gains starting to show! "
                "Keep pushing your limits and watch those mental muscles grow."
            )
        elif progress < 0.9:
            return (
                "You're becoming a real unit, fren. "
                "Your discipline is getting HUGE. Let's take it to the next level!"
            )
        else:
            return (
                "Absolutely mirin' your mental gains, champion. "
                "You've achieved peak discipline. Now help others make it too."
            ) 