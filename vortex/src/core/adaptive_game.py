from typing import Dict, Optional
import time

from .ui.terminal import TerminalUI
from .user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from .user_profiling.questionnaire import VoightKampffQuestionnaire
from .user_profiling.adaptive_questionnaire import AdaptiveQuestionnaire

class AdaptiveGame:
    """Game implementation with adaptive questioning and profiling."""
    
    def __init__(self):
        self.ui = TerminalUI()
        self.profile_matrix = ProfileMatrix()
        self.base_questionnaire = VoightKampffQuestionnaire()
        self.adaptive_questionnaire = AdaptiveQuestionnaire(
            base_questionnaire=self.base_questionnaire,
            profile_matrix=self.profile_matrix,
            min_confidence_threshold=0.6,
            max_questions=20
        )
        
    def run_adaptive_questionnaire(self, user_id: str) -> Optional[Dict[ProfileDimension, float]]:
        """Run an adaptive questionnaire session."""
        try:
            self.ui.display_text(
                "\nWelcome to the Vortex of Enlightenment. "
                "I will present you with a series of scenarios, "
                "adapting to your responses to better understand your path. "
                "Please answer thoughtfully and honestly - there are no right or wrong answers."
            )
            
            question_count = 0
            while question_count < self.adaptive_questionnaire.max_questions:
                # Get next question
                question = self.adaptive_questionnaire.get_next_question(user_id)
                if not question:
                    break
                    
                # Display question with context
                if question.context:
                    self.ui.display_text(f"\n{question.context}")
                self.ui.display_text(f"\n{question.text}")
                
                # Get response
                try:
                    response = self.ui.prompt("\nYour response: ")
                    if not response.strip():
                        self.ui.display_text("Please provide a response.")
                        response = self.ui.prompt("\nYour response: ")
                except Exception as e:
                    self.ui.display_text(f"Error getting response: {str(e)}")
                    continue
                
                # Process response and update profile
                try:
                    updates = self.adaptive_questionnaire.process_response(
                        user_id,
                        question,
                        response
                    )
                except Exception as e:
                    self.ui.display_text(f"Error processing response: {str(e)}")
                    continue
                
                question_count += 1
                
                # Add a thoughtful pause between questions
                self.ui.display_text("\n...")
                time.sleep(2)
                
                # Display insights (optional)
                self._display_dimension_updates(updates)
            
            # Get final profile
            profile = self.profile_matrix.get_profile(user_id)
            if profile:
                self.ui.display_text("\nQuestionnaire complete. Thank you for your insights.")
                return profile.dimensions
            
            return None
            
        except Exception as e:
            self.ui.display_text(f"\nAn error occurred: {str(e)}")
            return None
            
    def _display_dimension_updates(
        self,
        updates: Dict[ProfileDimension, tuple[float, float]]
    ) -> None:
        """Display meaningful insights about dimension updates."""
        significant_updates = [
            (dim, value, conf)
            for dim, (value, conf) in updates.items()
            if conf > 0.7 or abs(value - 0.5) > 0.3
        ]
        
        if not significant_updates:
            return
            
        self.ui.display_text("\nInsights from your response:")
        for dimension, value, confidence in significant_updates:
            if confidence > 0.7:
                strength = "strong" if abs(value - 0.5) > 0.3 else "clear"
                direction = "high" if value > 0.6 else "low" if value < 0.4 else "balanced"
                self.ui.display_text(
                    f"- Showing a {strength} tendency toward {direction} "
                    f"{dimension.value.replace('_', ' ')}"
                ) 