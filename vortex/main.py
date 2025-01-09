#!/usr/bin/env python3
"""
Vortex of Enlightenment - A text-based journey through mystical ponds.
"""
import sys
import signal
import atexit
from typing import Optional
from src.core.user_profiling.profile_matrix import ProfileMatrix
from src.core.user_profiling.questionnaire import VoightKampffQuestionnaire
from src.core.user_profiling.behavioral_analysis import BehavioralAnalysis
from src.core.user_profiling.personalization import PersonalizationEngine, ContentItem

class VortexProfiler:
    """Manages the behavioral profiling system."""
    
    def __init__(self):
        self.profile_matrix = ProfileMatrix()
        self.questionnaire = VoightKampffQuestionnaire()
        self.behavioral_analysis = BehavioralAnalysis(self.profile_matrix)
        self.personalization = PersonalizationEngine(self.profile_matrix)
        
    def cleanup(self):
        """Cleanup resources on exit."""
        # Add persistence logic here if needed
        print("\nCleaning up resources...")
        
    def handle_questionnaire(self, user_id: str) -> None:
        """Process questionnaire responses with error handling."""
        try:
            for i in range(5):
                question = self.questionnaire.get_question(i)
                if not question:
                    continue
                    
                # Simulate user response (in real app, this would come from user input)
                response_index = 0  # Example: always choose first option
                impacts = self.questionnaire.analyze_response(question, response_index)
                
                # Update profile based on response
                for dim, value in impacts.items():
                    if dim == 'human_probability':
                        self.profile_matrix.update_human_probability(
                            user_id,
                            value,
                            confidence=0.5
                        )
        except ValueError as e:
            print(f"Error processing questionnaire: {e}")
        except Exception as e:
            print(f"Unexpected error in questionnaire: {e}")
            
    def record_user_interaction(
        self,
        user_id: str,
        event_type: str,
        context: str,
        duration: float,
        metadata: Optional[dict] = None
    ) -> None:
        """Record user interaction with error handling."""
        try:
            self.behavioral_analysis.record_interaction(
                user_id,
                event_type,
                context,
                duration,
                metadata
            )
        except Exception as e:
            print(f"Error recording interaction: {e}")
            
    def get_content_recommendation(
        self,
        user_id: str,
        category: str
    ) -> None:
        """Get and display content recommendations."""
        try:
            recommended_content = self.personalization.get_personalized_content(
                user_id,
                category
            )
            
            if recommended_content:
                print(f"Recommended content: {recommended_content[0].content}")
            else:
                print("No content recommendations available.")
                
        except Exception as e:
            print(f"Error getting content recommendation: {e}")

def signal_handler(signum, frame):
    """Handle interrupt signals."""
    print("\nReceived interrupt signal. Cleaning up...")
    sys.exit(0)

def main():
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        profiler = VortexProfiler()
        atexit.register(profiler.cleanup)
        
        # Example user
        user_id = "user123"
        
        # Process questionnaire
        profiler.handle_questionnaire(user_id)
        
        # Record interactions
        profiler.record_user_interaction(
            user_id,
            "puzzle_solve",
            "maze_level_1",
            duration=5.2,
            metadata={"success": True, "emotional_value": 0.7}
        )
        
        profiler.record_user_interaction(
            user_id,
            "story_choice",
            "chapter_1_dilemma",
            duration=3.1,
            metadata={"choice": "help_stranger", "emotional_value": 0.9}
        )
        
        # Register example content
        try:
            content_item = ContentItem(
                content_id="puzzle_1",
                content="Complex maze puzzle",
                dimension_weights={
                    ProfileDimension.STRATEGIC_THINKING: 0.5,
                    ProfileDimension.CREATIVITY: 0.2,
                    ProfileDimension.DECISION_MAKING: 0.3
                },
                difficulty_level=0.7,
                emotional_intensity=0.3,
                creativity_required=0.5,
                strategic_depth=0.8
            )
            
            profiler.personalization.register_content("puzzles", content_item)
        except ValueError as e:
            print(f"Error registering content: {e}")
            return
            
        # Get recommendations
        profiler.get_content_recommendation(user_id, "puzzles")
        
        # Get difficulty and emotional intensity
        try:
            difficulty = profiler.personalization.adapt_difficulty(
                user_id,
                0.5,
                0.8
            )
            print(f"Adapted difficulty level: {difficulty}")
            
            emotional_level = profiler.personalization.get_emotional_intensity(
                user_id
            )
            print(f"Recommended emotional intensity: {emotional_level}")
            
        except Exception as e:
            print(f"Error calculating adaptations: {e}")
            
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 