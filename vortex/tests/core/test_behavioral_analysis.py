"""Tests for the behavioral analysis system."""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import numpy as np
from vortex.src.core.user_profiling.behavioral_analysis import (
    BehavioralAnalysis,
    InteractionEvent,
    ProfileMatrix,
    ProfileDimension
)
import logging

class TestBehavioralAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.profile_matrix = Mock(spec=ProfileMatrix)
        self.analysis = BehavioralAnalysis(
            profile_matrix=self.profile_matrix,
            max_history_age=3600  # 1 hour for testing
        )
        self.test_user_id = "test_user_123"
        self.current_time = datetime.now().timestamp()
        
        # Configure root logger for testing
        logging.basicConfig(level=logging.ERROR)
        
    def test_interaction_event_creation(self):
        """Test creation of interaction events."""
        event = InteractionEvent(
            timestamp=self.current_time,
            event_type="test_event",
            context="test_context",
            duration=1.0,
            metadata={"key": "value"}
        )
        
        self.assertEqual(event.timestamp, self.current_time)
        self.assertEqual(event.event_type, "test_event")
        self.assertEqual(event.context, "test_context")
        self.assertEqual(event.duration, 1.0)
        self.assertEqual(event.metadata, {"key": "value"})
        
    def test_record_interaction_basic(self):
        """Test basic interaction recording."""
        self.analysis.record_interaction(
            self.test_user_id,
            "test_event",
            "test_context",
            1.0,
            {"key": "value"}
        )
        
        events = self.analysis.interaction_history[self.test_user_id]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_type, "test_event")
        self.assertEqual(events[0].context, "test_context")
        
    def test_cleanup_old_events(self):
        """Test cleanup of old interaction events."""
        # Add old event
        old_time = self.current_time - 7200  # 2 hours ago
        self.analysis.interaction_history[self.test_user_id] = [
            InteractionEvent(
                timestamp=old_time,
                event_type="old_event",
                context="test",
                duration=1.0,
                metadata={}
            )
        ]
        
        # Add new event
        self.analysis.record_interaction(
            self.test_user_id,
            "new_event",
            "test",
            1.0
        )
        
        # Verify only new event remains
        events = self.analysis.interaction_history[self.test_user_id]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_type, "new_event")
        
    def test_bot_pattern_detection(self):
        """Test detection of bot-like behavior patterns."""
        # Simulate bot-like behavior with very consistent timing
        for _ in range(10):
            self.analysis.record_interaction(
                self.test_user_id,
                "repeated_action",
                "test",
                1.0,  # Exactly same duration
                {"response_text": "test"}
            )
            
        # Verify profile update reflects bot-like behavior
        self.profile_matrix.update_human_probability.assert_called_with(
            self.test_user_id,
            0.2,  # Low human probability due to consistent timing
            confidence=0.08  # 10 events = 0.08 confidence
        )
        
    def test_human_pattern_detection(self):
        """Test detection of human-like behavior patterns."""
        # Simulate human-like behavior with varied timing and responses
        durations = [1.2, 0.8, 1.5, 0.9, 1.3]
        responses = [
            "Hello there!",
            "That's interesting...",
            "I need to think about this",
            "Let me try something different",
            "This is challenging"
        ]
        
        for duration, text in zip(durations, responses):
            self.analysis.record_interaction(
                self.test_user_id,
                "varied_action",
                "test",
                duration,
                {"response_text": text}
            )
            
        # Verify profile update reflects human-like behavior
        self.profile_matrix.update_human_probability.assert_called_with(
            self.test_user_id,
            0.9,  # High human probability due to varied behavior
            confidence=0.05  # 5 events = 0.05 confidence
        )
        
    def test_edge_case_single_event(self):
        """Test handling of single interaction event."""
        self.analysis.record_interaction(
            self.test_user_id,
            "single_event",
            "test",
            1.0
        )
        
        # Verify no profile updates with insufficient data
        self.profile_matrix.update_human_probability.assert_not_called()
        
    def test_edge_case_empty_metadata(self):
        """Test handling of events with empty metadata."""
        for _ in range(5):
            self.analysis.record_interaction(
                self.test_user_id,
                "test_event",
                "test",
                1.0,
                {}  # Empty metadata
            )
            
        # Verify system still functions with missing metadata
        self.assertTrue(
            len(self.analysis.interaction_history[self.test_user_id]) > 0
        )
        
    def test_edge_case_invalid_duration(self):
        """Test handling of invalid duration values."""
        with self.assertRaises(ValueError):
            self.analysis.record_interaction(
                self.test_user_id,
                "test_event",
                "test",
                -1.0  # Invalid negative duration
            )
            
    def test_edge_case_missing_user(self):
        """Test behavior with non-existent user."""
        events = self.analysis.interaction_history.get("nonexistent_user", [])
        self.assertEqual(len(events), 0)
        
    def test_linguistic_pattern_analysis(self):
        """Test analysis of linguistic patterns."""
        # Record interactions with varied linguistic content
        responses = [
            "This is a simple response",
            "I need to carefully consider the implications of this situation",
            "The quantum nature of consciousness suggests deeper patterns",
            "Let me analyze this from multiple perspectives",
            "The synchronicity of these events is fascinating"
        ]
        
        for i, text in enumerate(responses):
            self.analysis.record_interaction(
                self.test_user_id,
                "text_response",
                "test",
                1.0,
                {"response_text": text}
            )
            
        # Get linguistic metrics
        metrics = self.analysis.analyze_linguistic_patterns(
            self.analysis.interaction_history[self.test_user_id]
        )
        
        # Verify metrics structure and ranges
        self.assertIn("vocabulary_richness", metrics)
        self.assertIn("syntactic_complexity", metrics)
        self.assertIn("emotional_content", metrics)
        self.assertIn("cognitive_indicators", metrics)
        
        for value in metrics.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)
            
    def test_timing_pattern_analysis(self):
        """Test analysis of response timing patterns."""
        # Record interactions with varied timing
        durations = [0.5, 1.2, 0.8, 1.5, 0.9]
        
        for duration in durations:
            self.analysis.record_interaction(
                self.test_user_id,
                "timed_response",
                "test",
                duration
            )
            
        # Get timing metrics
        metrics = self.analysis.analyze_response_timing_patterns(
            self.analysis.interaction_history[self.test_user_id]
        )
        
        # Verify metrics structure and ranges
        self.assertIn("consistency", metrics)
        self.assertIn("adaptability", metrics)
        self.assertIn("micro_variance", metrics)
        self.assertIn("cognitive_load", metrics)
        
        for value in metrics.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)
            
    def test_integration_profile_updates(self):
        """Test integration of behavior analysis with profile updates."""
        # Record a series of interactions that should trigger profile updates
        contexts = ["strategic", "emotional", "creative", "analytical"]
        responses = [
            "Let me think this through carefully",
            "I feel strongly about this situation",
            "Here's an innovative approach",
            "The logical conclusion would be..."
        ]
        
        for context, text in zip(contexts, responses):
            self.analysis.record_interaction(
                self.test_user_id,
                "integrated_response",
                context,
                1.0,
                {
                    "response_text": text,
                    "emotional_value": 0.7,
                    "cognitive_load": 0.6
                }
            )
            
        # Verify profile dimension updates
        self.profile_matrix.update_profile.assert_called()
        call_args = self.profile_matrix.update_profile.call_args_list
        
        # Verify updates for different dimensions
        dimensions_updated = set()
        for args, _ in call_args:
            dimensions_updated.add(args[1])  # Add the dimension argument
            
        expected_dimensions = {
            ProfileDimension.STRATEGIC_THINKING,
            ProfileDimension.EMOTIONAL_RESPONSE,
            ProfileDimension.CREATIVITY,
            ProfileDimension.CONSCIOUSNESS_DEPTH
        }
        
        self.assertTrue(
            expected_dimensions.issubset(dimensions_updated),
            "Not all expected dimensions were updated"
        )
        
    def test_error_handling_profile_update(self):
        """Test error handling during profile updates."""
        # Mock profile matrix to raise an exception
        self.profile_matrix.update_profile.side_effect = Exception("Update failed")
        
        # Record interaction that should trigger profile update
        with self.assertLogs(level='ERROR') as log:
            self.analysis.record_interaction(
                self.test_user_id,
                "error_test",
                "test",
                1.0,
                {"response_text": "test"}
            )
            
        self.assertIn("Failed to update profile", log.output[0])
        
    def test_concurrent_user_isolation(self):
        """Test isolation between different users' interaction histories."""
        user1 = "user1"
        user2 = "user2"
        
        # Record interactions for both users
        self.analysis.record_interaction(user1, "event1", "test", 1.0)
        self.analysis.record_interaction(user2, "event2", "test", 1.0)
        
        # Verify histories are separate
        self.assertEqual(
            self.analysis.interaction_history[user1][0].event_type,
            "event1"
        )
        self.assertEqual(
            self.analysis.interaction_history[user2][0].event_type,
            "event2"
        )
        
    def test_performance_large_history(self):
        """Test performance with large interaction history."""
        # Record many interactions
        start_time = datetime.now()
        for _ in range(100):
            self.analysis.record_interaction(
                self.test_user_id,
                "perf_test",
                "test",
                1.0
            )
            
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Verify reasonable processing time (adjust threshold as needed)
        self.assertLess(processing_time, 1.0)  # Should process 100 events in under 1 second

if __name__ == '__main__':
    unittest.main() 