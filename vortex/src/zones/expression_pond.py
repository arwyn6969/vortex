from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class ExpressionPond(Zone):
    """The Pond of Expression - A place of creativity and emotional authenticity."""
    
    def __init__(self):
        # Initialize with Thoth as the guide (Egyptian god of creative expression)
        from ..guides.thoth import ThothGuide
        guide = ThothGuide()
        super().__init__("Pond of Expression", guide)
        
        self.description = "A vibrant pond where flames dance upon the surface, each one a different color. The waters shimmer with creative energy, inviting authentic expression."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.CREATIVITY: 0.6,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.4,
            ProfileDimension.EMPATHY: 0.2,
            ProfileDimension.PERCEPTION: 0.1
        }
        
        self.required_dimensions = [
            ProfileDimension.CREATIVITY,
            ProfileDimension.EMOTIONAL_RESPONSE
        ]
        
        self.min_dimension_values = {
            ProfileDimension.CREATIVITY: 0.3,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Fire",
            "color": "Red",
            "sefirot": SefirotAttribute.GEVURAH,
            "animal": "Phoenix",
            "mineral": "Ruby"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Expression Pond."""
        # Basic creative expression
        basic_expression = LearningPathNode(
            node_id="expression_basic",
            content=ContentItem(
                content_id="creative_spark",
                content="Touch the surface of the pond and watch the colors respond "
                       "to your emotions. Let your feelings guide the patterns.",
                dimension_weights={
                    ProfileDimension.CREATIVITY: 0.5,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.5
                },
                difficulty_level=0.3,
                emotional_intensity=0.5,
                creativity_required=0.4,
                strategic_depth=0.1
            ),
            required_dimensions={
                ProfileDimension.CREATIVITY: 0.2,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.2
            },
            next_nodes=["expression_emotional_depth", "expression_creative_flow"]
        )
        
        # Emotional depth exploration
        emotional_depth = LearningPathNode(
            node_id="expression_emotional_depth",
            content=ContentItem(
                content_id="emotional_journey",
                content="Dive beneath the surface to explore the deeper currents "
                       "of emotion. Each layer reveals new aspects of feeling.",
                dimension_weights={
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.7,
                    ProfileDimension.EMPATHY: 0.3
                },
                difficulty_level=0.5,
                emotional_intensity=0.8,
                creativity_required=0.3,
                strategic_depth=0.2
            ),
            required_dimensions={
                ProfileDimension.EMOTIONAL_RESPONSE: 0.4,
                ProfileDimension.EMPATHY: 0.3
            },
            next_nodes=["expression_creative_flow", "expression_resonance"]
        )
        
        # Creative flow state
        creative_flow = LearningPathNode(
            node_id="expression_creative_flow",
            content=ContentItem(
                content_id="flow_state",
                content="Shape the dancing flames into forms that express your inner "
                       "vision. Let your creativity flow without judgment.",
                dimension_weights={
                    ProfileDimension.CREATIVITY: 0.8,
                    ProfileDimension.PERCEPTION: 0.2
                },
                difficulty_level=0.6,
                emotional_intensity=0.4,
                creativity_required=0.7,
                strategic_depth=0.3
            ),
            required_dimensions={
                ProfileDimension.CREATIVITY: 0.5,
                ProfileDimension.PERCEPTION: 0.3
            },
            next_nodes=["expression_resonance", "expression_mastery"]
        )
        
        # Emotional resonance
        emotional_resonance = LearningPathNode(
            node_id="expression_resonance",
            content=ContentItem(
                content_id="resonance_challenge",
                content="Create patterns that resonate with others' emotions while "
                       "maintaining your authentic expression.",
                dimension_weights={
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.4,
                    ProfileDimension.EMPATHY: 0.3,
                    ProfileDimension.CREATIVITY: 0.3
                },
                difficulty_level=0.7,
                emotional_intensity=0.8,
                creativity_required=0.6,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.EMOTIONAL_RESPONSE: 0.5,
                ProfileDimension.EMPATHY: 0.4
            },
            next_nodes=["expression_mastery"]
        )
        
        # Creative mastery
        creative_mastery = LearningPathNode(
            node_id="expression_mastery",
            content=ContentItem(
                content_id="creative_mastery",
                content="Orchestrate a symphony of flames and colors that expresses "
                       "complex emotional truths while inspiring others.",
                dimension_weights={
                    ProfileDimension.CREATIVITY: 0.4,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.3,
                    ProfileDimension.EMPATHY: 0.2,
                    ProfileDimension.PERCEPTION: 0.1
                },
                difficulty_level=0.9,
                emotional_intensity=0.9,
                creativity_required=0.9,
                strategic_depth=0.5
            ),
            required_dimensions={
                ProfileDimension.CREATIVITY: 0.7,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.6,
                ProfileDimension.EMPATHY: 0.5
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [
            basic_expression,
            emotional_depth,
            creative_flow,
            emotional_resonance,
            creative_mastery
        ]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        creativity = profile.get(ProfileDimension.CREATIVITY, 0.0)
        emotional = profile.get(ProfileDimension.EMOTIONAL_RESPONSE, 0.0)
        
        if progress < 0.3:
            if creativity < emotional:
                return (
                    "Let the dancing flames inspire your creative spirit. "
                    "Each color is a brush waiting for your unique touch."
                )
            else:
                return (
                    "Your creativity flows freely. Now learn to infuse it "
                    "with the depth of authentic emotion."
                )
        elif progress < 0.6:
            if creativity < 0.6:
                return (
                    "The pond's flames reveal new possibilities. "
                    "Trust your vision and let it guide your expression."
                )
            else:
                return (
                    "Your artistry creates mesmerizing patterns. "
                    "Now learn to touch others' hearts with your creations."
                )
        elif progress < 0.9:
            return (
                "The pond's creative fire flows through you. "
                "Seek now to inspire others with your authentic expression."
            )
        else:
            return (
                "You have become one with the pond's creative essence. "
                "Your presence here now ignites the artistic spirit in others."
            ) 