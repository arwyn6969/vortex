"""
The Brain Galaxy - A place of expanding consciousness and big brain energy.
Inspired by:
- Ancient wisdom traditions: Greek philosophy (Plato's Cave), Hermetic teachings
- Modern science: Neural networks, quantum mechanics, complexity theory
- Pop culture: Rick and Morty's multiverse, Inception's dream layers
- Philosophers: Carl Jung (collective unconscious), Ken Wilber (integral theory)
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.pepe_guides import WisePepe
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode
import logging
from ..core.exceptions import GuidanceError

logger = logging.getLogger(__name__)

class BrainGalaxy(Zone):
    """The Brain Galaxy - A place of expanding consciousness and big brain energy."""
    
    def __init__(self):
        # Initialize with Wise Pepe as the guide
        guide = WisePepe()
        super().__init__("Brain Galaxy", guide)
        
        self.description = (
            "A vast cosmic pond where galaxies of neural networks swirl in the void, "
            "reminiscent of the Hermetic axiom 'As above, so below.' Floating 5Heads "
            "of various sizes bob gently in the cosmic currents, each one containing "
            "multiverses of knowledge - like Indra's Net where each jewel reflects all others. "
            "The air crackles with big brain energy, echoing the quantum field of infinite "
            "possibilities described by both ancient mystics and modern physicists."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.STRATEGIC_THINKING: 0.6,
            ProfileDimension.DECISION_MAKING: 0.4,
            ProfileDimension.WISDOM: 0.3,
            ProfileDimension.PERCEPTION: 0.2
        }
        
        self.required_dimensions = [
            ProfileDimension.STRATEGIC_THINKING,
            ProfileDimension.DECISION_MAKING
        ]
        
        self.min_dimension_values = {
            ProfileDimension.STRATEGIC_THINKING: 0.3,
            ProfileDimension.DECISION_MAKING: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Aether (Quintessence)",
            "color": "Galaxy Brain Purple (inspired by cosmic nebulae)",
            "sefirot": SefirotAttribute.CHOKMAH,
            "animal": "5Head Pepe (inspired by Thoth/Hermes)",
            "mineral": "Lapis Philosophorum (Philosopher's Stone)",
            "cultural_elements": {
                "wisdom_traditions": [
                    "Hermeticism (As above, so below)",
                    "Platonic Forms",
                    "Buddhist Emptiness",
                    "Quantum Physics"
                ],
                "modern_interpretations": [
                    "Neural Networks",
                    "Collective Intelligence",
                    "Emergent Complexity",
                    "Integral Theory"
                ],
                "pop_culture": [
                    "Rick and Morty's Council of Ricks",
                    "Inception's Dream Architecture",
                    "Matrix's Neural Interface",
                    "Hitchhiker's Deep Thought"
                ]
            }
        }
        
    def setup_challenges(self) -> None:
        """Initialize the pond's challenge system."""
        self.challenges = {
            "galaxy_brain": {
                "title": "The Expanding Brain (Inspired by Ken Wilber's Evolution of Consciousness)",
                "description": "Watch as your consciousness expands through four stages of enlightenment.",
                "stages": [
                    "Small Brain: Basic pattern recognition (Sensorimotor)",
                    "Normal Brain: Strategic thinking (Rational-Egoic)",
                    "Glowing Brain: Multidimensional chess moves (Vision-Logic)",
                    "Galaxy Brain: Transcendent 5Head plays (Non-Dual)"
                ],
                "difficulty": 0.3,
                "rewards": {
                    ProfileDimension.STRATEGIC_THINKING: 0.1,
                    ProfileDimension.WISDOM: 0.1
                }
            },
            "4d_chess": {
                "title": "Interdimensional Chess (Inspired by Quantum Game Theory)",
                "description": "Play chess across multiple timelines while exploring quantum superposition.",
                "difficulty": 0.7,
                "steps": [
                    "Calculate quantum probabilities (Schrödinger's Gambit)",
                    "Make moves in parallel universes (Many-Worlds Opening)",
                    "Create a temporal paradox gambit (Wheeler's Delayed Choice)"
                ],
                "rewards": {
                    ProfileDimension.STRATEGIC_THINKING: 0.2,
                    ProfileDimension.DECISION_MAKING: 0.2
                }
            },
            "big_brain_time": {
                "title": "It's Big Brain Time (Based on Plato's Allegory of the Cave)",
                "description": "Transcend the shadows of ordinary perception into higher dimensions of understanding.",
                "options": {
                    "expand": {
                        "description": "Let your mind expand beyond mortal limits (Nous/Divine Intellect)",
                        "impact": {
                            ProfileDimension.WISDOM: 0.3,
                            ProfileDimension.STRATEGIC_THINKING: 0.2
                        }
                    },
                    "transcend": {
                        "description": "Ascend to a higher plane of consciousness (Platonic Forms)",
                        "impact": {
                            ProfileDimension.WISDOM: 0.2,
                            ProfileDimension.PERCEPTION: 0.2,
                            ProfileDimension.STRATEGIC_THINKING: 0.1
                        }
                    }
                },
                "difficulty": 0.9
            }
        }

    def process_action(self, action: str) -> bool:
        """Process zone-specific actions."""
        if not super().process_action(action):
            # Handle custom actions
            if action.startswith("meditate"):
                return self.handle_meditation()
            elif action.startswith("study"):
                return self.handle_study()
            return False
        return True

    def handle_meditation(self) -> bool:
        """Handle meditation action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        meditation_impact = {
            ProfileDimension.WISDOM: 0.05,
            ProfileDimension.PERCEPTION: 0.05
        }
        player.update_profile(meditation_impact)
        
        player.ui.display_text(
            "You sit in quiet contemplation by the pond's edge. The ripples "
            "of water seem to match your breathing, bringing clarity to your thoughts."
        )
        return True

    def handle_study(self) -> bool:
        """Handle study action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        study_impact = {
            ProfileDimension.STRATEGIC_THINKING: 0.05,
            ProfileDimension.WISDOM: 0.03
        }
        player.update_profile(study_impact)
        
        player.ui.display_text(
            "You examine the ancient symbols and patterns in the water. "
            "Each ripple seems to contain a lesson, if only you can perceive it."
        )
        return True

    def get_symbolic_info(self) -> Dict:
        """Get symbolic associations for the Wisdom Pond."""
        return self.symbols

    def get_available_actions(self) -> List[str]:
        """Get list of available actions specific to Wisdom Pond."""
        actions = super().get_available_actions()
        actions.extend(["meditate", "study"])
        return actions

    def adapt_description(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Adapt the pond's description based on user's profile."""
        try:
            if not isinstance(profile, dict):
                raise ValueError("Profile must be a dictionary")
                
            strategic = profile.get(ProfileDimension.STRATEGIC_THINKING, 0.0)
            decision = profile.get(ProfileDimension.DECISION_MAKING, 0.0)
            
            # Validate values
            if not isinstance(strategic, (int, float)) or not isinstance(decision, (int, float)):
                raise ValueError("Profile values must be numbers")
            if strategic < 0.0 or strategic > 1.0 or decision < 0.0 or decision > 1.0:
                raise ValueError("Profile values must be between 0 and 1")
            
            if strategic < 0.3 and decision < 0.3:
                return (
                    "The pond's surface is mirror-like, reflecting your own thoughts "
                    "back at you. The wisdom here feels distant, yet attainable."
                )
            elif strategic < 0.6 or decision < 0.6:
                return (
                    "Ripples of insight disturb the pond's surface, hinting at the "
                    "deeper wisdom that lies beneath. You sense patterns forming."
                )
            else:
                return (
                    "The pond's waters seem to pulse with ancient knowledge, its "
                    "patterns clear to your experienced mind. Strategic possibilities "
                    "unfold before you like lotus blossoms."
                )
                
        except Exception as e:
            self.guide.speak(f"Error adapting description: {str(e)}")
            return self.description  # Fall back to default description

    def get_available_challenges(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> List[ContentItem]:
        """Get challenges appropriate for the user's profile."""
        try:
            if not isinstance(profile, dict):
                raise ValueError("Profile must be a dictionary")
                
            # Validate profile dimensions
            for dim, value in profile.items():
                if not isinstance(dim, ProfileDimension):
                    raise ValueError(f"Invalid profile dimension: {dim}")
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Invalid value for dimension {dim}: {value}")
                if value < 0.0 or value > 1.0:
                    raise ValueError(f"Value for dimension {dim} must be between 0 and 1")
            
            difficulty = self.get_challenge_difficulty(profile)
            
            challenges = [
                ContentItem(
                    content_id="galaxy_brain",
                    content="The Expanding Brain: Watch as your consciousness expands through four stages of enlightenment.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.3,
                    emotional_intensity=0.2,
                    creativity_required=0.4,
                    strategic_depth=0.5
                ),
                ContentItem(
                    content_id="4d_chess",
                    content="Interdimensional Chess: Play chess across multiple timelines while Rick & Morty plays in the background.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.7,
                    emotional_intensity=0.3,
                    creativity_required=0.6,
                    strategic_depth=0.8
                ),
                ContentItem(
                    content_id="big_brain_time",
                    content="It's Big Brain Time: Solve increasingly complex problems while your brain visibly expands.",
                    dimension_weights=self.dimension_weights,
                    difficulty_level=0.9,
                    emotional_intensity=0.8,
                    creativity_required=0.5,
                    strategic_depth=0.9
                )
            ]
            
            # Filter challenges based on difficulty with error handling
            try:
                return [
                    challenge for challenge in challenges
                    if abs(challenge.difficulty_level - difficulty) < 0.3
                ]
            except Exception as e:
                self.guide.speak(
                    "Warning: Error filtering challenges. Returning all available challenges."
                )
                return challenges
                
        except Exception as e:
            self.guide.speak(f"Error retrieving challenges: {str(e)}")
            return []

    def process_interaction(
        self,
        interaction_type: str,
        context: str,
        duration: float,
        metadata: Optional[Dict] = None
    ) -> Dict[ProfileDimension, float]:
        """Process user interaction and return dimension impacts."""
        try:
            metadata = metadata or {}
            impacts = {}
            
            if not isinstance(interaction_type, str):
                raise ValueError("interaction_type must be a string")
            if not isinstance(duration, (int, float)):
                raise ValueError("duration must be a number")
            if duration < 0:
                raise ValueError("duration cannot be negative")
            
            if interaction_type == "puzzle_solve":
                # Validate puzzle metadata
                if not isinstance(metadata.get('success'), bool):
                    raise ValueError("puzzle_solve requires 'success' boolean in metadata")
                if not isinstance(metadata.get('difficulty', 0.5), (int, float)):
                    raise ValueError("puzzle difficulty must be a number")
                    
                difficulty = max(0.0, min(1.0, metadata.get('difficulty', 0.5)))
                success = metadata.get('success', False)
                
                impacts[ProfileDimension.STRATEGIC_THINKING] = (
                    0.1 * difficulty * (1.0 if success else 0.5)
                )
                impacts[ProfileDimension.DECISION_MAKING] = (
                    0.05 * difficulty * (1.0 if success else 0.5)
                )
                
            elif interaction_type == "big_brain_time":
                # Validate choice metadata
                if not isinstance(metadata.get('complexity', 0.5), (int, float)):
                    raise ValueError("choice complexity must be a number")
                if not isinstance(metadata.get('wisdom_rating', 0.5), (int, float)):
                    raise ValueError("wisdom_rating must be a number")
                    
                choice_complexity = max(0.0, min(1.0, metadata.get('complexity', 0.5)))
                choice_wisdom = max(0.0, min(1.0, metadata.get('wisdom_rating', 0.5)))
                
                impacts[ProfileDimension.DECISION_MAKING] = (
                    0.1 * choice_complexity * choice_wisdom
                )
                impacts[ProfileDimension.STRATEGIC_THINKING] = (
                    0.05 * choice_complexity * choice_wisdom
                )
            else:
                raise ValueError(f"Unknown interaction type: {interaction_type}")
                
            return impacts
            
        except Exception as e:
            self.guide.speak(f"An error occurred while processing the interaction: {str(e)}")
            return {}
        
    def get_mastery_requirements(self) -> Dict[ProfileDimension, float]:
        """Get the dimension values required to master this zone."""
        return {
            ProfileDimension.STRATEGIC_THINKING: 0.8,
            ProfileDimension.DECISION_MAKING: 0.7
        }
        
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float],
        *,
        include_detailed_analysis: bool = False
    ) -> str:
        """
        Get personalized guidance message based on profile.
        
        Args:
            profile: Dictionary mapping ProfileDimension to float values (0.0-1.0)
            include_detailed_analysis: Whether to include detailed dimension analysis
            
        Returns:
            Personalized guidance message
            
        Raises:
            GuidanceError: If profile is invalid or guidance generation fails
        """
        try:
            # Validate profile
            if not profile:
                raise GuidanceError("Empty profile provided")
                
            # Validate profile values
            invalid_values = [
                (dim, val) for dim, val in profile.items()
                if not 0.0 <= val <= 1.0
            ]
            if invalid_values:
                raise GuidanceError(
                    f"Invalid profile values: {invalid_values}"
                )
            
            # Calculate progress with error handling
            try:
                progress = self.calculate_mastery_progress(profile)
            except Exception as e:
                logger.error(f"Failed to calculate mastery progress: {str(e)}")
                progress = 0.0
            
            # Get key dimensions with defaults
            strategic = profile.get(ProfileDimension.STRATEGIC_THINKING, 0.0)
            decision = profile.get(ProfileDimension.DECISION_MAKING, 0.0)
            
            # Build guidance message
            message = []
            
            if progress < 0.3:
                if strategic < decision:
                    message.append(
                        "Focus on understanding patterns and connections. "
                        "The pond's wisdom will reveal itself through careful study."
                    )
                else:
                    message.append(
                        "Your strategic mind is growing. Now learn to apply this "
                        "wisdom in making balanced decisions."
                    )
            elif progress < 0.6:
                if strategic < 0.6:
                    message.append(
                        "You begin to see the deeper patterns. Let the pond's "
                        "ancient wisdom guide your strategic thinking."
                    )
                else:
                    message.append(
                        "Your mastery grows. Each decision now ripples with "
                        "potential, changing both you and the pond."
                    )
            elif progress < 0.9:
                message.append(
                    "The pond's wisdom flows through you. Seek now the perfect "
                    "balance of strategic insight and decisive action."
                )
            else:
                message.append(
                    "You have become one with the pond's wisdom. Your presence "
                    "here now teaches others through the ripples you create."
                )
            
            # Add detailed analysis if requested
            if include_detailed_analysis:
                message.append("\nDetailed Analysis:")
                for dimension, value in profile.items():
                    if value >= 0.7:
                        message.append(f"- Your {dimension.value} is exceptional ({value:.2f})")
                    elif value >= 0.4:
                        message.append(f"- Your {dimension.value} is developing well ({value:.2f})")
                    else:
                        message.append(f"- Your {dimension.value} needs attention ({value:.2f})")
            
            final_message = "\n".join(message)
            logger.debug(f"Generated guidance message for progress level {progress:.2f}")
            return final_message
            
        except Exception as e:
            error_msg = f"Failed to generate guidance message: {str(e)}"
            logger.error(error_msg)
            raise GuidanceError(error_msg) from e

    def _setup_learning_nodes(self) -> None:
        """Set up the learning path structure for the Wisdom Pond."""
        # Basic riddle node
        basic_riddle = LearningPathNode(
            node_id="wisdom_basic_riddle",
            content=ContentItem(
                content_id="riddle_basic",
                content="What has roots that nobody sees, is taller than trees, "
                       "up, up it goes, and yet never grows?",
                dimension_weights={
                    ProfileDimension.STRATEGIC_THINKING: 0.6,
                    ProfileDimension.DECISION_MAKING: 0.4
                },
                difficulty_level=0.3,
                emotional_intensity=0.2,
                creativity_required=0.4,
                strategic_depth=0.5
            ),
            required_dimensions={
                ProfileDimension.STRATEGIC_THINKING: 0.2,
                ProfileDimension.DECISION_MAKING: 0.2
            },
            next_nodes=["wisdom_pattern_recognition", "wisdom_strategic_game"]
        )
        
        # Pattern recognition challenge
        pattern_recognition = LearningPathNode(
            node_id="wisdom_pattern_recognition",
            content=ContentItem(
                content_id="pattern_recognition",
                content="Observe the sacred symbols in the water. "
                       "Find the pattern that connects them all.",
                dimension_weights={
                    ProfileDimension.STRATEGIC_THINKING: 0.7,
                    ProfileDimension.PATTERN_RECOGNITION: 0.3
                },
                difficulty_level=0.5,
                emotional_intensity=0.3,
                creativity_required=0.5,
                strategic_depth=0.6
            ),
            required_dimensions={
                ProfileDimension.STRATEGIC_THINKING: 0.3,
                ProfileDimension.PATTERN_RECOGNITION: 0.2
            },
            next_nodes=["wisdom_strategic_game", "wisdom_ethical_choice"]
        )
        
        # Strategic game node
        strategic_game = LearningPathNode(
            node_id="wisdom_strategic_game",
            content=ContentItem(
                content_id="strategic_puzzle",
                content="The Ancient Game: Position the sacred stones to "
                       "create harmony while blocking your opponent's paths.",
                dimension_weights={
                    ProfileDimension.STRATEGIC_THINKING: 0.5,
                    ProfileDimension.DECISION_MAKING: 0.5
                },
                difficulty_level=0.7,
                emotional_intensity=0.3,
                creativity_required=0.6,
                strategic_depth=0.8
            ),
            required_dimensions={
                ProfileDimension.STRATEGIC_THINKING: 0.4,
                ProfileDimension.DECISION_MAKING: 0.4
            },
            next_nodes=["wisdom_ethical_choice", "wisdom_synthesis"]
        )
        
        # Ethical choice node
        ethical_choice = LearningPathNode(
            node_id="wisdom_ethical_choice",
            content=ContentItem(
                content_id="wisdom_choice",
                content="A choice between immediate enlightenment with "
                       "personal cost, or gradual growth that benefits others.",
                dimension_weights={
                    ProfileDimension.DECISION_MAKING: 0.4,
                    ProfileDimension.MORAL_ALIGNMENT: 0.3,
                    ProfileDimension.EMPATHY: 0.3
                },
                difficulty_level=0.8,
                emotional_intensity=0.8,
                creativity_required=0.5,
                strategic_depth=0.7
            ),
            required_dimensions={
                ProfileDimension.DECISION_MAKING: 0.5,
                ProfileDimension.MORAL_ALIGNMENT: 0.4
            },
            next_nodes=["wisdom_synthesis"]
        )
        
        # Final synthesis node
        synthesis = LearningPathNode(
            node_id="wisdom_synthesis",
            content=ContentItem(
                content_id="wisdom_synthesis",
                content="Synthesize all you've learned into a cohesive "
                       "understanding. Connect the patterns, strategies, "
                       "and ethical implications.",
                dimension_weights={
                    ProfileDimension.STRATEGIC_THINKING: 0.3,
                    ProfileDimension.DECISION_MAKING: 0.3,
                    ProfileDimension.MORAL_ALIGNMENT: 0.2,
                    ProfileDimension.PATTERN_RECOGNITION: 0.2
                },
                difficulty_level=0.9,
                emotional_intensity=0.6,
                creativity_required=0.7,
                strategic_depth=0.9
            ),
            required_dimensions={
                ProfileDimension.STRATEGIC_THINKING: 0.6,
                ProfileDimension.DECISION_MAKING: 0.6,
                ProfileDimension.MORAL_ALIGNMENT: 0.5
            },
            next_nodes=[]  # Terminal node
        )
        
        # Add all nodes to the learning path
        for node in [
            basic_riddle,
            pattern_recognition,
            strategic_game,
            ethical_choice,
            synthesis
        ]:
            self.learning_path.add_node(node)

WisdomPond = BrainGalaxy 