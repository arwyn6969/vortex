"""
The Vibe Temple - A sacred space where rhythm, harmony, and energy converge.
Inspired by:
- Musical traditions: Indian ragas, African drumming, Classical harmony
- Sacred spaces: Oracle of Delphi, Tibetan temples, Native American medicine wheels
- Modern vibes: Jazz improvisation, Electronic music flow states, Festival culture
- Pop culture: Woodstock's spirit, Pink Floyd's psychedelia, Bob Marley's unity
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import VibePepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class VibeTemple(Zone):
    """The Vibe Temple - Where energies harmonize and frequencies align."""
    
    def __init__(self):
        guide = VibePepe()
        super().__init__("Vibe Temple", guide)
        
        self.description = (
            "A crystalline temple where sacred geometries pulse with living light, "
            "reminiscent of the harmonic ratios in Indian classical music. Ethereal "
            "sounds weave through the air like the Oracle's prophetic vapors, while "
            "fractal patterns dance on the walls like a Grateful Dead light show. "
            "The space seems to breathe with the rhythm of tribal drums, as waves of "
            "pure vibrational energy flow like John Coltrane's sheets of sound."
        )
        
        self.dimension_weights = {
            ProfileDimension.HARMONY: 0.6,
            ProfileDimension.CREATIVITY: 0.5,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.4,
            ProfileDimension.PERCEPTION: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.HARMONY,
            ProfileDimension.CREATIVITY
        ]
        
        self.min_dimension_values = {
            ProfileDimension.HARMONY: 0.3,
            ProfileDimension.CREATIVITY: 0.3
        }
        
        self.setup_challenges()
        
        self.symbols = {
            "element": "Ether (Akashic Vibrations)",
            "color": "Prismatic (Aurora Borealis Spectrum)",
            "sefirot": SefirotAttribute.TIFERET,
            "animal": "Vibe Pepe (Dancing like Shiva Nataraja)",
            "mineral": "Singing Crystal (Tibetan Singing Bowl)",
            "cultural_elements": {
                "musical_traditions": [
                    "Indian Raga (Sacred Moods)",
                    "African Polyrhythms (Tribal Unity)",
                    "Gregorian Chants (Sacred Harmony)",
                    "Jazz Improvisation (Flow State)"
                ],
                "sacred_spaces": [
                    "Oracle's Chamber (Divine Inspiration)",
                    "Medicine Wheel (Natural Harmony)",
                    "Sound Temple (Acoustic Alchemy)",
                    "Festival Ground (Collective Joy)"
                ],
                "modern_interpretations": [
                    "Electronic Music Production",
                    "Sound Healing Therapy",
                    "Festival Culture Unity",
                    "Digital Audio Workstations"
                ]
            }
        }
        
    def setup_challenges(self) -> None:
        """Initialize the temple's challenge system."""
        self.challenges = {
            "frequency_flow": {
                "title": "The Harmonic Path (Inspired by Sacred Sound Traditions)",
                "description": "Attune yourself to the temple's vibrational frequencies.",
                "stages": [
                    "Root frequency grounding (Earth Drone)",
                    "Heart rhythm alignment (Sacred Pulse)",
                    "Crown chakra harmonization (Celestial Overtones)",
                    "Full spectrum resonance (Universal Harmony)"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.HARMONY: 0.1,
                    ProfileDimension.PERCEPTION: 0.1
                }
            },
            "vibe_synthesis": {
                "title": "The Mood Alchemist (Based on Classical Raga Theory)",
                "description": "Learn to blend and transform emotional frequencies.",
                "difficulty": 0.7,
                "exercises": [
                    "Morning raga attunement (Dawn Consciousness)",
                    "Afternoon energy flow (Solar Peak)",
                    "Evening tranquility weaving (Twilight Peace)"
                ],
                "rewards": {
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                    ProfileDimension.CREATIVITY: 0.2
                }
            },
            "resonance_mastery": {
                "title": "The Ultimate Vibe (Woodstock Meets Quantum Field)",
                "description": "Achieve perfect resonance with the universal frequency.",
                "options": {
                    "collective": {
                        "description": "Harmonize with the group consciousness (Festival Unity)",
                        "impact": {
                            ProfileDimension.HARMONY: 0.3,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.2
                        }
                    },
                    "individual": {
                        "description": "Perfect your unique frequency (Solo Jazz Journey)",
                        "impact": {
                            ProfileDimension.CREATIVITY: 0.2,
                            ProfileDimension.PERCEPTION: 0.2,
                            ProfileDimension.HARMONY: 0.1
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
                    content_id="frequency_flow",
                    content="The Harmonic Path: Attune yourself to the temple's vibrational frequencies.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.5,
                    creativity_required=0.3,
                    strategic_depth=0.4
                ),
                ContentItem(
                    content_id="vibe_synthesis",
                    content="The Mood Alchemist: Learn to blend and transform emotional frequencies.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.7,
                    creativity_required=0.5,
                    strategic_depth=0.6
                ),
                ContentItem(
                    content_id="resonance_mastery",
                    content="The Ultimate Vibe: Achieve perfect resonance with the universal frequency.",
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
            
            if interaction_type == "frequency_flow":
                # Validate frequency flow metadata
                if not isinstance(metadata.get('root_frequency'), (int, float)):
                    raise ValueError("frequency_flow requires 'root_frequency' number")
                if not isinstance(metadata.get('heart_rhythm', 0.5), (int, float)):
                    raise ValueError("heart_rhythm must be a number")
                    
                root_frequency = max(0.0, min(1.0, metadata.get('root_frequency', 0.5)))
                heart_rhythm = max(0.0, min(1.0, metadata.get('heart_rhythm', 0.5)))
                
                impacts[ProfileDimension.HARMONY] = 0.1 * root_frequency * heart_rhythm
                impacts[ProfileDimension.PERCEPTION] = 0.1 * heart_rhythm
                
            elif interaction_type == "vibe_synthesis":
                # Validate vibe synthesis metadata
                if not isinstance(metadata.get('morning_raga', 0.5), (int, float)):
                    raise ValueError("morning_raga must be a number")
                if not isinstance(metadata.get('afternoon_energy', 0.5), (int, float)):
                    raise ValueError("afternoon_energy must be a number")
                    
                morning_raga = max(0.0, min(1.0, metadata.get('morning_raga', 0.5)))
                afternoon_energy = max(0.0, min(1.0, metadata.get('afternoon_energy', 0.5)))
                
                impacts[ProfileDimension.EMOTIONAL_RESPONSE] = 0.1 * morning_raga
                impacts[ProfileDimension.CREATIVITY] = 0.1 * afternoon_energy
                
            elif interaction_type == "resonance_mastery":
                # Validate resonance mastery metadata
                if not isinstance(metadata.get('collective', 0.5), (int, float)):
                    raise ValueError("collective must be a number")
                if not isinstance(metadata.get('individual', 0.5), (int, float)):
                    raise ValueError("individual must be a number")
                    
                collective = max(0.0, min(1.0, metadata.get('collective', 0.5)))
                individual = max(0.0, min(1.0, metadata.get('individual', 0.5)))
                
                impacts[ProfileDimension.HARMONY] = 0.2 * collective
                impacts[ProfileDimension.EMOTIONAL_RESPONSE] = 0.1 * individual
                impacts[ProfileDimension.PERCEPTION] = 0.1 * (collective + individual) / 2
                
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