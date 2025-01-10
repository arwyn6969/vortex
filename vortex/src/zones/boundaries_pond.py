from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class BoundariesPond(Zone):
    """The Pond of Boundaries - A place of limits, protection, and balanced growth."""
    
    def __init__(self):
        # Initialize with Horus as the guide (Egyptian god of protection and boundaries)
        from ..guides.horus import HorusGuide
        guide = HorusGuide()
        super().__init__("Pond of Boundaries", guide)
        
        self.description = "A pond encircled by crystalline walls, its surface marked by intricate geometric patterns. The waters pulse with a steady rhythm, teaching the dance of limits and growth."
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.RISK_TOLERANCE: 0.5,
            ProfileDimension.DECISION_MAKING: 0.3,
            ProfileDimension.STRATEGIC_THINKING: 0.2,
            ProfileDimension.MORAL_ALIGNMENT: 0.1
        }
        
        self.required_dimensions = [
            ProfileDimension.RISK_TOLERANCE,
            ProfileDimension.DECISION_MAKING
        ]
        
        self.min_dimension_values = {
            ProfileDimension.RISK_TOLERANCE: 0.3,
            ProfileDimension.DECISION_MAKING: 0.3
        }
        
        # Symbolic associations
        self.symbols = {
            "element": "Earth",
            "color": "Green",
            "sefirot": SefirotAttribute.NETZACH,
            "animal": "Turtle",
            "mineral": "Emerald"
        }
        
    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Boundaries Pond."""
        # Basic boundaries awareness
        basic_boundaries = LearningPathNode(
            node_id="boundaries_basic",
            content=ContentItem(
                content_id="boundary_awareness",
                content="Observe the crystalline walls of the pond. Feel where they "
                       "are firm and where they might flex.",
                dimension_weights={
                    ProfileDimension.RISK_TOLERANCE: 0.6,
                    ProfileDimension.PERCEPTION: 0.4
                },
                difficulty_level=0.3,
                emotional_intensity=0.3,
                creativity_required=0.2,
                strategic_depth=0.4
            ),
            required_dimensions={
                ProfileDimension.RISK_TOLERANCE: 0.2,
                ProfileDimension.PERCEPTION: 0.2
            },
            next_nodes=["boundaries_testing", "boundaries_protection"]
        )
        
        # Boundary testing
        boundary_testing = LearningPathNode(
            node_id="boundaries_testing",
            content=ContentItem(
                content_id="testing_limits",
                content="Create gentle waves that test the pond's boundaries. "
                       "Learn where flexibility serves and where firmness protects.",
                dimension_weights={
                    ProfileDimension.RISK_TOLERANCE: 0.5,
                    ProfileDimension.STRATEGIC_THINKING: 0.3,
                    ProfileDimension.DECISION_MAKING: 0.2
                },
                difficulty_level=0.5,
                emotional_intensity=0.4,
                creativity_required=0.3,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.RISK_TOLERANCE: 0.4,
                ProfileDimension.STRATEGIC_THINKING: 0.3
            },
            next_nodes=["boundaries_protection", "boundaries_balance"]
        )
        
        # Protection challenge
        protection = LearningPathNode(
            node_id="boundaries_protection",
            content=ContentItem(
                content_id="protective_barrier",
                content="A storm approaches the pond. Create protective barriers that "
                       "shield without completely isolating.",
                dimension_weights={
                    ProfileDimension.DECISION_MAKING: 0.4,
                    ProfileDimension.RISK_TOLERANCE: 0.3,
                    ProfileDimension.STRATEGIC_THINKING: 0.3
                },
                difficulty_level=0.7,
                emotional_intensity=0.5,
                creativity_required=0.4,
                strategic_depth=0.7
            ),
            required_dimensions={
                ProfileDimension.DECISION_MAKING: 0.5,
                ProfileDimension.RISK_TOLERANCE: 0.4
            },
            next_nodes=["boundaries_balance", "boundaries_mastery"]
        )
        
        # Balance challenge
        balance = LearningPathNode(
            node_id="boundaries_balance",
            content=ContentItem(
                content_id="balance_challenge",
                content="The pond's waters rise and fall. Maintain healthy boundaries "
                       "while allowing necessary flow and exchange.",
                dimension_weights={
                    ProfileDimension.RISK_TOLERANCE: 0.4,
                    ProfileDimension.DECISION_MAKING: 0.3,
                    ProfileDimension.MORAL_ALIGNMENT: 0.3
                },
                difficulty_level=0.8,
                emotional_intensity=0.6,
                creativity_required=0.5,
                strategic_depth=0.7
            ),
            required_dimensions={
                ProfileDimension.RISK_TOLERANCE: 0.6,
                ProfileDimension.DECISION_MAKING: 0.5
            },
            next_nodes=["boundaries_mastery"]
        )
        
        # Mastery challenge
        mastery = LearningPathNode(
            node_id="boundaries_mastery",
            content=ContentItem(
                content_id="boundary_mastery",
                content="Orchestrate the perfect dance of boundaries - protecting "
                       "while nurturing, limiting while allowing growth.",
                dimension_weights={
                    ProfileDimension.RISK_TOLERANCE: 0.3,
                    ProfileDimension.DECISION_MAKING: 0.3,
                    ProfileDimension.STRATEGIC_THINKING: 0.2,
                    ProfileDimension.MORAL_ALIGNMENT: 0.2
                },
                difficulty_level=0.9,
                emotional_intensity=0.7,
                creativity_required=0.6,
                strategic_depth=0.8
            ),
            required_dimensions={
                ProfileDimension.RISK_TOLERANCE: 0.7,
                ProfileDimension.DECISION_MAKING: 0.6,
                ProfileDimension.STRATEGIC_THINKING: 0.5
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [
            basic_boundaries,
            boundary_testing,
            protection,
            balance,
            mastery
        ]:
            self.learning_path.add_node(node)
            
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        risk = profile.get(ProfileDimension.RISK_TOLERANCE, 0.0)
        decision = profile.get(ProfileDimension.DECISION_MAKING, 0.0)
        
        if progress < 0.3:
            if risk < decision:
                return (
                    "Feel the strength in the pond's crystal walls. "
                    "They teach us when to hold firm and when to yield."
                )
            else:
                return (
                    "You understand risk well. Now learn to set boundaries "
                    "that protect while allowing connection."
                )
        elif progress < 0.6:
            if risk < 0.6:
                return (
                    "The pond's patterns reveal the wisdom of limits. "
                    "Study where flexibility serves and where firmness protects."
                )
            else:
                return (
                    "Your boundaries show wisdom. Now learn to maintain them "
                    "while fostering growth and connection."
                )
        elif progress < 0.9:
            return (
                "The pond's protective wisdom flows through you. "
                "Seek now the perfect balance of strength and openness."
            )
        else:
            return (
                "You have become one with the pond's protective essence. "
                "Your presence here now guides others in finding their own boundaries."
            ) 