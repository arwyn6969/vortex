from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class VictoryPond(Zone):
    """The Victory Pond (Netzach) - The seventh sphere representing endurance and victory."""
    
    def __init__(self):
        # Initialize with Haniel as the guide (angel of Venus and victory)
        from ..guides.haniel import HanielGuide
        guide = HanielGuide()
        super().__init__("Pond of Victory", guide)
        
        self.description = "A pond of vibrant emerald green, pulsing with natural energy. The waters flow with eternal rhythms and the enduring power of life itself."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.PERSISTENCE: 0.7,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.5,
            ProfileDimension.CREATIVITY: 0.4,
            ProfileDimension.VITALITY: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.PERSISTENCE,
            ProfileDimension.EMOTIONAL_RESPONSE
        ]
        
        self.min_dimension_values = {
            ProfileDimension.PERSISTENCE: 0.4,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Fire/Water",
            "color": "Emerald Green",
            "sefirot": SefirotAttribute.NETZACH,
            "animal": "Dove",
            "mineral": "Emerald"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Victory Pond."""
        # Natural rhythm
        rhythm = LearningPathNode(
            node_id="victory_rhythm",
            content=ContentItem(
                content_id="natural_flow",
                content="Feel the eternal rhythms in the pond's green waters. "
                       "Let your energy align with nature's endless cycles.",
                dimension_weights={
                    ProfileDimension.VITALITY: 0.6,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.4
                },
                difficulty_level=0.4,
                emotional_intensity=0.5,
                creativity_required=0.3,
                strategic_depth=0.2
            ),
            required_dimensions={
                ProfileDimension.VITALITY: 0.3,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.3
            },
            next_nodes=["victory_endurance", "victory_nature"]
        )
        
        # Endurance development
        endurance = LearningPathNode(
            node_id="victory_endurance",
            content=ContentItem(
                content_id="lasting_power",
                content="Build your capacity for sustained effort. Let the pond's "
                       "eternal flow teach you the power of persistence.",
                dimension_weights={
                    ProfileDimension.PERSISTENCE: 0.8,
                    ProfileDimension.VITALITY: 0.2
                },
                difficulty_level=0.6,
                emotional_intensity=0.4,
                creativity_required=0.2,
                strategic_depth=0.5
            ),
            required_dimensions={
                ProfileDimension.PERSISTENCE: 0.5,
                ProfileDimension.VITALITY: 0.4
            },
            next_nodes=["victory_nature", "victory_mastery"]
        )
        
        # Nature connection
        nature = LearningPathNode(
            node_id="victory_nature",
            content=ContentItem(
                content_id="natural_harmony",
                content="Merge with the natural forces flowing through the pond. "
                       "Let your creativity dance with life's endless expressions.",
                dimension_weights={
                    ProfileDimension.CREATIVITY: 0.6,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.4
                },
                difficulty_level=0.7,
                emotional_intensity=0.7,
                creativity_required=0.6,
                strategic_depth=0.3
            ),
            required_dimensions={
                ProfileDimension.CREATIVITY: 0.5,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.5
            },
            next_nodes=["victory_mastery"]
        )
        
        # Victory mastery
        mastery = LearningPathNode(
            node_id="victory_mastery",
            content=ContentItem(
                content_id="eternal_victory",
                content="Embody the enduring power of natural forces. Let your "
                       "presence ripple with the eternal victory of life.",
                dimension_weights={
                    ProfileDimension.PERSISTENCE: 0.5,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.3,
                    ProfileDimension.CREATIVITY: 0.3,
                    ProfileDimension.VITALITY: 0.4
                },
                difficulty_level=0.9,
                emotional_intensity=0.8,
                creativity_required=0.7,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.PERSISTENCE: 0.7,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.6,
                ProfileDimension.CREATIVITY: 0.5
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [rhythm, endurance, nature, mastery]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        persistence = profile.get(ProfileDimension.PERSISTENCE, 0.0)
        emotional = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.0)
        
        if progress < 0.3:
            if persistence < emotional:
                return (
                    "Let the pond's eternal rhythms strengthen your resolve. "
                    "Victory comes to those who persist."
                )
            else:
                return (
                    "Your persistence is strong. Now learn to flow with the "
                    "natural cycles of effort and rest."
                )
        elif progress < 0.6:
            if persistence < 0.6:
                return (
                    "The pond's green waters teach endurance. Let your strength "
                    "grow like a mighty tree, steady and sure."
                )
            else:
                return (
                    "You have found your rhythm. Now learn to share your "
                    "strength with others through natural harmony."
                )
        elif progress < 0.9:
            return (
                "The pond's eternal power flows through you. Seek now to "
                "embody the endless victory of life itself."
            )
        else:
            return (
                "You have become one with Victory's eternal dance. Your presence "
                "here inspires others to find their enduring strength."
            ) 