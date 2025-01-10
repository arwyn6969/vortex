from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class KindnessPond(Zone):
    """The Pond of Kindness - A place of empathy and compassionate understanding."""
    
    def __init__(self):
        # Initialize with Hathor as the guide (Egyptian goddess of love and kindness)
        from ..guides.hathor import HathorGuide
        guide = HathorGuide()
        super().__init__("Pond of Kindness", guide)
        
        self.description = "A tranquil blue pond where ripples of compassion spread endlessly outward. Water lilies float on the surface, each one representing a different aspect of kindness."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.EMPATHY: 0.7,
            ProfileDimension.MORAL_ALIGNMENT: 0.3,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
            ProfileDimension.DECISION_MAKING: 0.1
        }
        
        self.required_dimensions = [
            ProfileDimension.EMPATHY,
            ProfileDimension.MORAL_ALIGNMENT
        ]
        
        self.min_dimension_values = {
            ProfileDimension.EMPATHY: 0.3,
            ProfileDimension.MORAL_ALIGNMENT: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Water",
            "color": "Blue",
            "sefirot": SefirotAttribute.CHESED,
            "animal": "Dove",
            "mineral": "Aquamarine"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Kindness Pond."""
        # Basic empathy exercise
        basic_empathy = LearningPathNode(
            node_id="kindness_basic_empathy",
            content=ContentItem(
                content_id="empathy_basics",
                content="Observe the water lilies and identify the emotions they "
                       "reflect. Each flower mirrors a different feeling.",
                dimension_weights={
                    ProfileDimension.EMPATHY: 0.7,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.3
                },
                difficulty_level=0.3,
                emotional_intensity=0.4,
                creativity_required=0.2,
                strategic_depth=0.1
            ),
            required_dimensions={
                ProfileDimension.EMPATHY: 0.2,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.2
            },
            next_nodes=["kindness_perspective", "kindness_helping"]
        )
        
        # Perspective taking challenge
        perspective_taking = LearningPathNode(
            node_id="kindness_perspective",
            content=ContentItem(
                content_id="perspective_challenge",
                content="Walk around the pond and view the same scene from different "
                       "angles. Notice how the reflections change with each perspective.",
                dimension_weights={
                    ProfileDimension.EMPATHY: 0.5,
                    ProfileDimension.PERCEPTION: 0.3,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.2
                },
                difficulty_level=0.5,
                emotional_intensity=0.6,
                creativity_required=0.4,
                strategic_depth=0.3
            ),
            required_dimensions={
                ProfileDimension.EMPATHY: 0.3,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.3
            },
            next_nodes=["kindness_helping", "kindness_moral_choice"]
        )
        
        # Helping hand challenge
        helping_hand = LearningPathNode(
            node_id="kindness_helping",
            content=ContentItem(
                content_id="helping_challenge",
                content="A water lily is trapped in a whirlpool. Find a way to free "
                       "it while ensuring other lilies aren't disturbed.",
                dimension_weights={
                    ProfileDimension.MORAL_ALIGNMENT: 0.4,
                    ProfileDimension.DECISION_MAKING: 0.3,
                    ProfileDimension.EMPATHY: 0.3
                },
                difficulty_level=0.6,
                emotional_intensity=0.5,
                creativity_required=0.6,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.MORAL_ALIGNMENT: 0.4,
                ProfileDimension.EMPATHY: 0.4
            },
            next_nodes=["kindness_moral_choice", "kindness_harmony"]
        )
        
        # Moral choice challenge
        moral_choice = LearningPathNode(
            node_id="kindness_moral_choice",
            content=ContentItem(
                content_id="moral_dilemma",
                content="Two lilies are wilting. You only have enough energy to save "
                       "one. The first supports many smaller buds, while the second "
                       "is the last of its rare kind.",
                dimension_weights={
                    ProfileDimension.MORAL_ALIGNMENT: 0.5,
                    ProfileDimension.DECISION_MAKING: 0.3,
                    ProfileDimension.EMPATHY: 0.2
                },
                difficulty_level=0.8,
                emotional_intensity=0.8,
                creativity_required=0.3,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.MORAL_ALIGNMENT: 0.5,
                ProfileDimension.EMPATHY: 0.5
            },
            next_nodes=["kindness_harmony"]
        )
        
        # Final harmony challenge
        harmony = LearningPathNode(
            node_id="kindness_harmony",
            content=ContentItem(
                content_id="kindness_harmony",
                content="Create a ripple pattern that brings joy to all the lilies "
                       "simultaneously, while maintaining the pond's delicate balance.",
                dimension_weights={
                    ProfileDimension.EMPATHY: 0.4,
                    ProfileDimension.MORAL_ALIGNMENT: 0.3,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.2,
                    ProfileDimension.DECISION_MAKING: 0.1
                },
                difficulty_level=0.9,
                emotional_intensity=0.9,
                creativity_required=0.7,
                strategic_depth=0.5
            ),
            required_dimensions={
                ProfileDimension.EMPATHY: 0.6,
                ProfileDimension.MORAL_ALIGNMENT: 0.6,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.5
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [
            basic_empathy,
            perspective_taking,
            helping_hand,
            moral_choice,
            harmony
        ]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        empathy = profile.get(ProfileDimension.EMPATHY, 0.0)
        moral = profile.get(ProfileDimension.MORAL_ALIGNMENT, 0.0)
        
        if progress < 0.3:
            if empathy < moral:
                return (
                    "Open your heart to the feelings reflected in the water. "
                    "Each ripple carries an emotion waiting to be understood."
                )
            else:
                return (
                    "Your empathy flows naturally. Now learn to channel it "
                    "into actions that benefit all."
                )
        elif progress < 0.6:
            if empathy < 0.6:
                return (
                    "The pond's waters mirror the depths of others' hearts. "
                    "Let their reflections deepen your understanding."
                )
            else:
                return (
                    "Your kindness creates beautiful patterns in the water. "
                    "Watch how your actions ripple outward, touching many lives."
                )
        elif progress < 0.9:
            return (
                "The pond's wisdom flows through your compassionate heart. "
                "Seek now to bring harmony to all who visit these waters."
            )
        else:
            return (
                "You have become one with the pond's boundless compassion. "
                "Your presence here now nurtures others in their journey."
            ) 