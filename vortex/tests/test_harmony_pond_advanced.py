"""Tests for advanced functionality of the Harmony Pond zone."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from vortex.src.zones.harmony_pond import HarmonyPond
from vortex.src.core.player import Player
from vortex.src.core.user_profiling.profile_matrix import ProfileDimension
from vortex.src.core.user_profiling.adaptive_learning import LearningPathNode
from vortex.src.core.user_profiling.personalization import ContentItem
from vortex.src.core.exceptions import NodeSetupError
from vortex.src.core.profiling.performance_monitor import performance_monitor

class TestHarmonyPondAdvanced(unittest.TestCase):
    """Test suite for advanced Harmony Pond functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pond = HarmonyPond()
        self.valid_profile = {
            ProfileDimension.EMPATHY: 0.6,
            ProfileDimension.CREATIVITY: 0.5,
            ProfileDimension.STRATEGIC_THINKING: 0.7,
            ProfileDimension.MORAL_ALIGNMENT: 0.4,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.5
        }
        
    def test_initialization_validation(self):
        """Test validation during initialization."""
        with patch.dict(HarmonyPond.dimension_weights, {ProfileDimension.EMPATHY: 0.5}):
            with self.assertRaises(ValueError) as context:
                HarmonyPond()
            self.assertIn("must sum to 1.0", str(context.exception))
    
    def test_guidance_message_validation(self):
        """Test input validation for guidance message generation."""
        # Test invalid profile type
        with self.assertRaises(TypeError):
            self.pond.get_guidance_message([])  # type: ignore
            
        # Test invalid dimension values
        invalid_profile = self.valid_profile.copy()
        invalid_profile[ProfileDimension.EMPATHY] = 1.5
        with self.assertRaises(ValueError):
            self.pond.get_guidance_message(invalid_profile)
            
        # Test non-numeric values
        invalid_profile = self.valid_profile.copy()
        invalid_profile[ProfileDimension.EMPATHY] = "invalid"  # type: ignore
        with self.assertRaises(ValueError):
            self.pond.get_guidance_message(invalid_profile)
    
    def test_detailed_analysis(self):
        """Test detailed analysis in guidance messages."""
        message = self.pond.get_guidance_message(
            self.valid_profile,
            include_detailed_analysis=True
        )
        
        # Check for analysis sections
        self.assertIn("Dimensional Analysis:", message)
        self.assertIn("Exceptional Qualities:", message)
        self.assertIn("Developing Well:", message)
        self.assertIn("Harmony Analysis:", message)
        
        # Check specific dimension reporting
        self.assertIn("strategic_thinking: 0.70", message.lower())
        self.assertIn("Balance Rating:", message)
        self.assertIn("Overall Progress:", message)
    
    def test_node_validation_comprehensive(self):
        """Test comprehensive node validation."""
        mock_node = Mock(spec=LearningPathNode)
        mock_node.node_id = "test_node"
        mock_node.content = Mock(spec=ContentItem)
        mock_node.content.dimension_weights = {
            ProfileDimension.EMPATHY: 0.5,
            ProfileDimension.CREATIVITY: 0.5
        }
        mock_node.required_dimensions = {
            ProfileDimension.EMPATHY: 0.4
        }
        mock_node.next_nodes = []
        mock_node.content.difficulty_level = 0.5
        mock_node.content.emotional_intensity = 0.5
        mock_node.content.creativity_required = 0.5
        mock_node.content.strategic_depth = 0.5
        
        # Test valid node
        self.pond._validate_node(mock_node)  # Should not raise
        
        # Test invalid content attributes
        mock_node.content.difficulty_level = 1.5
        with self.assertRaises(ValueError):
            self.pond._validate_node(mock_node)
            
        mock_node.content.difficulty_level = 0.5
        mock_node.content.emotional_intensity = "invalid"  # type: ignore
        with self.assertRaises(ValueError):
            self.pond._validate_node(mock_node)
    
    def test_performance_monitoring(self):
        """Test performance monitoring integration."""
        # Clear existing metrics
        performance_monitor.metrics.clear()
        
        # Generate guidance message
        self.pond.get_guidance_message(self.valid_profile)
        
        # Check metrics were recorded
        self.assertIn("harmony_guidance_generation", performance_monitor.metrics)
        
        # Get summary
        summary = performance_monitor.get_summary()
        self.assertIn("harmony_guidance_generation", summary)
        self.assertTrue(all(key in summary["harmony_guidance_generation"] 
                          for key in ["avg", "min", "max", "count"]))
    
    def test_progress_calculation(self):
        """Test progress calculation with different profiles."""
        test_cases = [
            # Low progress case
            ({dim: 0.2 for dim in self.valid_profile}, 0.3),
            # Medium progress case
            ({dim: 0.5 for dim in self.valid_profile}, 0.6),
            # High progress case
            ({dim: 0.8 for dim in self.valid_profile}, 0.9)
        ]
        
        for profile, expected_threshold in test_cases:
            message = self.pond.get_guidance_message(profile)
            if expected_threshold == 0.3:
                self.assertIn("balance your inner waters", message)
            elif expected_threshold == 0.6:
                self.assertIn("maintain the harmony", message)
            else:
                self.assertIn("perfect harmony", message)
    
    @patch('logging.Logger.debug')
    def test_logging_integration(self, mock_debug):
        """Test logging integration."""
        self.pond.get_guidance_message(self.valid_profile)
        mock_debug.assert_called()
        
        # Check log message content
        log_message = mock_debug.call_args[0][0]
        self.assertIn("Generated guidance message", log_message)
        self.assertIn("balance rating", log_message)
    
    def test_node_setup_error_handling(self):
        """Test error handling during node setup."""
        with patch.object(HarmonyPond, '_validate_node') as mock_validate:
            mock_validate.side_effect = NodeSetupError("Test error")
            
            with self.assertRaises(NodeSetupError) as context:
                self.pond._setup_learning_nodes()
            
            self.assertIn("Test error", str(context.exception))
    
    def tearDown(self):
        """Clean up after tests."""
        performance_monitor.metrics.clear() 