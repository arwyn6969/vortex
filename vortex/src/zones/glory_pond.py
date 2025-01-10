from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class GloryPond(Zone):
    """The Glory Pond (Hod) - The eighth sphere representing intellectual splendor and form."""
    
    def __init__(self):
        # Initialize with Michael as the guide (angel of Mercury and divine glory)
        from ..guides.michael import MichaelGuide
        guide = MichaelGuide()
        super().__init__("Pond of Glory", guide)
        
        self.description = "A pond of shimmering orange-gold, its surface inscribed with ever-shifting patterns of sacred geometry. The waters resonate with divine order and intellectual brilliance."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.INTELLECT: 0.7,
            ProfileDimension.COMMUNICATION: 0.6,
            ProfileDimension.PERCEPTION: 0.4,
            ProfileDimension.ANALYSIS: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.INTELLECT,
            ProfileDimension.COMMUNICATION
        ]
        
        self.min_dimension_values = {
            ProfileDimension.INTELLECT: 0.4,
            ProfileDimension.COMMUNICATION: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Water/Fire",
            "color": "Orange",
            "sefirot": SefirotAttribute.HOD,
            "animal": "Phoenix",
            "mineral": "Opal"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Glory Pond."""
        # Sacred patterns
        patterns = LearningPathNode(
            node_id="glory_patterns",
            content=ContentItem(
                content_id="sacred_geometry",
                content="Study the geometric patterns on the pond's surface. "
                       "Let your mind grasp the language of divine form.",
                dimension_weights={
                    ProfileDimension.PERCEPTION: 0.6,
                    ProfileDimension.ANALYSIS: 0.4
                },
                difficulty_level=0.4,
                emotional_intensity=0.3,
                creativity_required=0.2,
                strategic_depth=0.5
            ),
            required_dimensions={
                ProfileDimension.PERCEPTION: 0.3,
                ProfileDimension.ANALYSIS: 0.3
            },
            next_nodes=["glory_communication", "glory_intellect"]
        )
        
        # Divine communication
        communication = LearningPathNode(
            node_id="glory_communication",
            content=ContentItem(
                content_id="sacred_speech",
                content="Learn to articulate divine truths with precision. Let the "
                       "pond's resonance guide your words with power and grace.",
                dimension_weights={
                    ProfileDimension.COMMUNICATION: 0.8,
                    ProfileDimension.INTELLECT: 0.2
                },
                difficulty_level=0.6,
                emotional_intensity=0.4,
                creativity_required=0.3,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.COMMUNICATION: 0.5,
                ProfileDimension.INTELLECT: 0.4
            },
            next_nodes=["glory_intellect", "glory_mastery"]
        )
        
        # Intellectual splendor
        intellect = LearningPathNode(
            node_id="glory_intellect",
            content=ContentItem(
                content_id="divine_intellect",
                content="Engage with the pond's intellectual radiance. Let your "
                       "mind expand to embrace higher forms of understanding.",
                dimension_weights={
                    ProfileDimension.INTELLECT: 0.7,
                    ProfileDimension.ANALYSIS: 0.3
                },
                difficulty_level=0.7,
                emotional_intensity=0.3,
                creativity_required=0.4,
                strategic_depth=0.8
            ),
            required_dimensions={
                ProfileDimension.INTELLECT: 0.6,
                ProfileDimension.ANALYSIS: 0.5
            },
            next_nodes=["glory_mastery"]
        )
        
        # Glory mastery
        mastery = LearningPathNode(
            node_id="glory_mastery",
            content=ContentItem(
                content_id="divine_glory",
                content="Embody the splendor of divine intellect. Let your presence "
                       "radiate with the glory of perfect understanding.",
                dimension_weights={
                    ProfileDimension.INTELLECT: 0.4,
                    ProfileDimension.COMMUNICATION: 0.3,
                    ProfileDimension.PERCEPTION: 0.3,
                    ProfileDimension.ANALYSIS: 0.3
                },
                difficulty_level=0.9,
                emotional_intensity=0.5,
                creativity_required=0.5,
                strategic_depth=0.9
            ),
            required_dimensions={
                ProfileDimension.INTELLECT: 0.7,
                ProfileDimension.COMMUNICATION: 0.6,
                ProfileDimension.ANALYSIS: 0.6
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [patterns, communication, intellect, mastery]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        intellect = profile.get(ProfileDimension.INTELLECT, 0.0)
        communication = profile.get(ProfileDimension.COMMUNICATION, 0.0)
        
        if progress < 0.3:
            if intellect < communication:
                return (
                    "Let the pond's sacred patterns expand your understanding. "
                    "Each ripple contains a lesson in divine order."
                )
            else:
                return (
                    "Your intellect is sharp. Now learn to communicate these "
                    "truths with clarity and grace."
                )
        elif progress < 0.6:
            if intellect < 0.6:
                return (
                    "The pond's wisdom deepens your comprehension. Let your mind "
                    "grasp ever more subtle forms of truth."
                )
            else:
                return (
                    "You grasp the patterns well. Now learn to share these "
                    "insights in ways that illuminate others."
                )
        elif progress < 0.9:
            return (
                "The pond's glory shines through your understanding. Seek now "
                "to embody the perfect balance of wisdom and expression."
            )
        else:
            return (
                "You have become one with Glory's divine light. Your presence "
                "here now helps others perceive higher truths."
            ) 