import unittest
from ..src.core.user_profiling.profile_matrix import ProfileDimension, BehavioralProfile
from typing import Dict
import time

class TestProfileMatrix(unittest.TestCase):
    def setUp(self):
        self.test_user_id = "test_user_123"
        self.test_dimensions: Dict[ProfileDimension, float] = {
            ProfileDimension.EMPATHY: 0.7,
            ProfileDimension.DECISION_MAKING: 0.6,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.5,
            ProfileDimension.CREATIVITY: 0.8,
            ProfileDimension.RISK_TOLERANCE: 0.4,
            ProfileDimension.STRATEGIC_THINKING: 0.6,
            ProfileDimension.MORAL_ALIGNMENT: 0.7
        }
        self.test_confidence = {dim: 0.8 for dim in ProfileDimension}
        self.current_time = time.time()

    def test_behavioral_profile_creation(self):
        """Test creation of BehavioralProfile with valid data."""
        profile = BehavioralProfile(
            user_id=self.test_user_id,
            dimensions=self.test_dimensions,
            confidence_scores=self.test_confidence,
            is_human_probability=0.95,
            last_updated=self.current_time,
            interaction_count=1
        )
        
        self.assertEqual(profile.user_id, self.test_user_id)
        self.assertEqual(profile.dimensions, self.test_dimensions)
        self.assertEqual(profile.confidence_scores, self.test_confidence)
        self.assertEqual(profile.is_human_probability, 0.95)
        self.assertEqual(profile.interaction_count, 1)

    def test_profile_dimension_values(self):
        """Test that profile dimension values are within valid range."""
        for value in self.test_dimensions.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_confidence_score_values(self):
        """Test that confidence scores are within valid range."""
        for value in self.test_confidence.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_profile_dimension_completeness(self):
        """Test that all ProfileDimension enum values are accounted for."""
        all_dimensions = set(ProfileDimension)
        profile_dimensions = set(self.test_dimensions.keys())
        self.assertEqual(all_dimensions, profile_dimensions)

if __name__ == '__main__':
    unittest.main() 