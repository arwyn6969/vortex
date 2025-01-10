from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple
import numpy as np

from .questionnaire import Question, VoightKampffQuestionnaire
from .profile_matrix import ProfileDimension, ProfileMatrix

@dataclass
class QuestionResponse:
    """Tracks a user's response to a question and its impact."""
    question: Question
    selected_option: int
    dimension_impacts: Dict[ProfileDimension, float]
    confidence_scores: Dict[ProfileDimension, float]
    timestamp: float

class AdaptiveQuestionnaire:
    """Enhanced questionnaire system with adaptive capabilities."""
    
    def __init__(
        self,
        base_questionnaire: VoightKampffQuestionnaire,
        profile_matrix: ProfileMatrix,
        min_confidence_threshold: float = 0.6,
        max_questions: int = 20
    ):
        self.base_questionnaire = base_questionnaire
        self.profile_matrix = profile_matrix
        self.min_confidence_threshold = min_confidence_threshold
        self.max_questions = max_questions
        self.response_history: Dict[str, List[QuestionResponse]] = {}
        
    def get_next_question(self, user_id: str) -> Optional[Question]:
        """Get the next most appropriate question based on current profile."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            # Start with first question if no profile exists
            return self.base_questionnaire.get_question(0)
            
        # Get dimensions that need more confidence
        low_confidence_dimensions = self._get_low_confidence_dimensions(profile)
        if not low_confidence_dimensions and len(self.response_history.get(user_id, [])) >= self.max_questions:
            return None
            
        # Get questions not yet asked
        asked_questions = {
            resp.question.id for resp in self.response_history.get(user_id, [])
        }
        available_questions = [
            q for q in self.base_questionnaire.questions
            if q.id not in asked_questions
        ]
        
        if not available_questions:
            return None
            
        # Score questions based on relevance to low confidence dimensions
        question_scores = []
        for question in available_questions:
            score = self._calculate_question_relevance(
                question,
                low_confidence_dimensions,
                profile
            )
            question_scores.append((question, score))
            
        # Return highest scoring question
        return max(question_scores, key=lambda x: x[1])[0]
        
    def process_response(
        self,
        user_id: str,
        question: Question,
        selected_option: int
    ) -> Dict[ProfileDimension, Tuple[float, float]]:
        """Process a response and update the profile with new insights."""
        # Validate response
        if not 0 <= selected_option < len(question.options):
            raise ValueError(f"Invalid option index: {selected_option}")
            
        # Calculate impacts
        impacts = self.base_questionnaire.analyze_response(question, selected_option)
        
        # Calculate confidence scores based on question relevance
        confidence_scores = {}
        for dimension, impact in impacts.items():
            if dimension == 'human_probability':
                continue
            # Higher confidence for primary dimensions of the question
            base_confidence = question.dimension_impacts.get(dimension, 0) * 0.2
            # Adjust confidence based on previous responses
            history_confidence = self._calculate_history_confidence(
                user_id,
                dimension,
                question,
                selected_option
            )
            confidence_scores[dimension] = min(0.9, base_confidence + history_confidence)
            
        # Record response
        response = QuestionResponse(
            question=question,
            selected_option=selected_option,
            dimension_impacts=impacts,
            confidence_scores=confidence_scores,
            timestamp=np.datetime64('now').astype(float)
        )
        
        if user_id not in self.response_history:
            self.response_history[user_id] = []
        self.response_history[user_id].append(response)
        
        # Update profile with new insights
        updates = {}
        for dimension, impact in impacts.items():
            if dimension == 'human_probability':
                self.profile_matrix.update_human_probability(
                    user_id,
                    impact,
                    confidence_scores.get(dimension, 0.5)
                )
            else:
                self.profile_matrix.update_profile(
                    user_id,
                    dimension,
                    impact,
                    confidence_scores.get(dimension, 0.5)
                )
                updates[dimension] = (impact, confidence_scores.get(dimension, 0.5))
                
        return updates
        
    def generate_followup_question(
        self,
        user_id: str,
        base_question: Question,
        response: int
    ) -> Optional[Question]:
        """Generate a contextual follow-up question based on the response pattern."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return None
            
        # Analyze the response pattern
        history = self.response_history.get(user_id, [])
        if len(history) < 2:
            return None
            
        # Look for interesting patterns
        patterns = self._analyze_response_patterns(history)
        if not patterns:
            return None
            
        # Select most relevant pattern for follow-up
        primary_pattern = max(patterns, key=lambda p: p[1])
        dimension, pattern_strength = primary_pattern
        
        # Find a question that explores this dimension more deeply
        available_questions = [
            q for q in self.base_questionnaire.questions
            if q.id not in {resp.question.id for resp in history}
            and dimension in q.dimension_impacts
            and q.dimension_impacts[dimension] > 0.7
        ]
        
        if not available_questions:
            return None
            
        # Return the most relevant follow-up question
        return max(
            available_questions,
            key=lambda q: q.dimension_impacts[dimension]
        )
        
    def _get_low_confidence_dimensions(
        self,
        profile: 'BehavioralProfile'
    ) -> Set[ProfileDimension]:
        """Identify dimensions that need more confidence."""
        return {
            dim for dim, conf in profile.confidence_scores.items()
            if conf < self.min_confidence_threshold
        }
        
    def _calculate_question_relevance(
        self,
        question: Question,
        low_confidence_dimensions: Set[ProfileDimension],
        profile: 'BehavioralProfile'
    ) -> float:
        """Calculate how relevant a question is for the current profile state."""
        relevance_score = 0.0
        
        # Higher score for questions targeting low confidence dimensions
        for dimension, impact in question.dimension_impacts.items():
            if dimension in low_confidence_dimensions:
                relevance_score += impact * 2.0
            else:
                relevance_score += impact * 0.5
                
        # Adjust based on profile values
        for dimension, impact in question.dimension_impacts.items():
            profile_value = profile.dimensions.get(dimension, 0.5)
            # Higher score for dimensions with extreme values
            extremity = abs(profile_value - 0.5) * 2
            relevance_score += impact * extremity
            
        return relevance_score
        
    def _calculate_history_confidence(
        self,
        user_id: str,
        dimension: ProfileDimension,
        current_question: Question,
        current_option: int
    ) -> float:
        """Calculate confidence adjustment based on response history."""
        history = self.response_history.get(user_id, [])
        if not history:
            return 0.0
            
        # Look for consistent patterns in responses
        dimension_responses = [
            resp for resp in history
            if dimension in resp.dimension_impacts
        ]
        
        if not dimension_responses:
            return 0.0
            
        # Calculate consistency of responses
        impacts = [resp.dimension_impacts[dimension] for resp in dimension_responses]
        consistency = 1.0 - np.std(impacts)
        
        # More confidence if responses have been consistent
        return consistency * 0.3
        
    def _analyze_response_patterns(
        self,
        history: List[QuestionResponse]
    ) -> List[Tuple[ProfileDimension, float]]:
        """Analyze response history for interesting patterns."""
        patterns = []
        
        # Group responses by dimension
        dimension_responses: Dict[ProfileDimension, List[float]] = {}
        for resp in history:
            for dim, impact in resp.dimension_impacts.items():
                if dim == 'human_probability':
                    continue
                if dim not in dimension_responses:
                    dimension_responses[dim] = []
                dimension_responses[dim].append(impact)
                
        # Look for strong trends or interesting patterns
        for dimension, impacts in dimension_responses.items():
            if len(impacts) < 2:
                continue
                
            # Calculate trend strength
            trend = np.polyfit(range(len(impacts)), impacts, 1)[0]
            variance = np.var(impacts)
            
            # Strong trends or high variance are interesting
            pattern_strength = abs(trend) + variance
            if pattern_strength > 0.3:  # Threshold for "interesting" patterns
                patterns.append((dimension, pattern_strength))
                
        return sorted(patterns, key=lambda x: x[1], reverse=True) 