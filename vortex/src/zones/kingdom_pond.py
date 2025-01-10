from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class KingdomPond(Zone):
    """The Kingdom Pond (Malkhut) - The tenth sphere representing physical manifestation and earthly presence."""
    
    def __init__(self):
        # Initialize with Sandalphon as the guide (angel of Earth and manifestation)
        from ..guides.sandalphon import SandalphonGuide
        guide = SandalphonGuide()
        super().__init__("Pond of Kingdom", guide)
        
        self.description = "A pond of deep russet-brown, its waters rich with the essence of earth. Crystal formations line its edges, and its surface reflects the material world in perfect detail."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.MANIFESTATION: 0.7,
            ProfileDimension.PRACTICALITY: 0.6,
            ProfileDimension.STABILITY: 0.4,
            ProfileDimension.GROUNDEDNESS: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.MANIFESTATION,
            ProfileDimension.PRACTICALITY
        ]
        
        self.min_dimension_values = {
            ProfileDimension.MANIFESTATION: 0.4,
            ProfileDimension.PRACTICALITY: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Earth",
            "color": "Russet Brown",
            "sefirot": SefirotAttribute.MALKHUT,
            "animal": "Snake",
            "mineral": "Rock Crystal"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Kingdom Pond."""
        # Physical awareness
        awareness = LearningPathNode(
            node_id="kingdom_awareness",
            content=ContentItem(
                content_id="earth_connection",
                content="Feel the solid presence of the earth in these waters. "
                       "Let your awareness ground itself in physical reality.",
                dimension_weights={
                    ProfileDimension.GROUNDEDNESS: 0.7,
                    ProfileDimension.STABILITY: 0.3
                },
                difficulty_level=0.4,
                emotional_intensity=0.3,
                creativity_required=0.2,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.GROUNDEDNESS: 0.3,
                ProfileDimension.STABILITY: 0.3
            },
            next_nodes=["kingdom_practicality", "kingdom_manifestation"]
        )
        
        # Practical wisdom
        practicality = LearningPathNode(
            node_id="kingdom_practicality",
            content=ContentItem(
                content_id="practical_wisdom",
                content="Learn to apply higher wisdom in practical ways. Let the "
                       "pond's earthly nature teach you effective action.",
                dimension_weights={
                    ProfileDimension.PRACTICALITY: 0.8,
                    ProfileDimension.STABILITY: 0.2
                },
                difficulty_level=0.6,
                emotional_intensity=0.4,
                creativity_required=0.3,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.PRACTICALITY: 0.5,
                ProfileDimension.STABILITY: 0.4
            },
            next_nodes=["kingdom_manifestation", "kingdom_mastery"]
        )
        
        # Manifestation power
        manifestation = LearningPathNode(
            node_id="kingdom_manifestation",
            content=ContentItem(
                content_id="manifest_power",
                content="Develop your power to manifest change in the physical "
                       "world. Let the pond's crystalline edges guide your will.",
                dimension_weights={
                    ProfileDimension.MANIFESTATION: 0.7,
                    ProfileDimension.PRACTICALITY: 0.3
                },
                difficulty_level=0.7,
                emotional_intensity=0.5,
                creativity_required=0.4,
                strategic_depth=0.7
            ),
            required_dimensions={
                ProfileDimension.MANIFESTATION: 0.6,
                ProfileDimension.PRACTICALITY: 0.5
            },
            next_nodes=["kingdom_mastery"]
        )
        
        # Kingdom mastery
        mastery = LearningPathNode(
            node_id="kingdom_mastery",
            content=ContentItem(
                content_id="earthly_mastery",
                content="Embody the perfect balance of spirit and matter. Let your "
                       "presence manifest divine will in physical form.",
                dimension_weights={
                    ProfileDimension.MANIFESTATION: 0.4,
                    ProfileDimension.PRACTICALITY: 0.3,
                    ProfileDimension.STABILITY: 0.3,
                    ProfileDimension.GROUNDEDNESS: 0.3
                },
                difficulty_level=0.9,
                emotional_intensity=0.6,
                creativity_required=0.5,
                strategic_depth=0.8
            ),
            required_dimensions={
                ProfileDimension.MANIFESTATION: 0.7,
                ProfileDimension.PRACTICALITY: 0.6,
                ProfileDimension.STABILITY: 0.6
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [awareness, practicality, manifestation, mastery]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        manifestation = profile.get(ProfileDimension.MANIFESTATION, 0.0)
        practicality = profile.get(ProfileDimension.PRACTICALITY, 0.0)
        
        if progress < 0.3:
            if manifestation < practicality:
                return (
                    "Let the pond's earthly essence strengthen your ability to "
                    "manifest. Each crystal holds a key to physical creation."
                )
            else:
                return (
                    "Your manifestation power is strong. Now learn to ground it "
                    "in practical, effective action."
                )
        elif progress < 0.6:
            if manifestation < 0.6:
                return (
                    "The pond's crystalline wisdom guides your hands. Let your "
                    "will shape the physical world with growing skill."
                )
            else:
                return (
                    "You manifest well. Now learn to sustain and stabilize "
                    "your creations in the material realm."
                )
        elif progress < 0.9:
            return (
                "The pond's earthly power flows through you. Seek now to "
                "become a perfect channel for divine will in action."
            )
        else:
            return (
                "You have become one with Kingdom's manifesting power. Your "
                "presence here now helps others ground spirit in matter."
            ) 