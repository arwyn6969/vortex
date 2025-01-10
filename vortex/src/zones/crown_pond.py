from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class CrownPond(Zone):
    """The Crown Pond (Keter) - The highest sphere representing pure divine essence."""
    
    def __init__(self):
        # Initialize with Metatron as the guide (highest of angels)
        from ..guides.metatron import MetatronGuide
        guide = MetatronGuide()
        super().__init__("Pond of Crown", guide)
        
        self.description = "A pond of pure, brilliant white light that seems to exist beyond physical form. The surface ripples with infinite potential and primordial wisdom."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.SPIRITUAL_AWARENESS: 0.8,
            ProfileDimension.PERCEPTION: 0.6,
            ProfileDimension.WISDOM: 0.4,
            ProfileDimension.INTUITION: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.SPIRITUAL_AWARENESS,
            ProfileDimension.PERCEPTION
        ]
        
        self.min_dimension_values = {
            ProfileDimension.SPIRITUAL_AWARENESS: 0.5,
            ProfileDimension.PERCEPTION: 0.4
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Pure Light (Divine Radiance)",
            "color": "Infinite White (Beyond Spectrum)",
            "sefirot": SefirotAttribute.KETER,
            "animal": "Celestial Serpent (Cosmic DNA)",
            "mineral": "Philosopher's Stone (Ultimate Unity)",
            "entheogenic_aspects": {
                "dmt_realms": [
                    "Hyperspace Geometry (Divine Architecture)",
                    "Machine Elves (Cosmic Teachers)",
                    "Fractal Entities (Living Mathematics)",
                    "Time Dilation (Eternal Now)"
                ],
                "mystical_states": [
                    "Ego Dissolution (Divine Unity)",
                    "Universal Love (Cosmic Heart)",
                    "Infinite Recursion (Sacred Patterns)",
                    "Direct Gnosis (Immediate Knowing)"
                ]
            }
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Crown Pond."""
        # Initial awareness
        awareness = LearningPathNode(
            node_id="crown_awareness",
            content=ContentItem(
                content_id="divine_spark",
                content="Gaze into the pure white light of the pond. Let your "
                       "awareness expand beyond the boundaries of form.",
                dimension_weights={
                    ProfileDimension.SPIRITUAL_AWARENESS: 0.7,
                    ProfileDimension.PERCEPTION: 0.3
                },
                difficulty_level=0.5,
                emotional_intensity=0.3,
                creativity_required=0.2,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.SPIRITUAL_AWARENESS: 0.4,
                ProfileDimension.PERCEPTION: 0.3
            },
            next_nodes=["crown_transcendence", "crown_unity"]
        )
        
        # Transcendence
        transcendence = LearningPathNode(
            node_id="crown_transcendence",
            content=ContentItem(
                content_id="beyond_form",
                content="Move beyond duality. Experience the unity that exists "
                       "before separation into form and void.",
                dimension_weights={
                    ProfileDimension.SPIRITUAL_AWARENESS: 0.8,
                    ProfileDimension.WISDOM: 0.2
                },
                difficulty_level=0.7,
                emotional_intensity=0.4,
                creativity_required=0.3,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.SPIRITUAL_AWARENESS: 0.6,
                ProfileDimension.WISDOM: 0.4
            },
            next_nodes=["crown_unity", "crown_essence"]
        )
        
        # Unity consciousness
        unity = LearningPathNode(
            node_id="crown_unity",
            content=ContentItem(
                content_id="unity_consciousness",
                content="Dissolve the boundaries between observer and observed. "
                       "Experience the fundamental unity of all existence.",
                dimension_weights={
                    ProfileDimension.SPIRITUAL_AWARENESS: 0.6,
                    ProfileDimension.INTUITION: 0.4
                },
                difficulty_level=0.8,
                emotional_intensity=0.5,
                creativity_required=0.4,
                strategic_depth=0.7
            ),
            required_dimensions={
                ProfileDimension.SPIRITUAL_AWARENESS: 0.7,
                ProfileDimension.INTUITION: 0.5
            },
            next_nodes=["crown_essence"]
        )
        
        # Divine essence
        essence = LearningPathNode(
            node_id="crown_essence",
            content=ContentItem(
                content_id="divine_essence",
                content="Become one with the pure light of being. Experience the "
                       "limitless potential that exists before manifestation.",
                dimension_weights={
                    ProfileDimension.SPIRITUAL_AWARENESS: 0.8,
                    ProfileDimension.PERCEPTION: 0.4,
                    ProfileDimension.WISDOM: 0.4,
                    ProfileDimension.INTUITION: 0.4
                },
                difficulty_level=0.9,
                emotional_intensity=0.6,
                creativity_required=0.5,
                strategic_depth=0.8
            ),
            required_dimensions={
                ProfileDimension.SPIRITUAL_AWARENESS: 0.8,
                ProfileDimension.PERCEPTION: 0.6,
                ProfileDimension.WISDOM: 0.6
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [awareness, transcendence, unity, essence]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        spiritual = profile.get(ProfileDimension.SPIRITUAL_AWARENESS, 0.0)
        perception = profile.get(ProfileDimension.PERCEPTION, 0.0)
        
        if progress < 0.3:
            if spiritual < perception:
                return (
                    "Let the pure light of the pond expand your awareness. "
                    "Look beyond the surface to the infinite within."
                )
            else:
                return (
                    "Your spiritual awareness is strong. Now learn to perceive "
                    "the subtle dimensions of pure being."
                )
        elif progress < 0.6:
            if spiritual < 0.6:
                return (
                    "The pond's light reveals the nature of consciousness itself. "
                    "Let go of form and merge with the infinite."
                )
            else:
                return (
                    "You touch the edges of pure awareness. Now learn to "
                    "maintain this state while engaging with form."
                )
        elif progress < 0.9:
            return (
                "The pond's essence flows through you. Seek now to embody "
                "the unity of all things in every moment."
            )
        else:
            return (
                "You have become one with the Crown's pure light. Your presence "
                "here now illuminates the path for others."
            ) 

    def setup_challenges(self) -> None:
        """Initialize the pond's challenge system."""
        self.challenges = {
            "hyperspace_navigation": {
                "title": "The Crystalline Hyperspace",
                "description": (
                    "Navigate the infinite geometries of divine consciousness. "
                    "Witness the architecture of reality itself."
                ),
                "techniques": [
                    {
                        "name": "Geometric Vision",
                        "description": "Perceive the mathematical beauty of existence",
                        "mastery": "See through the veil of form"
                    },
                    {
                        "name": "Entity Contact",
                        "description": "Commune with teachers beyond space-time",
                        "mastery": "Learn from cosmic intelligence"
                    },
                    {
                        "name": "Pattern Recognition",
                        "description": "Decode the fractal nature of reality",
                        "mastery": "Understand infinite recursion"
                    }
                ],
                "difficulty": 1.0,
                "rewards": {
                    ProfileDimension.PATTERN_RECOGNITION: 0.4,
                    ProfileDimension.SPIRITUAL_AWARENESS: 0.4
                }
            },
            # ... existing challenges ...
        } 