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