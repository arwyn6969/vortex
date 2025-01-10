"""
Understanding Pond (Binah) - The third Sefirot, representing deep comprehension and analysis.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class UnderstandingPond(Zone):
    """The Pond of Understanding - A place of deep comprehension and wisdom sharing."""
    
    def __init__(self):
        # Initialize with Isis as the guide (Egyptian goddess of wisdom and knowledge)
        from ..guides.isis import IsisGuide
        guide = IsisGuide()
        super().__init__("Pond of Understanding", guide)
        
        self.description = "A deep purple pond whose waters seem to hold infinite depths. Ancient symbols float beneath the surface, their meanings shifting and interweaving like living thoughts."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.COMPREHENSION: 0.5,
            ProfileDimension.EMPATHY: 0.3,
            ProfileDimension.PATTERN_RECOGNITION: 0.2,
            ProfileDimension.ANALYTICAL_THINKING: 0.2
        }
        
        self.required_dimensions = [
            ProfileDimension.COMPREHENSION,
            ProfileDimension.EMPATHY
        ]
        
        self.min_dimension_values = {
            ProfileDimension.COMPREHENSION: 0.3,
            ProfileDimension.EMPATHY: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Spirit",
            "color": "Purple",
            "sefirot": SefirotAttribute.BINAH,
            "animal": "Owl",
            "mineral": "Amethyst"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Understanding Pond."""
        # Basic comprehension
        basic_comprehension = LearningPathNode(
            node_id="understanding_basic",
            content=ContentItem(
                content_id="basic_understanding",
                content="Gaze into the pond's depths and identify the simplest "
                       "symbols. Let their meanings surface naturally.",
                dimension_weights={
                    ProfileDimension.COMPREHENSION: 0.6,
                    ProfileDimension.PATTERN_RECOGNITION: 0.4
                },
                difficulty_level=0.3,
                emotional_intensity=0.2,
                creativity_required=0.3,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.COMPREHENSION: 0.2,
                ProfileDimension.PATTERN_RECOGNITION: 0.2
            },
            next_nodes=["understanding_patterns", "understanding_empathy"]
        )
        
        # Pattern recognition
        pattern_recognition = LearningPathNode(
            node_id="understanding_patterns",
            content=ContentItem(
                content_id="pattern_insight",
                content="The symbols begin to dance and connect. Discover the "
                       "patterns that link seemingly disparate concepts.",
                dimension_weights={
                    ProfileDimension.PATTERN_RECOGNITION: 0.5,
                    ProfileDimension.ANALYTICAL_THINKING: 0.3,
                    ProfileDimension.COMPREHENSION: 0.2
                },
                difficulty_level=0.5,
                emotional_intensity=0.3,
                creativity_required=0.4,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.PATTERN_RECOGNITION: 0.3,
                ProfileDimension.COMPREHENSION: 0.3
            },
            next_nodes=["understanding_empathy", "understanding_synthesis"]
        )
        
        # Empathetic understanding
        empathetic_understanding = LearningPathNode(
            node_id="understanding_empathy",
            content=ContentItem(
                content_id="empathetic_insight",
                content="Feel how each symbol resonates with different emotions "
                       "and experiences. Understanding flows through connection.",
                dimension_weights={
                    ProfileDimension.EMPATHY: 0.5,
                    ProfileDimension.COMPREHENSION: 0.3,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.2
                },
                difficulty_level=0.6,
                emotional_intensity=0.7,
                creativity_required=0.3,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.EMPATHY: 0.4,
                ProfileDimension.COMPREHENSION: 0.4
            },
            next_nodes=["understanding_synthesis", "understanding_teaching"]
        )
        
        # Synthesis challenge
        synthesis = LearningPathNode(
            node_id="understanding_synthesis",
            content=ContentItem(
                content_id="synthesis_challenge",
                content="Weave together patterns, emotions, and insights into a "
                       "coherent tapestry of understanding.",
                dimension_weights={
                    ProfileDimension.COMPREHENSION: 0.4,
                    ProfileDimension.PATTERN_RECOGNITION: 0.3,
                    ProfileDimension.ANALYTICAL_THINKING: 0.3
                },
                difficulty_level=0.8,
                emotional_intensity=0.5,
                creativity_required=0.6,
                strategic_depth=0.7
            ),
            required_dimensions={
                ProfileDimension.COMPREHENSION: 0.5,
                ProfileDimension.PATTERN_RECOGNITION: 0.4
            },
            next_nodes=["understanding_teaching"]
        )
        
        # Teaching challenge
        teaching = LearningPathNode(
            node_id="understanding_teaching",
            content=ContentItem(
                content_id="teaching_mastery",
                content="Guide others to their own understanding, adapting your "
                       "approach to their unique way of learning.",
                dimension_weights={
                    ProfileDimension.COMPREHENSION: 0.3,
                    ProfileDimension.EMPATHY: 0.3,
                    ProfileDimension.PATTERN_RECOGNITION: 0.2,
                    ProfileDimension.ANALYTICAL_THINKING: 0.2
                },
                difficulty_level=0.9,
                emotional_intensity=0.8,
                creativity_required=0.7,
                strategic_depth=0.8
            ),
            required_dimensions={
                ProfileDimension.COMPREHENSION: 0.7,
                ProfileDimension.EMPATHY: 0.6,
                ProfileDimension.PATTERN_RECOGNITION: 0.5
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [
            basic_comprehension,
            pattern_recognition,
            empathetic_understanding,
            synthesis,
            teaching
        ]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        comprehension = profile.get(ProfileDimension.COMPREHENSION, 0.0)
        empathy = profile.get(ProfileDimension.EMPATHY, 0.0)
        
        if progress < 0.3:
            if comprehension < empathy:
                return (
                    "Let the symbols speak to your mind. "
                    "Each one holds a truth waiting to be understood."
                )
            else:
                return (
                    "Your mind grasps concepts well. Now learn to feel "
                    "the deeper resonance of understanding."
                )
        elif progress < 0.6:
            if comprehension < 0.6:
                return (
                    "The pond's depths reveal new layers of meaning. "
                    "Let each insight build upon the last."
                )
            else:
                return (
                    "Your understanding grows deep. Now learn to share "
                    "these insights in ways others can grasp."
                )
        elif progress < 0.9:
            return (
                "The pond's wisdom illuminates your mind and heart. "
                "Seek now to bridge understanding between all seekers."
            )
        else:
            return (
                "You have become one with the pond's infinite understanding. "
                "Your presence here now lights the path for others."
            )
``` 