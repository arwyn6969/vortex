"""
Mercy Pond (Chesed) - The fourth Sefirot, representing loving-kindness and compassion.
Inspired by:
- Ancient wisdom: Egyptian Ma'at, Buddhist Metta, Christian Agape
- Modern psychology: Compassion-focused therapy, emotional intelligence
- Cultural elements: Healing waters, sacred lotus
- Philosophical concepts: Ethics of care, moral philosophy
"""
from typing import Dict, List, Optional, Any
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode
import logging
from ..core.exceptions import GuidanceError

logger = logging.getLogger(__name__)

class MercyPond(Zone):
    """The Pond of Mercy - A place of compassion, kindness, and benevolent action."""
    
    def __init__(self):
        # Initialize with Ma'at as the guide (Egyptian goddess of truth, justice, and harmony)
        from ..guides.maat import MaatGuide
        guide = MaatGuide()
        super().__init__("Pond of Mercy", guide)
        
        self.description = (
            "A radiant pool of silver-blue water, its surface perfectly still yet "
            "somehow flowing with gentle currents. White lotus flowers float serenely "
            "on the surface, their petals occasionally opening to reveal soft light. "
            "The air carries whispers of ancient healing traditions, from Egyptian "
            "temples to Buddhist sanctuaries. Around the pond's edge, crystals pulse "
            "with healing energy, their light synchronized with the lotus blooms."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.EMPATHY: 0.6,
            ProfileDimension.COMPASSION: 0.5,
            ProfileDimension.WISDOM: 0.3,
            ProfileDimension.HARMONY: 0.4,
            ProfileDimension.EMOTIONAL_INTELLIGENCE: 0.4,
            ProfileDimension.HEALING: 0.5
        }
        
        self.required_dimensions = [
            ProfileDimension.EMPATHY,
            ProfileDimension.COMPASSION
        ]
        
        self.min_dimension_values = {
            ProfileDimension.EMPATHY: 0.3,
            ProfileDimension.COMPASSION: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations with expanded cultural elements
        self.symbols = {
            "element": "Water",
            "color": "Blue",
            "sefirot": SefirotAttribute.CHESED,
            "animal": "Swan",
            "mineral": "Sapphire",
            "cultural_elements": {
                "wisdom_traditions": [
                    "Egyptian Ma'at (Divine Order)",
                    "Buddhist Metta (Loving-kindness)",
                    "Christian Agape (Divine Love)",
                    "Jewish Chesed (Loving-kindness)"
                ],
                "modern_interpretations": [
                    "Compassion-focused Therapy",
                    "Emotional Intelligence",
                    "Positive Psychology",
                    "Mindfulness Practice"
                ],
                "healing_practices": [
                    "Energy Healing",
                    "Sound Therapy",
                    "Crystal Healing",
                    "Meditation"
                ]
            },
            "sacred_geometry": {
                "form": "Circle",
                "meaning": "Wholeness and Unity",
                "manifestation": "Ripples of Healing"
            }
        }
        
        # Initialize learning paths
        self.setup_learning_paths()
        
    def setup_learning_paths(self) -> None:
        """Initialize adaptive learning paths for the zone."""
        self.learning_paths = {
            "compassion_mastery": {
                "nodes": [
                    LearningPathNode(
                        id="basic_empathy",
                        title="Foundation of Empathy",
                        description="Learn to recognize and resonate with others' emotions",
                        requirements={ProfileDimension.EMPATHY: 0.3}
                    ),
                    LearningPathNode(
                        id="active_compassion",
                        title="Active Compassion",
                        description="Transform empathy into helpful action",
                        requirements={
                            ProfileDimension.EMPATHY: 0.4,
                            ProfileDimension.COMPASSION: 0.4
                        }
                    ),
                    LearningPathNode(
                        id="healing_presence",
                        title="Healing Presence",
                        description="Develop the ability to create healing space",
                        requirements={
                            ProfileDimension.HEALING: 0.5,
                            ProfileDimension.HARMONY: 0.4
                        }
                    )
                ],
                "rewards": {
                    "completion": {
                        ProfileDimension.COMPASSION: 0.3,
                        ProfileDimension.WISDOM: 0.2
                    }
                }
            }
        }
        
    def setup_challenges(self) -> None:
        """Initialize the pond's challenge system with enhanced complexity."""
        self.challenges = {
            "empathy_bridge": {
                "title": "The Bridge of Understanding",
                "description": (
                    "Before you stand three spirits, each bearing a different burden. "
                    "You must help them find peace by understanding their perspectives."
                ),
                "spirits": [
                    {
                        "name": "The Grieving",
                        "story": "Lost something precious, fears to love again",
                        "need": "Acceptance of cycles of loss and renewal",
                        "resolution_paths": [
                            {
                                "approach": "Gentle Presence",
                                "effect": "Creates safe space for grief",
                                "reward": {ProfileDimension.EMPATHY: 0.1}
                            },
                            {
                                "approach": "Share Wisdom",
                                "effect": "Offers perspective on impermanence",
                                "reward": {ProfileDimension.WISDOM: 0.1}
                            }
                        ]
                    },
                    {
                        "name": "The Angry",
                        "story": "Suffered injustice, seeks vengeance",
                        "need": "Understanding that hatred harms the self",
                        "resolution_paths": [
                            {
                                "approach": "Compassionate Listening",
                                "effect": "Allows anger to be fully heard",
                                "reward": {ProfileDimension.COMPASSION: 0.1}
                            },
                            {
                                "approach": "Mirror of Truth",
                                "effect": "Shows impact of holding onto anger",
                                "reward": {ProfileDimension.WISDOM: 0.1}
                            }
                        ]
                    },
                    {
                        "name": "The Fearful",
                        "story": "Paralyzed by possible futures",
                        "need": "Courage to embrace uncertainty with hope",
                        "resolution_paths": [
                            {
                                "approach": "Grounding Presence",
                                "effect": "Anchors in present moment",
                                "reward": {ProfileDimension.HARMONY: 0.1}
                            },
                            {
                                "approach": "Light of Hope",
                                "effect": "Illuminates positive possibilities",
                                "reward": {ProfileDimension.HEALING: 0.1}
                            }
                        ]
                    }
                ],
                "difficulty": 0.5,
                "rewards": {
                    ProfileDimension.EMPATHY: 0.2,
                    ProfileDimension.COMPASSION: 0.2
                }
            },
            "healing_choice": {
                "title": "The Healer's Dilemma",
                "description": (
                    "Two seekers need healing, but you only have energy for one. "
                    "Choose wisely, considering both immediate and long-term effects."
                ),
                "options": {
                    "healer": {
                        "description": "Heal the traveling healer who can help others",
                        "impact": {
                            ProfileDimension.WISDOM: 0.2,
                            ProfileDimension.COMPASSION: 0.1
                        }
                    },
                    "child": {
                        "description": "Heal the child who needs immediate help",
                        "impact": {
                            ProfileDimension.EMPATHY: 0.2,
                            ProfileDimension.COMPASSION: 0.1
                        }
                    }
                },
                "difficulty": 0.7
            },
            "harmony_weaving": {
                "title": "Weaving the Threads of Peace",
                "description": (
                    "Guide conflicting energies into harmony by weaving them together. "
                    "Each thread represents a different aspect that must be balanced."
                ),
                "threads": [
                    "Justice and Mercy",
                    "Truth and Kindness",
                    "Strength and Gentleness",
                    "Wisdom and Love"
                ],
                "difficulty": 0.8,
                "rewards": {
                    ProfileDimension.HARMONY: 0.3,
                    ProfileDimension.WISDOM: 0.2,
                    ProfileDimension.EMPATHY: 0.2
                }
            }
        }

    def process_action(self, action: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Process zone-specific actions with enhanced context handling."""
        try:
            if not super().process_action(action):
                if action.startswith("comfort"):
                    return self.handle_comfort(context)
                elif action.startswith("heal"):
                    return self.handle_healing(context)
                elif action.startswith("meditate"):
                    return self.handle_meditation(context)
                elif action.startswith("teach"):
                    return self.handle_teaching(context)
                return False
            return True
        except Exception as e:
            logger.error(f"Error processing action {action}: {str(e)}")
            raise GuidanceError(f"Could not process action: {str(e)}")

    def handle_comfort(self, context: Optional[Dict[str, Any]] = None) -> bool:
        """Handle comfort action with enhanced feedback and progression."""
        try:
            player = self.current_state.get('last_player')
            if not player:
                return False
                
            # Calculate impact based on context
            base_impact = {
                ProfileDimension.EMPATHY: 0.05,
                ProfileDimension.COMPASSION: 0.05
            }
            
            # Modify impact based on context
            if context and context.get("target_emotional_state"):
                emotional_resonance = self._calculate_emotional_resonance(
                    context["target_emotional_state"]
                )
                base_impact = {k: v * emotional_resonance for k, v in base_impact.items()}
            
            player.update_profile(base_impact)
            
            # Generate dynamic feedback
            feedback = self._generate_comfort_feedback(context)
            player.ui.display_text(feedback)
            
            return True
        except Exception as e:
            logger.error(f"Error in comfort action: {str(e)}")
            return False

    def _calculate_emotional_resonance(self, target_state: str) -> float:
        """Calculate how well the player resonates with the target emotional state."""
        # Implementation details...
        return 1.0

    def _generate_comfort_feedback(self, context: Optional[Dict[str, Any]]) -> str:
        """Generate contextual feedback for comfort action."""
        base_message = (
            "You extend your compassion to those around you. The lotus flowers "
            "seem to glow more brightly in response to your kindness."
        )
        
        if not context:
            return base_message
            
        # Add contextual elements
        if context.get("target_emotional_state") == "grief":
            return base_message + (
                " The waters ripple with understanding, creating a safe "
                "space for sorrow to be held and transformed."
            )
        # Add more contextual responses...
        
        return base_message

    def handle_healing(self, context: Optional[Dict[str, Any]] = None) -> bool:
        """Handle healing action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        healing_impact = {
            ProfileDimension.COMPASSION: 0.05,
            ProfileDimension.HARMONY: 0.03
        }
        player.update_profile(healing_impact)
        
        player.ui.display_text(
            "You channel the pond's healing energy, letting it flow through you. "
            "The water ripples with silver light, responding to your intention."
        )
        return True

    def get_available_actions(self) -> List[str]:
        """Get list of available actions specific to Mercy Pond."""
        actions = super().get_available_actions()
        actions.extend(["comfort", "heal"])
        return actions

    def adapt_description(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Adapt the pond's description based on user's profile."""
        empathy = profile.get(ProfileDimension.EMPATHY, 0.0)
        compassion = profile.get(ProfileDimension.COMPASSION, 0.0)
        
        if empathy < 0.3 and compassion < 0.3:
            return (
                "The silver-blue waters lie still and quiet. You sense there is "
                "healing here, but its source remains distant and unclear."
            )
        elif empathy < 0.6 or compassion < 0.6:
            return (
                "The lotus flowers seem to respond to your presence, their petals "
                "gradually opening to reveal soft, healing light. The water's "
                "gentle currents carry whispers of compassion."
            )
        else:
            return (
                "The pond resonates with your compassionate nature. Each lotus "
                "flower glows with inner light, and the waters themselves seem "
                "to reach out with healing energy. You feel at one with the "
                "pond's merciful essence."
            )

    def get_mastery_requirements(self) -> Dict[ProfileDimension, float]:
        """Get the dimension values required to master this zone."""
        return {
            ProfileDimension.EMPATHY: 0.8,
            ProfileDimension.COMPASSION: 0.8,
            ProfileDimension.HARMONY: 0.7
        }

    def get_learning_progress(self, profile: Dict[ProfileDimension, float]) -> Dict[str, Any]:
        """Get detailed progress information for learning paths."""
        try:
            progress = {}
            for path_name, path_data in self.learning_paths.items():
                path_progress = {
                    "completed_nodes": [],
                    "available_nodes": [],
                    "locked_nodes": [],
                    "completion_percentage": 0.0
                }
                
                total_nodes = len(path_data["nodes"])
                completed_count = 0
                
                for node in path_data["nodes"]:
                    if self._check_node_completion(node, profile):
                        path_progress["completed_nodes"].append(node.id)
                        completed_count += 1
                    elif self._check_node_availability(node, profile):
                        path_progress["available_nodes"].append(node.id)
                    else:
                        path_progress["locked_nodes"].append(node.id)
                
                path_progress["completion_percentage"] = (completed_count / total_nodes) * 100
                progress[path_name] = path_progress
                
            return progress
        except Exception as e:
            logger.error(f"Error calculating learning progress: {str(e)}")
            return {}

    def _check_node_completion(self, node: LearningPathNode, profile: Dict[ProfileDimension, float]) -> bool:
        """Check if a learning node has been completed."""
        return all(
            profile.get(dim, 0) >= value
            for dim, value in node.requirements.items()
        )

    def _check_node_availability(self, node: LearningPathNode, profile: Dict[ProfileDimension, float]) -> bool:
        """Check if a learning node is available to start."""
        return all(
            profile.get(dim, 0) >= value * 0.7  # 70% of requirements
            for dim, value in node.requirements.items()
        )
