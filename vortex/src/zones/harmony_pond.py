from typing import Dict, List, Optional
from vortex.src.zones.base_zone import Zone
from vortex.src.guides.base_guide import Guide
from vortex.src.core.user_profiling.profile_matrix import ProfileDimension
from vortex.src.core.user_profiling.personalization import ContentItem
from vortex.src.mythology.sefirot import SefirotAttribute
from vortex.src.core.user_profiling.adaptive_learning import LearningPathNode
from vortex.src.core.profiling import profile_function, profile_block, monitor_performance, performance_monitor
import logging
from dataclasses import dataclass
from vortex.src.core.exceptions import NodeSetupError

logger = logging.getLogger(__name__)

class HarmonyPond(Zone):
    """
    The Pond of Harmony - A place of integration and balanced mastery.
    
    This zone represents the culmination of all learning paths, where players
    must demonstrate mastery across multiple dimensions simultaneously.
    
    Attributes:
        dimension_weights (Dict[ProfileDimension, float]): Weights for each behavioral dimension
        required_dimensions (List[ProfileDimension]): Dimensions required for progression
        min_dimension_values (Dict[ProfileDimension, float]): Minimum values needed
        symbols (Dict[str, str]): Symbolic associations for the pond
        
    Example:
        >>> pond = HarmonyPond()
        >>> pond._setup_learning_nodes()
        >>> print(len(pond.learning_nodes))
        4
    """
    
    @monitor_performance("harmony_pond_init")
    def __init__(self) -> None:
        """
        Initialize the Harmony Pond zone.
        
        The Harmony Pond is a special zone that focuses on the integration and
        balance of all behavioral dimensions. It is guided by Ma'at, the Egyptian
        goddess of harmony and balance.
        
        The zone's challenges require players to demonstrate mastery across
        multiple dimensions simultaneously, with a strong emphasis on maintaining
        equilibrium between different aspects of their development.
        
        Attributes initialized:
            description (str): Visual description of the pond
            dimension_weights (Dict[ProfileDimension, float]): Dimension importance
            required_dimensions (List[ProfileDimension]): Core dimensions needed
            min_dimension_values (Dict[ProfileDimension, float]): Minimum requirements
            symbols (Dict[str, str]): Symbolic associations
            
        Raises:
            ImportError: If required guide module cannot be imported
            ValueError: If dimension weights don't sum to 1.0
        """
        try:
            # Initialize with Ma'at as the guide
            from ..guides.maat import MaatGuide
            guide = MaatGuide()
            super().__init__("Pond of Harmony", guide)
            
            self.description = (
                "A pristine pond of pure white light, where all elements dance in "
                "perfect balance. The surface reflects all colors while remaining "
                "clear as crystal."
            )
            
            # Configure behavioral dimensions - requires balance across all
            self.dimension_weights = {
                ProfileDimension.EMPATHY: 0.2,
                ProfileDimension.CREATIVITY: 0.2,
                ProfileDimension.STRATEGIC_THINKING: 0.2,
                ProfileDimension.MORAL_ALIGNMENT: 0.2,
                ProfileDimension.EMOTIONAL_RESPONSE: 0.2
            }
            
            # Validate dimension weights
            weight_sum = sum(self.dimension_weights.values())
            if not 0.99 <= weight_sum <= 1.01:
                raise ValueError(
                    f"Dimension weights must sum to 1.0, got {weight_sum}"
                )
            
            self.required_dimensions = [
                ProfileDimension.EMPATHY,
                ProfileDimension.CREATIVITY,
                ProfileDimension.STRATEGIC_THINKING,
                ProfileDimension.MORAL_ALIGNMENT
            ]
            
            # Validate required dimensions exist in weights
            missing_dims = set(self.required_dimensions) - set(self.dimension_weights.keys())
            if missing_dims:
                raise ValueError(
                    f"Required dimensions {missing_dims} not found in weights"
                )
            
            self.min_dimension_values = {
                ProfileDimension.EMPATHY: 0.4,
                ProfileDimension.CREATIVITY: 0.4,
                ProfileDimension.STRATEGIC_THINKING: 0.4,
                ProfileDimension.MORAL_ALIGNMENT: 0.4
            }
            
            # Validate minimum values
            invalid_mins = [
                (dim, val) for dim, val in self.min_dimension_values.items()
                if not 0.0 <= val <= 1.0
            ]
            if invalid_mins:
                raise ValueError(
                    f"Invalid minimum dimension values: {invalid_mins}"
                )
            
            # Symbolic associations
            self.symbols = {
                "element": "Void",
                "color": "White",
                "sefirot": SefirotAttribute.TIFERET,
                "animal": "Swan",
                "mineral": "Diamond"
            }
            
            # Initialize learning nodes
            self.learning_nodes = {}
            self._setup_learning_nodes()
            
            logger.info(
                f"Successfully initialized Harmony Pond with "
                f"{len(self.learning_nodes)} learning nodes"
            )
            
        except ImportError as e:
            error_msg = f"Failed to import required guide module: {str(e)}"
            logger.error(error_msg)
            raise ImportError(error_msg) from e
        except (ValueError, TypeError) as e:
            error_msg = f"Failed to initialize Harmony Pond: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e

    @monitor_performance("node_validation")
    def _validate_node(self, node: LearningPathNode) -> None:
        """
        Validate the configuration of a learning path node.
        
        This method performs comprehensive validation of a node's configuration,
        including dimension weights, required dimensions, and node connections.
        
        Args:
            node: The LearningPathNode to validate
            
        Raises:
            NodeSetupError: If any validation check fails
            TypeError: If node is not a LearningPathNode instance
            ValueError: If node contains invalid values
        """
        try:
            if not isinstance(node, LearningPathNode):
                raise TypeError("Input must be a LearningPathNode instance")
                
            if not node.node_id:
                raise ValueError("Node ID cannot be empty")
                
            # Validate content
            if not node.content:
                raise ValueError(f"Node {node.node_id} has no content")
                
            # Validate dimension weights
            if not node.content.dimension_weights:
                raise ValueError(f"Node {node.node_id} has no dimension weights")
                
            weight_sum = sum(node.content.dimension_weights.values())
            if not 0.99 <= weight_sum <= 1.01:  # Allow small floating point errors
                raise NodeSetupError(
                    f"Dimension weights for node {node.node_id} sum to {weight_sum}, "
                    "expected 1.0"
                )
            
            # Validate individual weights
            invalid_weights = [
                (dim, weight) for dim, weight in node.content.dimension_weights.items()
                if not isinstance(weight, (int, float)) or not 0.0 <= weight <= 1.0
            ]
            if invalid_weights:
                raise ValueError(
                    f"Invalid dimension weights in node {node.node_id}: {invalid_weights}"
                )
            
            # Validate required dimensions exist in weights
            missing_dims = set(node.required_dimensions.keys()) - set(node.content.dimension_weights.keys())
            if missing_dims:
                raise NodeSetupError(
                    f"Required dimensions {missing_dims} not found in weights for "
                    f"node {node.node_id}"
                )
            
            # Validate required dimension values
            invalid_requirements = [
                (dim, val) for dim, val in node.required_dimensions.items()
                if not isinstance(val, (int, float)) or not 0.0 <= val <= 1.0
            ]
            if invalid_requirements:
                raise ValueError(
                    f"Invalid required dimension values in node {node.node_id}: "
                    f"{invalid_requirements}"
                )
            
            # Validate next_nodes
            if not isinstance(node.next_nodes, list):
                raise NodeSetupError(
                    f"next_nodes must be a list for node {node.node_id}"
                )
            
            # Validate node content attributes
            for attr in ['difficulty_level', 'emotional_intensity', 
                        'creativity_required', 'strategic_depth']:
                value = getattr(node.content, attr)
                if not isinstance(value, (int, float)) or not 0.0 <= value <= 1.0:
                    raise ValueError(
                        f"Invalid {attr} value in node {node.node_id}: {value}"
                    )
            
            logger.debug(f"Successfully validated node: {node.node_id}")
                
        except (TypeError, ValueError, NodeSetupError) as e:
            error_msg = f"Node validation failed: {str(e)}"
            logger.error(error_msg)
            raise
        except AttributeError as e:
            error_msg = f"Invalid node structure: {str(e)}"
            logger.error(error_msg)
            raise NodeSetupError(f"Failed to validate node {node.node_id}: {str(e)}") from e

    @profile_function()
    @monitor_performance("harmony_pond_setup")
    def _setup_learning_nodes(self) -> None:
        """
        Set up the learning path structure for the Harmony Pond.
        
        This method creates and configures the learning nodes that form the
        progression path through the Harmony Pond. Each node represents a
        challenge that tests different aspects of the player's mastery.
        
        The nodes are structured in a directed graph with multiple possible
        paths, allowing for adaptive progression based on player performance.
        
        Raises:
            NodeSetupError: If node creation or validation fails
        """
        try:
            with profile_block("initial_balance_setup"):
                # Initial balance node
                initial_balance = LearningPathNode(
                    node_id="harmony_initial",
                    content=ContentItem(
                        content_id="balance_basics",
                        content="Feel the interplay of all elements in the pond. Let them "
                               "find their natural equilibrium within you.",
                        dimension_weights={
                            ProfileDimension.EMPATHY: 0.25,
                            ProfileDimension.CREATIVITY: 0.25,
                            ProfileDimension.STRATEGIC_THINKING: 0.25,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.25
                        },
                        difficulty_level=0.4,
                        emotional_intensity=0.5,
                        creativity_required=0.5,
                        strategic_depth=0.5
                    ),
                    required_dimensions={
                        ProfileDimension.EMPATHY: 0.4,
                        ProfileDimension.STRATEGIC_THINKING: 0.4
                    },
                    next_nodes=["harmony_integration", "harmony_flow"]
                )
                
                self._validate_node(initial_balance)
                logger.debug(f"Successfully created initial balance node: {initial_balance.node_id}")
            
            with profile_block("integration_setup"):
                # Integration challenge node
                integration = LearningPathNode(
                    node_id="harmony_integration",
                    content=ContentItem(
                        content_id="integration_challenge",
                        content="Bring together wisdom from all ponds, letting their "
                               "teachings merge into a unified understanding.",
                        dimension_weights={
                            ProfileDimension.COMPREHENSION: 0.4,
                            ProfileDimension.PATTERN_RECOGNITION: 0.3,
                            ProfileDimension.STRATEGIC_THINKING: 0.3
                        },
                        difficulty_level=0.6,
                        emotional_intensity=0.6,
                        creativity_required=0.6,
                        strategic_depth=0.7
                    ),
                    required_dimensions={
                        ProfileDimension.COMPREHENSION: 0.5,
                        ProfileDimension.STRATEGIC_THINKING: 0.5
                    },
                    next_nodes=["harmony_flow", "harmony_resonance"]
                )
                
                self._validate_node(integration)
                logger.debug(f"Successfully created integration node: {integration.node_id}")
            
            with profile_block("flow_state_setup"):
                # Flow state node
                flow_state = LearningPathNode(
                    node_id="harmony_flow",
                    content=ContentItem(
                        content_id="flow_mastery",
                        content="Move seamlessly between different modes of being, "
                               "maintaining balance while in constant motion.",
                        dimension_weights={
                            ProfileDimension.CREATIVITY: 0.4,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.3,
                            ProfileDimension.EMPATHY: 0.3
                        },
                        difficulty_level=0.7,
                        emotional_intensity=0.7,
                        creativity_required=0.8,
                        strategic_depth=0.6
                    ),
                    required_dimensions={
                        ProfileDimension.CREATIVITY: 0.6,
                        ProfileDimension.EMOTIONAL_RESPONSE: 0.5
                    },
                    next_nodes=["harmony_resonance", "harmony_transcendence"]
                )
                
                self._validate_node(flow_state)
                logger.debug(f"Successfully created flow state node: {flow_state.node_id}")
            
            with profile_block("resonance_setup"):
                # Universal resonance node
                resonance = LearningPathNode(
                    node_id="harmony_resonance",
                    content=ContentItem(
                        content_id="universal_resonance",
                        content="Attune yourself to the universal rhythms that flow "
                               "through all ponds, all beings, all existence.",
                        dimension_weights={
                            ProfileDimension.EMPATHY: 0.4,
                            ProfileDimension.MORAL_ALIGNMENT: 0.3,
                            ProfileDimension.EMOTIONAL_RESPONSE: 0.3
                        },
                        difficulty_level=0.8,
                        emotional_intensity=0.9,
                        creativity_required=0.7,
                        strategic_depth=0.7
                    ),
                    required_dimensions={
                        ProfileDimension.EMPATHY: 0.7,
                        ProfileDimension.MORAL_ALIGNMENT: 0.6
                    },
                    next_nodes=["harmony_transcendence"]
                )
                
                self._validate_node(resonance)
                logger.debug(f"Successfully created resonance node: {resonance.node_id}")
            
            # Store nodes in instance
            self.learning_nodes = {
                initial_balance.node_id: initial_balance,
                integration.node_id: integration,
                flow_state.node_id: flow_state,
                resonance.node_id: resonance
            }
            
            logger.info(
                f"Successfully set up all learning nodes for Harmony Pond. "
                f"Performance metrics: {performance_monitor.get_summary()}"
            )
            
        except Exception as e:
            error_msg = f"Failed to set up Harmony Pond nodes: {str(e)}"
            logger.error(error_msg)
            raise NodeSetupError(error_msg) from e
        
    @profile_function()
    @monitor_performance("harmony_guidance_generation")
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float],
        *,
        include_detailed_analysis: bool = False
    ) -> str:
        """
        Get personalized guidance message based on player's profile.
        
        This method analyzes the player's profile to generate a tailored guidance
        message that helps them progress through the Harmony Pond. The message
        adapts based on both overall progress and the balance between different
        dimensions.
        
        Args:
            profile: Dictionary mapping ProfileDimension to float values (0.0-1.0)
            include_detailed_analysis: Whether to include detailed dimension analysis
            
        Returns:
            A personalized guidance message tailored to the player's progress
            
        Raises:
            ValueError: If profile contains invalid dimension values
            TypeError: If profile is not a dictionary
        """
        try:
            if not isinstance(profile, dict):
                raise TypeError("Profile must be a dictionary")
                
            # Validate profile values
            invalid_values = [
                (dim, val) for dim, val in profile.items()
                if not isinstance(val, (int, float)) or not 0.0 <= val <= 1.0
            ]
            if invalid_values:
                raise ValueError(
                    f"Invalid profile values: {invalid_values}. "
                    "Values must be between 0.0 and 1.0"
                )
            
            with profile_block("progress_calculation"):
                progress = self.calculate_mastery_progress(profile)
                
                # Calculate overall balance
                dimensions = [
                    ProfileDimension.EMPATHY,
                    ProfileDimension.CREATIVITY,
                    ProfileDimension.STRATEGIC_THINKING,
                    ProfileDimension.MORAL_ALIGNMENT
                ]
                values = [profile.get(dim, 0.0) for dim in dimensions]
                avg_value = sum(values) / len(values)
                max_deviation = max(abs(v - avg_value) for v in values)
            
            # Build guidance message
            message_parts = []
            
            with profile_block("message_generation"):
                if progress < 0.3:
                    if max_deviation > 0.3:
                        message_parts.append(
                            "Seek first to balance your inner waters. "
                            "All dimensions must flow as one."
                        )
                    else:
                        message_parts.append(
                            "Your foundation is balanced. Now build upon it, "
                            "letting each aspect strengthen the others."
                        )
                elif progress < 0.6:
                    if max_deviation > 0.2:
                        message_parts.append(
                            "As you grow, maintain the harmony between all aspects. "
                            "No single quality should overshadow the others."
                        )
                    else:
                        message_parts.append(
                            "Your growth shows beautiful symmetry. Continue to nurture "
                            "all dimensions equally."
                        )
                elif progress < 0.9:
                    message_parts.append(
                        "The pond's perfect harmony resonates through your being. "
                        "Seek now the transcendent unity of all qualities."
                    )
                else:
                    message_parts.append(
                        "You have become one with the pond's divine harmony. "
                        "Your presence here now helps others find their own balance."
                    )
                
                # Add detailed analysis if requested
                if include_detailed_analysis:
                    message_parts.append("\nDimensional Analysis:")
                    
                    # Group dimensions by their level
                    exceptional = []
                    developing = []
                    needs_work = []
                    
                    for dim in dimensions:
                        value = profile.get(dim, 0.0)
                        if value >= 0.7:
                            exceptional.append(f"{dim.value}: {value:.2f}")
                        elif value >= 0.4:
                            developing.append(f"{dim.value}: {value:.2f}")
                        else:
                            needs_work.append(f"{dim.value}: {value:.2f}")
                    
                    if exceptional:
                        message_parts.append(
                            "Exceptional Qualities:\n- " + "\n- ".join(exceptional)
                        )
                    if developing:
                        message_parts.append(
                            "Developing Well:\n- " + "\n- ".join(developing)
                        )
                    if needs_work:
                        message_parts.append(
                            "Areas for Growth:\n- " + "\n- ".join(needs_work)
                        )
                    
                    # Add balance analysis
                    message_parts.append(
                        f"\nHarmony Analysis:\n"
                        f"- Overall Progress: {progress:.1%}\n"
                        f"- Balance Rating: {1.0 - max_deviation:.1%}\n"
                        f"- Average Level: {avg_value:.2f}"
                    )
            
            final_message = "\n\n".join(message_parts)
            logger.debug(
                f"Generated guidance message for progress level {progress:.2f} "
                f"with balance rating {1.0 - max_deviation:.2f}"
            )
            return final_message
            
        except (TypeError, ValueError) as e:
            error_msg = f"Error generating guidance message: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
        except KeyError as e:
            error_msg = f"Missing required profile dimension: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e 