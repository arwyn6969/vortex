"""Integration tests for behavioral analysis system."""

import unittest
from datetime import datetime
import numpy as np
from vortex.src.core.user_profiling.behavioral_analysis import BehavioralAnalysis
from vortex.src.core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from vortex.src.core.user_profiling.questionnaire import VoightKampffQuestionnaire

class TestBehavioralIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment with real components."""
        self.profile_matrix = ProfileMatrix()
        self.analysis = BehavioralAnalysis(self.profile_matrix)
        self.questionnaire = VoightKampffQuestionnaire()
        self.test_user_id = "test_user_456"
        
    def test_questionnaire_behavior_integration(self):
        """Test integration between questionnaire responses and behavioral analysis."""
        # First, record questionnaire responses
        question = self.questionnaire.get_question(0)
        response_impacts = self.questionnaire.analyze_response(question, 0)
        
        # Record the questionnaire interaction
        self.analysis.record_interaction(
            self.test_user_id,
            "questionnaire_response",
            "initial_assessment",
            2.5,  # Simulated response time
            {
                "question_id": question.id,
                "response_index": 0,
                "impacts": response_impacts
            }
        )
        
        # Verify profile was updated
        profile = self.profile_matrix.get_profile(self.test_user_id)
        self.assertIsNotNone(profile)
        self.assertGreater(profile.interaction_count, 0)
        
    def test_behavioral_profile_evolution(self):
        """Test how behavioral analysis affects profile over time."""
        # Record a series of interactions simulating a session
        interaction_types = [
            ("quick_response", 0.5),
            ("thoughtful_response", 3.0),
            ("emotional_response", 1.5),
            ("analytical_response", 2.0)
        ]
        
        initial_profile = None
        final_profile = None
        
        for event_type, duration in interaction_types:
            self.analysis.record_interaction(
                self.test_user_id,
                event_type,
                "session_flow",
                duration,
                {
                    "response_text": f"Test response for {event_type}",
                    "emotional_value": 0.7 if "emotional" in event_type else 0.3
                }
            )
            
            if initial_profile is None:
                initial_profile = self.profile_matrix.get_profile(self.test_user_id)
            final_profile = self.profile_matrix.get_profile(self.test_user_id)
            
        # Verify profile evolution
        self.assertNotEqual(
            initial_profile.dimensions[ProfileDimension.EMOTIONAL_RESPONSE],
            final_profile.dimensions[ProfileDimension.EMOTIONAL_RESPONSE]
        )
        
    def test_cross_component_consistency(self):
        """Test consistency of behavioral analysis across components."""
        # Record interactions that should affect multiple profile dimensions
        contexts = ["strategic", "emotional", "creative"]
        responses = [
            "Let me analyze this situation",
            "I feel strongly about this",
            "Here's an innovative solution"
        ]
        
        for context, text in zip(contexts, responses):
            # Record interaction
            self.analysis.record_interaction(
                self.test_user_id,
                f"{context}_response",
                context,
                1.5,
                {"response_text": text}
            )
            
            # Record related questionnaire response
            question = self.questionnaire.get_question(0)
            impacts = self.questionnaire.analyze_response(question, 0)
            
            self.analysis.record_interaction(
                self.test_user_id,
                "questionnaire_response",
                context,
                2.0,
                {
                    "question_id": question.id,
                    "response_index": 0,
                    "impacts": impacts
                }
            )
            
        # Verify profile consistency
        profile = self.profile_matrix.get_profile(self.test_user_id)
        
        # Check that related dimensions are affected consistently
        strategic = profile.dimensions[ProfileDimension.STRATEGIC_THINKING]
        emotional = profile.dimensions[ProfileDimension.EMOTIONAL_RESPONSE]
        creative = profile.dimensions[ProfileDimension.CREATIVITY]
        
        # Verify reasonable value ranges and relationships
        self.assertGreaterEqual(strategic, 0.0)
        self.assertLessEqual(strategic, 1.0)
        self.assertGreaterEqual(emotional, 0.0)
        self.assertLessEqual(emotional, 1.0)
        self.assertGreaterEqual(creative, 0.0)
        self.assertLessEqual(creative, 1.0)
        
    def test_long_term_behavioral_patterns(self):
        """Test detection and analysis of long-term behavioral patterns."""
        # Simulate interactions over multiple sessions
        session_counts = 3
        interactions_per_session = 5
        
        for session in range(session_counts):
            # Simulate session start
            self.analysis.record_interaction(
                self.test_user_id,
                "session_start",
                "login",
                0.5
            )
            
            # Record session interactions
            for i in range(interactions_per_session):
                response_time = 1.0 + np.random.normal(0, 0.2)  # Varied response times
                self.analysis.record_interaction(
                    self.test_user_id,
                    "session_interaction",
                    f"context_{i}",
                    response_time,
                    {
                        "session_id": session,
                        "interaction_index": i,
                        "response_text": f"Response {i} in session {session}"
                    }
                )
                
            # Simulate session end
            self.analysis.record_interaction(
                self.test_user_id,
                "session_end",
                "logout",
                0.5
            )
            
        # Verify long-term pattern analysis
        profile = self.profile_matrix.get_profile(self.test_user_id)
        
        # Check interaction count
        expected_interactions = session_counts * (interactions_per_session + 2)  # +2 for login/logout
        self.assertEqual(profile.interaction_count, expected_interactions)
        
        # Verify confidence scores increased with more interactions
        for confidence in profile.confidence_scores.values():
            self.assertGreater(confidence, 0.5)  # Expect higher confidence with more data
            
    def test_error_recovery_and_consistency(self):
        """Test system recovery and data consistency after errors."""
        # Simulate normal interaction
        self.analysis.record_interaction(
            self.test_user_id,
            "normal_interaction",
            "test",
            1.0,
            {"status": "success"}
        )
        
        # Simulate error condition
        try:
            self.analysis.record_interaction(
                self.test_user_id,
                "error_interaction",
                "test",
                -1.0,  # Invalid duration
                {"status": "error"}
            )
        except ValueError:
            pass
            
        # Verify system state remains consistent
        events = self.analysis.interaction_history[self.test_user_id]
        self.assertEqual(len(events), 1)  # Only successful interaction recorded
        self.assertEqual(events[0].event_type, "normal_interaction")
        
        # Verify profile remains valid
        profile = self.profile_matrix.get_profile(self.test_user_id)
        self.assertIsNotNone(profile)
        
        # Continue with valid interaction after error
        self.analysis.record_interaction(
            self.test_user_id,
            "recovery_interaction",
            "test",
            1.0,
            {"status": "recovered"}
        )
        
        # Verify system recovered and continued normally
        events = self.analysis.interaction_history[self.test_user_id]
        self.assertEqual(len(events), 2)
        self.assertEqual(events[-1].event_type, "recovery_interaction")

if __name__ == '__main__':
    unittest.main() 