"""
Dynamic response generator that adapts quick response options based on user's personality profile.
"""
from typing import List, Dict, Optional, Tuple
from enum import Enum
from ..user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
import numpy as np

class ResponseTone(Enum):
    """Different tones for responses based on personality traits."""
    ANALYTICAL = "analytical"  # Logical, precise, detailed
    EMPATHETIC = "empathetic"  # Warm, understanding, supportive
    INTUITIVE = "intuitive"    # Abstract, metaphorical, insightful
    DYNAMIC = "dynamic"        # Energetic, action-oriented, direct

class AttitudeDirection(Enum):
    """Core attitudes that each response button represents."""
    ENTHUSIASM = "enthusiasm"      # Positive, eager engagement
    SKEPTICISM = "skepticism"      # Questioning, cautious approach
    REFLECTION = "reflection"      # Thoughtful, contemplative stance
    AVOIDANCE = "avoidance"        # Resistance or desire to move away

class ResponseTemplate:
    """Template for generating responses with different tones and attitudes."""
    def __init__(
        self,
        attitudes: Dict[AttitudeDirection, Dict[ResponseTone, str]],
        context_type: str
    ):
        self.attitudes = attitudes
        self.context_type = context_type

class ResponseGenerator:
    """Generates contextually appropriate responses based on user profile."""
    
    def __init__(self, profile_matrix: ProfileMatrix):
        self.profile_matrix = profile_matrix
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, List[ResponseTemplate]]:
        """Initialize response templates for different contexts."""
        return {
            "exploration": [
                ResponseTemplate(
                    attitudes={
                        AttitudeDirection.ENTHUSIASM: {
                            ResponseTone.ANALYTICAL: "Analyze every detail",
                            ResponseTone.EMPATHETIC: "Connect with wonder",
                            ResponseTone.INTUITIVE: "Flow with curiosity",
                            ResponseTone.DYNAMIC: "Dive right in"
                        },
                        AttitudeDirection.SKEPTICISM: {
                            ResponseTone.ANALYTICAL: "Question assumptions",
                            ResponseTone.EMPATHETIC: "Trust but verify",
                            ResponseTone.INTUITIVE: "Sense inconsistencies",
                            ResponseTone.DYNAMIC: "Test boundaries"
                        },
                        AttitudeDirection.REFLECTION: {
                            ResponseTone.ANALYTICAL: "Consider implications",
                            ResponseTone.EMPATHETIC: "Feel the resonance",
                            ResponseTone.INTUITIVE: "Perceive patterns",
                            ResponseTone.DYNAMIC: "Explore meaning"
                        },
                        AttitudeDirection.AVOIDANCE: {
                            ResponseTone.ANALYTICAL: "Maintain distance",
                            ResponseTone.EMPATHETIC: "Need space",
                            ResponseTone.INTUITIVE: "Sense resistance",
                            ResponseTone.DYNAMIC: "Step back"
                        }
                    },
                    context_type="navigation"
                )
            ],
            "reflection": [
                ResponseTemplate(
                    attitudes={
                        AttitudeDirection.ENTHUSIASM: {
                            ResponseTone.ANALYTICAL: "Examine deeply",
                            ResponseTone.EMPATHETIC: "Open heart fully",
                            ResponseTone.INTUITIVE: "Embrace wisdom",
                            ResponseTone.DYNAMIC: "Engage completely"
                        },
                        AttitudeDirection.SKEPTICISM: {
                            ResponseTone.ANALYTICAL: "Seek evidence",
                            ResponseTone.EMPATHETIC: "Question feelings",
                            ResponseTone.INTUITIVE: "Challenge insights",
                            ResponseTone.DYNAMIC: "Test beliefs"
                        },
                        AttitudeDirection.REFLECTION: {
                            ResponseTone.ANALYTICAL: "Contemplate deeply",
                            ResponseTone.EMPATHETIC: "Feel inward",
                            ResponseTone.INTUITIVE: "Listen to whispers",
                            ResponseTone.DYNAMIC: "Process actively"
                        },
                        AttitudeDirection.AVOIDANCE: {
                            ResponseTone.ANALYTICAL: "Postpone analysis",
                            ResponseTone.EMPATHETIC: "Need distance",
                            ResponseTone.INTUITIVE: "Resist insight",
                            ResponseTone.DYNAMIC: "Move away"
                        }
                    },
                    context_type="personal"
                )
            ],
            "challenge": [
                ResponseTemplate(
                    attitudes={
                        AttitudeDirection.ENTHUSIASM: {
                            ResponseTone.ANALYTICAL: "Solve systematically",
                            ResponseTone.EMPATHETIC: "Face with courage",
                            ResponseTone.INTUITIVE: "Welcome challenge",
                            ResponseTone.DYNAMIC: "Take it on"
                        },
                        AttitudeDirection.SKEPTICISM: {
                            ResponseTone.ANALYTICAL: "Assess difficulty",
                            ResponseTone.EMPATHETIC: "Question readiness",
                            ResponseTone.INTUITIVE: "Sense obstacles",
                            ResponseTone.DYNAMIC: "Test waters"
                        },
                        AttitudeDirection.REFLECTION: {
                            ResponseTone.ANALYTICAL: "Study approach",
                            ResponseTone.EMPATHETIC: "Consider impact",
                            ResponseTone.INTUITIVE: "Feel path",
                            ResponseTone.DYNAMIC: "Weigh options"
                        },
                        AttitudeDirection.AVOIDANCE: {
                            ResponseTone.ANALYTICAL: "Delay attempt",
                            ResponseTone.EMPATHETIC: "Not ready",
                            ResponseTone.INTUITIVE: "Pass for now",
                            ResponseTone.DYNAMIC: "Skip this"
                        }
                    },
                    context_type="puzzle"
                )
            ],
            "learning": [
                ResponseTemplate(
                    attitudes={
                        AttitudeDirection.ENTHUSIASM: {
                            ResponseTone.ANALYTICAL: "Study intensely",
                            ResponseTone.EMPATHETIC: "Learn with joy",
                            ResponseTone.INTUITIVE: "Absorb wisdom",
                            ResponseTone.DYNAMIC: "Dive into knowledge"
                        },
                        AttitudeDirection.SKEPTICISM: {
                            ResponseTone.ANALYTICAL: "Verify facts",
                            ResponseTone.EMPATHETIC: "Question teachings",
                            ResponseTone.INTUITIVE: "Test wisdom",
                            ResponseTone.DYNAMIC: "Challenge concepts"
                        },
                        AttitudeDirection.REFLECTION: {
                            ResponseTone.ANALYTICAL: "Process carefully",
                            ResponseTone.EMPATHETIC: "Internalize gently",
                            ResponseTone.INTUITIVE: "Contemplate meaning",
                            ResponseTone.DYNAMIC: "Explore depth"
                        },
                        AttitudeDirection.AVOIDANCE: {
                            ResponseTone.ANALYTICAL: "Too complex now",
                            ResponseTone.EMPATHETIC: "Need preparation",
                            ResponseTone.INTUITIVE: "Not aligned yet",
                            ResponseTone.DYNAMIC: "Skip lesson"
                        }
                    },
                    context_type="knowledge"
                )
            ]
        }
    
    def _get_dominant_dimensions(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> List[Tuple[ProfileDimension, float]]:
        """Get the most dominant personality dimensions."""
        sorted_dims = sorted(
            profile.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_dims[:4]  # Return top 4 dimensions
    
    def _calculate_tone_weights(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> Dict[ResponseTone, float]:
        """Calculate weights for each response tone based on profile."""
        # Map dimensions to tones they influence
        tone_influences = {
            ResponseTone.ANALYTICAL: [
                ProfileDimension.STRATEGIC_THINKING,
                ProfileDimension.DECISION_MAKING,
                ProfileDimension.TEMPORAL_AWARENESS,
                ProfileDimension.CONTEXTUAL_FLUIDITY
            ],
            ResponseTone.EMPATHETIC: [
                ProfileDimension.EMPATHY,
                ProfileDimension.EMOTIONAL_RESPONSE,
                ProfileDimension.SOCIAL_AWARENESS,
                ProfileDimension.MORAL_ALIGNMENT
            ],
            ResponseTone.INTUITIVE: [
                ProfileDimension.QUANTUM_INTUITION,
                ProfileDimension.DREAM_LOGIC,
                ProfileDimension.SYNCHRONICITY_AWARENESS,
                ProfileDimension.METAPHORICAL_THINKING
            ],
            ResponseTone.DYNAMIC: [
                ProfileDimension.CREATIVITY,
                ProfileDimension.EMERGENT_CREATIVITY,
                ProfileDimension.ADAPTABILITY,
                ProfileDimension.RISK_TOLERANCE
            ]
        }
        
        # Calculate weighted scores for each tone
        weights = {}
        for tone, dimensions in tone_influences.items():
            relevant_scores = [
                profile.get(dim, 0.5)  # Default to 0.5 if dimension not found
                for dim in dimensions
            ]
            weights[tone] = np.mean(relevant_scores)
        
        # Normalize weights
        total = sum(weights.values())
        return {
            tone: weight/total
            for tone, weight in weights.items()
        }
    
    def _select_templates(
        self,
        context: str,
        count: int = 1  # We only need one template now as it contains all attitudes
    ) -> List[ResponseTemplate]:
        """Select appropriate templates for the current context."""
        if context not in self.templates:
            # Default to exploration if context not found
            context = "exploration"
        
        available = self.templates[context]
        if len(available) <= count:
            return available
        
        # Randomly select distinct templates
        return np.random.choice(
            available,
            size=min(count, len(available)),
            replace=False
        ).tolist()
    
    def generate_responses(
        self,
        user_id: str,
        context: str = "exploration"
    ) -> List[str]:
        """Generate personalized quick responses for the user."""
        # Get user's profile
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            # Return default responses if no profile exists
            return [
                "Explore with interest",
                "Question this",
                "Think about it",
                "Maybe later"
            ]
        
        # Calculate tone weights based on profile
        tone_weights = self._calculate_tone_weights(profile.dimensions)
        
        # Select template based on context
        templates = self._select_templates(context)
        if not templates:
            return [
                "Continue with interest",
                "Express doubt",
                "Consider carefully",
                "Step back"
            ]
        
        template = templates[0]
        
        # Generate one response for each attitude, using weighted tone selection
        responses = []
        tones = list(ResponseTone)
        
        # Generate responses in consistent attitude order
        for attitude in AttitudeDirection:
            # Select tone based on weights
            tone = np.random.choice(
                tones,
                p=[tone_weights[t] for t in tones]
            )
            responses.append(template.attitudes[attitude][tone])
        
        return responses
    
    def get_response_context(
        self,
        recent_interactions: List[str],
        current_location: Optional[str] = None
    ) -> str:
        """Determine the appropriate response context based on recent interactions."""
        # Simple context detection based on keywords
        context_keywords = {
            "exploration": ["explore", "discover", "find", "look", "search"],
            "reflection": ["think", "feel", "reflect", "consider", "ponder"],
            "challenge": ["solve", "challenge", "puzzle", "problem", "quest"],
            "learning": ["learn", "study", "understand", "know", "grasp"]
        }
        
        # Count keyword matches in recent interactions
        context_scores = {context: 0 for context in context_keywords}
        
        for interaction in recent_interactions:
            lower_interaction = interaction.lower()
            for context, keywords in context_keywords.items():
                if any(keyword in lower_interaction for keyword in keywords):
                    context_scores[context] += 1
        
        # Consider current location if provided
        if current_location:
            location_lower = current_location.lower()
            if "pond" in location_lower or "stream" in location_lower:
                context_scores["exploration"] += 1
            elif "temple" in location_lower or "sanctuary" in location_lower:
                context_scores["reflection"] += 1
            elif "trial" in location_lower or "test" in location_lower:
                context_scores["challenge"] += 1
            elif "library" in location_lower or "study" in location_lower:
                context_scores["learning"] += 1
        
        # Return the context with highest score, default to exploration
        return max(context_scores.items(), key=lambda x: x[1])[0] 