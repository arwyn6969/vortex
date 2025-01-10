from dataclasses import dataclass
from typing import Dict, List, Optional
from .profile_matrix import ProfileDimension

@dataclass
class Question:
    """Represents a profiling question with its analysis parameters."""
    id: str
    text: str
    options: List[str]
    dimension_impacts: Dict[ProfileDimension, float]
    human_detection_weight: float

class VoightKampffQuestionnaire:
    """Implements an advanced questionnaire system inspired by the Voight-Kampff test."""
    
    def __init__(self):
        self.questions = self._initialize_questions()
        
    def _initialize_questions(self) -> List[Question]:
        """Initialize the questionnaire with carefully crafted questions."""
        return [
            Question(
                id="empathy_1",
                text="You find an injured animal on your way home. What's your immediate response?",
                options=[
                    "Take it to a vet immediately",
                    "Call animal services for help",
                    "Leave it be - nature takes its course",
                    "Take a photo to post online"
                ],
                dimension_impacts={
                    ProfileDimension.EMPATHY: 1.0,
                    ProfileDimension.DECISION_MAKING: 0.5,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.8
                },
                human_detection_weight=0.8
            ),
            Question(
                id="creativity_1",
                text="You have unlimited resources for one day. What do you create?",
                options=[
                    "A solution to a global problem",
                    "A piece of art that moves people",
                    "A revolutionary technology",
                    "A perfect moment with loved ones"
                ],
                dimension_impacts={
                    ProfileDimension.CREATIVITY: 1.0,
                    ProfileDimension.MORAL_ALIGNMENT: 0.6,
                    ProfileDimension.STRATEGIC_THINKING: 0.4
                },
                human_detection_weight=0.6
            ),
            Question(
                id="risk_1",
                text="You discover a potential security flaw in a major system. Your response?",
                options=[
                    "Report it through proper channels",
                    "Exploit it for personal gain",
                    "Share it publicly to force action",
                    "Ignore it - not your problem"
                ],
                dimension_impacts={
                    ProfileDimension.MORAL_ALIGNMENT: 1.0,
                    ProfileDimension.RISK_TOLERANCE: 0.8,
                    ProfileDimension.DECISION_MAKING: 0.7
                },
                human_detection_weight=0.9
            ),
            Question(
                id="emotional_1",
                text="A close friend betrays your trust. How do you process this?",
                options=[
                    "Confront them immediately",
                    "Take time to understand their perspective",
                    "Cut them out of your life",
                    "Pretend nothing happened"
                ],
                dimension_impacts={
                    ProfileDimension.EMOTIONAL_RESPONSE: 1.0,
                    ProfileDimension.EMPATHY: 0.7,
                    ProfileDimension.DECISION_MAKING: 0.6
                },
                human_detection_weight=0.85
            ),
            Question(
                id="strategic_1",
                text="You're faced with a complex puzzle with high stakes. Your approach?",
                options=[
                    "Analyze all possibilities methodically",
                    "Trust your intuition",
                    "Seek help from others",
                    "Look for unconventional solutions"
                ],
                dimension_impacts={
                    ProfileDimension.STRATEGIC_THINKING: 1.0,
                    ProfileDimension.RISK_TOLERANCE: 0.6,
                    ProfileDimension.DECISION_MAKING: 0.8
                },
                human_detection_weight=0.7
            ),
            # New questions for deeper profiling
            Question(
                id="empathy_2",
                text="You witness someone being unfairly criticized in public. What do you do?",
                options=[
                    "Speak up in their defense",
                    "Comfort them privately afterward",
                    "Observe the dynamics silently",
                    "Share your observations with others"
                ],
                dimension_impacts={
                    ProfileDimension.EMPATHY: 1.0,
                    ProfileDimension.MORAL_ALIGNMENT: 0.8,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.6
                },
                human_detection_weight=0.75
            ),
            Question(
                id="creativity_2",
                text="You discover an ancient symbol. How do you interpret its meaning?",
                options=[
                    "Research historical contexts",
                    "Meditate on its personal meaning",
                    "Compare it to modern symbols",
                    "Create art inspired by it"
                ],
                dimension_impacts={
                    ProfileDimension.CREATIVITY: 1.0,
                    ProfileDimension.STRATEGIC_THINKING: 0.5,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.7
                },
                human_detection_weight=0.65
            ),
            Question(
                id="moral_1",
                text="You find a powerful artifact that grants wishes, but each use harms others. Your choice?",
                options=[
                    "Destroy it to prevent misuse",
                    "Use it only for greater good",
                    "Study it to understand its power",
                    "Hide it away safely"
                ],
                dimension_impacts={
                    ProfileDimension.MORAL_ALIGNMENT: 1.0,
                    ProfileDimension.DECISION_MAKING: 0.8,
                    ProfileDimension.STRATEGIC_THINKING: 0.6
                },
                human_detection_weight=0.9
            ),
            Question(
                id="risk_2",
                text="A mysterious door appears, promising knowledge but warning of danger. Your response?",
                options=[
                    "Carefully assess the risks first",
                    "Enter immediately - knowledge is worth it",
                    "Mark the location and research it",
                    "Warn others to stay away"
                ],
                dimension_impacts={
                    ProfileDimension.RISK_TOLERANCE: 1.0,
                    ProfileDimension.STRATEGIC_THINKING: 0.7,
                    ProfileDimension.DECISION_MAKING: 0.8
                },
                human_detection_weight=0.8
            ),
            Question(
                id="emotional_2",
                text="You achieve a significant personal goal. How do you process this success?",
                options=[
                    "Celebrate with loved ones",
                    "Reflect on the journey privately",
                    "Immediately set new goals",
                    "Share your achievement publicly"
                ],
                dimension_impacts={
                    ProfileDimension.EMOTIONAL_RESPONSE: 1.0,
                    ProfileDimension.EMPATHY: 0.4,
                    ProfileDimension.STRATEGIC_THINKING: 0.5
                },
                human_detection_weight=0.7
            ),
            # New questions for additional dimensions
            Question(
                id="adaptability_1",
                text="You're suddenly transported to an unfamiliar realm with different rules of reality. Your first priority is to:",
                options=[
                    "Observe and learn the new rules systematically",
                    "Experiment to test the boundaries of this realm",
                    "Find others who might help you understand",
                    "Stick to what you know works in your reality"
                ],
                dimension_impacts={
                    ProfileDimension.ADAPTABILITY: 1.0,
                    ProfileDimension.CURIOSITY: 0.7,
                    ProfileDimension.STRATEGIC_THINKING: 0.5
                },
                human_detection_weight=0.8
            ),
            Question(
                id="curiosity_1",
                text="You discover an ancient text in an unknown language, with strange symbols that seem to shift and change. How do you approach it?",
                options=[
                    "Spend time studying the patterns in the shifting symbols",
                    "Seek out experts who might understand it",
                    "Try to replicate the symbols and experiment",
                    "Leave it be - some knowledge is better left unknown"
                ],
                dimension_impacts={
                    ProfileDimension.CURIOSITY: 1.0,
                    ProfileDimension.WISDOM: 0.6,
                    ProfileDimension.RISK_TOLERANCE: 0.4
                },
                human_detection_weight=0.7
            ),
            Question(
                id="persistence_1",
                text="You're faced with a seemingly impossible puzzle that others have given up on. After many failed attempts, you:",
                options=[
                    "Keep trying new approaches until you solve it",
                    "Take a break to reflect, then return with fresh perspective",
                    "Document your attempts and seek patterns",
                    "Accept that some puzzles aren't meant to be solved"
                ],
                dimension_impacts={
                    ProfileDimension.PERSISTENCE: 1.0,
                    ProfileDimension.ADAPTABILITY: 0.6,
                    ProfileDimension.SELF_REFLECTION: 0.5
                },
                human_detection_weight=0.8
            ),
            Question(
                id="social_awareness_1",
                text="In a gathering of diverse beings from different realms, you notice tensions rising. How do you contribute to the situation?",
                options=[
                    "Observe the underlying dynamics and mediate",
                    "Share stories that highlight common ground",
                    "Focus on the shared goal that brought everyone together",
                    "Maintain distance to avoid potential conflict"
                ],
                dimension_impacts={
                    ProfileDimension.SOCIAL_AWARENESS: 1.0,
                    ProfileDimension.EMPATHY: 0.8,
                    ProfileDimension.WISDOM: 0.5
                },
                human_detection_weight=0.9
            ),
            Question(
                id="self_reflection_1",
                text="After a significant failure that affected others, you find yourself:",
                options=[
                    "Analyzing your decision-making process in detail",
                    "Seeking feedback from those affected",
                    "Planning how to prevent similar situations",
                    "Moving on to focus on the next challenge"
                ],
                dimension_impacts={
                    ProfileDimension.SELF_REFLECTION: 1.0,
                    ProfileDimension.EMOTIONAL_RESPONSE: 0.7,
                    ProfileDimension.MORAL_ALIGNMENT: 0.6
                },
                human_detection_weight=0.85
            ),
            Question(
                id="wisdom_integration_1",
                text="You possess knowledge that could grant great power, but its origins are mysterious. What matters most in deciding how to use it?",
                options=[
                    "Understanding the potential consequences for all involved",
                    "The practical applications and immediate benefits",
                    "The historical context and patterns of similar power",
                    "Your intuitive sense of right and wrong"
                ],
                dimension_impacts={
                    ProfileDimension.WISDOM: 1.0,
                    ProfileDimension.MORAL_ALIGNMENT: 0.8,
                    ProfileDimension.STRATEGIC_THINKING: 0.6
                },
                human_detection_weight=0.9
            ),
            Question(
                id="adaptability_2",
                text="The fundamental laws of your reality suddenly shift. Your magic works differently, and familiar patterns yield unexpected results. You:",
                options=[
                    "Systematically test and document the new patterns",
                    "Embrace the chaos and improvise new approaches",
                    "Seek others experiencing the same changes",
                    "Focus on preserving what still works normally"
                ],
                dimension_impacts={
                    ProfileDimension.ADAPTABILITY: 1.0,
                    ProfileDimension.PERSISTENCE: 0.7,
                    ProfileDimension.CREATIVITY: 0.6
                },
                human_detection_weight=0.8
            ),
            Question(
                id="social_wisdom_1",
                text="You discover that a powerful artifact is causing subtle but significant changes in people's behavior. Your approach is to:",
                options=[
                    "Study both the artifact and its social impact",
                    "Remove it immediately to prevent further influence",
                    "Consult with those affected before acting",
                    "Monitor the changes to understand their purpose"
                ],
                dimension_impacts={
                    ProfileDimension.SOCIAL_AWARENESS: 0.9,
                    ProfileDimension.WISDOM: 0.8,
                    ProfileDimension.EMPATHY: 0.7
                },
                human_detection_weight=0.85
            ),
            Question(
                id="curiosity_wisdom_1",
                text="You find a way to access all knowledge in existence, but each truth learned permanently changes your perspective. How do you proceed?",
                options=[
                    "Carefully select specific knowledge that aids growth",
                    "Embrace the changes and learn as much as possible",
                    "Focus on practical knowledge with clear benefits",
                    "Share the access with others to distribute the impact"
                ],
                dimension_impacts={
                    ProfileDimension.CURIOSITY: 0.9,
                    ProfileDimension.WISDOM: 0.8,
                    ProfileDimension.SELF_REFLECTION: 0.7
                },
                human_detection_weight=0.9
            ),
            Question(
                id="persistence_reflection_1",
                text="After multiple failed attempts at a challenging magical ritual, you notice each failure reveals something about yourself. You decide to:",
                options=[
                    "Document both the technical and personal insights",
                    "Focus solely on perfecting the ritual technique",
                    "Share your journey to help others learn",
                    "Reevaluate if this path is right for you"
                ],
                dimension_impacts={
                    ProfileDimension.PERSISTENCE: 0.9,
                    ProfileDimension.SELF_REFLECTION: 0.8,
                    ProfileDimension.WISDOM: 0.6
                },
                human_detection_weight=0.85
            ),
            Question(
                id="cognitive_entropy_1",
                text="You're asked to generate a truly random sequence. Which feels most natural to you?",
                options=[
                    "Let your mind wander and type whatever numbers come",
                    "Use external events like leaf movements to generate numbers",
                    "Create a mathematical pattern then break it deliberately",
                    "Alternate between different personal sequences"
                ],
                dimension_impacts={
                    ProfileDimension.COGNITIVE_ENTROPY: 1.0,
                    ProfileDimension.EMERGENT_CREATIVITY: 0.7,
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 0.5
                },
                human_detection_weight=0.9
            ),
            Question(
                id="temporal_paradox_1",
                text="You encounter your future self who tells you to do exactly what led to them becoming who they are. What's your response?",
                options=[
                    "Question the nature of free will and causality",
                    "Choose a different path to test if destiny is fixed",
                    "Accept the loop but seek to understand it",
                    "Ignore the encounter to maintain autonomy"
                ],
                dimension_impacts={
                    ProfileDimension.TEMPORAL_AWARENESS: 1.0,
                    ProfileDimension.CONTEXTUAL_FLUIDITY: 0.8,
                    ProfileDimension.QUANTUM_INTUITION: 0.6
                },
                human_detection_weight=0.85
            ),
            Question(
                id="paradox_handling_1",
                text="You're presented with a statement that is both true and false simultaneously. Your approach is to:",
                options=[
                    "Hold both truths simultaneously while exploring their interaction",
                    "Break down the context that makes it paradoxical",
                    "Accept it as a limitation of binary logic",
                    "Choose the interpretation that's most useful"
                ],
                dimension_impacts={
                    ProfileDimension.CONTEXTUAL_FLUIDITY: 1.0,
                    ProfileDimension.DREAM_LOGIC: 0.8,
                    ProfileDimension.QUANTUM_INTUITION: 0.7
                },
                human_detection_weight=0.9
            ),
            Question(
                id="metaphor_depth_1",
                text="In a dream, you're both the ocean and a single drop of water. This makes you feel:",
                options=[
                    "A profound understanding of unity and individuality",
                    "Confused by the logical impossibility",
                    "Curious about the symbolic meaning",
                    "Focused on the emotional resonance"
                ],
                dimension_impacts={
                    ProfileDimension.METAPHORICAL_THINKING: 1.0,
                    ProfileDimension.DREAM_LOGIC: 0.8,
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 0.7
                },
                human_detection_weight=0.95
            ),
            Question(
                id="sensory_synthesis_1",
                text="You experience a moment where sounds have colors and emotions have textures. Your reaction is to:",
                options=[
                    "Explore how different senses interconnect",
                    "Try to separate and categorize each sensation",
                    "Express the experience through art",
                    "Analyze if it's a new form of perception"
                ],
                dimension_impacts={
                    ProfileDimension.SENSORY_INTEGRATION: 1.0,
                    ProfileDimension.EMERGENT_CREATIVITY: 0.8,
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 0.6
                },
                human_detection_weight=0.9
            ),
            Question(
                id="quantum_perception_1",
                text="You observe a particle that only exists when unobserved. You feel:",
                options=[
                    "A deep resonance with the paradox",
                    "Frustrated by the logical contradiction",
                    "Excited to explore the implications",
                    "Determined to find a classical explanation"
                ],
                dimension_impacts={
                    ProfileDimension.QUANTUM_INTUITION: 1.0,
                    ProfileDimension.CONTEXTUAL_FLUIDITY: 0.7,
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 0.6
                },
                human_detection_weight=0.85
            ),
            Question(
                id="emergent_pattern_1",
                text="You notice a pattern that seems meaningful but defies logical explanation. You:",
                options=[
                    "Trust your intuition about its significance",
                    "Look for hidden variables causing the pattern",
                    "Document it without trying to explain it",
                    "Dismiss it as coincidence"
                ],
                dimension_impacts={
                    ProfileDimension.SYNCHRONICITY_AWARENESS: 1.0,
                    ProfileDimension.QUANTUM_INTUITION: 0.7,
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 0.6
                },
                human_detection_weight=0.9
            ),
            Question(
                id="consciousness_probe_1",
                text="During meditation, you experience being simultaneously everywhere and nowhere. This makes you:",
                options=[
                    "Feel a deeper understanding of consciousness",
                    "Question the nature of individual identity",
                    "Try to maintain and extend the experience",
                    "Return to normal awareness for stability"
                ],
                dimension_impacts={
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 1.0,
                    ProfileDimension.METAPHORICAL_THINKING: 0.8,
                    ProfileDimension.TEMPORAL_AWARENESS: 0.6
                },
                human_detection_weight=0.95
            ),
            Question(
                id="dream_logic_1",
                text="In a lucid dream, you can change the rules of reality. You choose to:",
                options=[
                    "Explore impossible geometries and paradoxes",
                    "Create new forms of consciousness",
                    "Test the limits of dream physics",
                    "Maintain normal physics for stability"
                ],
                dimension_impacts={
                    ProfileDimension.DREAM_LOGIC: 1.0,
                    ProfileDimension.EMERGENT_CREATIVITY: 0.8,
                    ProfileDimension.QUANTUM_INTUITION: 0.7
                },
                human_detection_weight=0.9
            ),
            Question(
                id="creative_emergence_1",
                text="You're asked to imagine a new color that no one has ever seen. Your approach is to:",
                options=[
                    "Blend existing colors in impossible ways",
                    "Try to perceive beyond visible spectrum",
                    "Imagine colors from other dimensions",
                    "Focus on the emotional quality of colors"
                ],
                dimension_impacts={
                    ProfileDimension.EMERGENT_CREATIVITY: 1.0,
                    ProfileDimension.SENSORY_INTEGRATION: 0.8,
                    ProfileDimension.CONSCIOUSNESS_DEPTH: 0.7
                },
                human_detection_weight=0.95
            )
        ]
        
    def get_question(self, index: int) -> Optional[Question]:
        """Retrieve a specific question by index."""
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
        
    def analyze_response(
        self,
        question: Question,
        option_index: int
    ) -> Dict[str, float]:
        """Analyze a user's response to generate profile updates."""
        # Validate inputs
        if not isinstance(option_index, int):
            raise ValueError("option_index must be an integer")
            
        if option_index < 0 or option_index >= len(question.options):
            raise ValueError(
                f"option_index must be between 0 and {len(question.options)-1}"
            )
            
        # Response analysis weights for each option (0-3)
        weights = [1.0, 0.7, 0.3, 0.0]
        weight = weights[option_index]
        
        # Generate impact values for each dimension
        impacts = {
            dim: value * weight
            for dim, value in question.dimension_impacts.items()
        }
        
        # Add human probability assessment
        impacts['human_probability'] = (
            question.human_detection_weight * weight
        )
        
        return impacts 