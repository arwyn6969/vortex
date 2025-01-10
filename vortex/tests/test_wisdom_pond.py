import unittest
from unittest.mock import Mock, patch
from ..src.zones.wisdom_pond import WisdomPond
from ..src.core.user_profiling.profile_matrix import ProfileDimension
from ..src.core.exceptions import GuidanceError

class TestWisdomPond(unittest.TestCase):
    def setUp(self):
        self.pond = WisdomPond()
        self.valid_profile = {
            ProfileDimension.STRATEGIC_THINKING: 0.7,
            ProfileDimension.DECISION_MAKING: 0.6,
            ProfileDimension.EMPATHY: 0.5,
            ProfileDimension.CREATIVITY: 0.4
        }
        
    def test_empty_profile(self):
        """Test guidance message generation with empty profile."""
        with self.assertRaises(GuidanceError) as context:
            self.pond.get_guidance_message({})
        self.assertIn("Empty profile provided", str(context.exception))
        
    def test_invalid_profile_values(self):
        """Test guidance message generation with invalid profile values."""
        invalid_profile = self.valid_profile.copy()
        invalid_profile[ProfileDimension.EMPATHY] = 1.5
        
        with self.assertRaises(GuidanceError) as context:
            self.pond.get_guidance_message(invalid_profile)
        self.assertIn("Invalid profile values", str(context.exception))
        
    @patch('logging.Logger.error')
    def test_mastery_progress_error(self, mock_error):
        """Test handling of mastery progress calculation error."""
        self.pond.calculate_mastery_progress = Mock(side_effect=Exception("Test error"))
        
        message = self.pond.get_guidance_message(self.valid_profile)
        mock_error.assert_called_with("Failed to calculate mastery progress: Test error")
        self.assertIn("Focus on understanding patterns", message)
        
    def test_guidance_message_beginner(self):
        """Test guidance message for beginner level."""
        self.pond.calculate_mastery_progress = Mock(return_value=0.2)
        
        # Test strategic < decision
        profile = self.valid_profile.copy()
        profile[ProfileDimension.STRATEGIC_THINKING] = 0.3
        profile[ProfileDimension.DECISION_MAKING] = 0.6
        
        message = self.pond.get_guidance_message(profile)
        self.assertIn("Focus on understanding patterns", message)
        
        # Test strategic > decision
        profile[ProfileDimension.STRATEGIC_THINKING] = 0.7
        profile[ProfileDimension.DECISION_MAKING] = 0.3
        
        message = self.pond.get_guidance_message(profile)
        self.assertIn("Your strategic mind is growing", message)
        
    def test_guidance_message_intermediate(self):
        """Test guidance message for intermediate level."""
        self.pond.calculate_mastery_progress = Mock(return_value=0.5)
        
        # Test strategic < 0.6
        profile = self.valid_profile.copy()
        profile[ProfileDimension.STRATEGIC_THINKING] = 0.5
        
        message = self.pond.get_guidance_message(profile)
        self.assertIn("begin to see the deeper patterns", message)
        
        # Test strategic >= 0.6
        profile[ProfileDimension.STRATEGIC_THINKING] = 0.7
        
        message = self.pond.get_guidance_message(profile)
        self.assertIn("Your mastery grows", message)
        
    def test_guidance_message_advanced(self):
        """Test guidance message for advanced level."""
        self.pond.calculate_mastery_progress = Mock(return_value=0.7)
        
        message = self.pond.get_guidance_message(self.valid_profile)
        self.assertIn("The pond's wisdom flows through you", message)
        
    def test_guidance_message_master(self):
        """Test guidance message for master level."""
        self.pond.calculate_mastery_progress = Mock(return_value=0.95)
        
        message = self.pond.get_guidance_message(self.valid_profile)
        self.assertIn("You have become one with the pond's wisdom", message)
        
    def test_detailed_analysis(self):
        """Test detailed analysis in guidance message."""
        self.pond.calculate_mastery_progress = Mock(return_value=0.5)
        
        message = self.pond.get_guidance_message(
            self.valid_profile,
            include_detailed_analysis=True
        )
        
        self.assertIn("Detailed Analysis:", message)
        self.assertIn("exceptional (0.70)", message)  # Strategic thinking
        self.assertIn("developing well (0.60)", message)  # Decision making
        self.assertIn("developing well (0.50)", message)  # Empathy
        self.assertIn("developing well (0.40)", message)  # Creativity 