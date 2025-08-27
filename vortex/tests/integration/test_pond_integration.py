"""Integration tests for the pond system and its interactions."""

import unittest
from typing import Dict
from vortex.src.zones.harmony_pond import HarmonyPond
from vortex.src.zones.wisdom_pond import WisdomPond
from vortex.src.zones.mercy_pond import MercyPond
from vortex.src.core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from vortex.src.core.user_profiling.adaptive_learning import LearningPathNode
from vortex.src.core.user_profiling.personalization import ContentItem

class TestPondIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment with real pond components."""
        self.profile_matrix = ProfileMatrix()
        self.harmony_pond = HarmonyPond()
        self.wisdom_pond = WisdomPond()
        self.mercy_pond = MercyPond()
        self.test_user_id = "test_user_789"
        
        # Initialize a basic profile
        self.basic_profile = {
            ProfileDimension.EMPATHY: 0.4,
            ProfileDimension.CREATIVITY: 0.4,
            ProfileDimension.STRATEGIC_THINKING: 0.4,
            ProfileDimension.MORAL_ALIGNMENT: 0.4,
            ProfileDimension.EMOTIONAL_RESPONSE: 0.4,
            ProfileDimension.WISDOM: 0.4,
            ProfileDimension.COMPREHENSION: 0.4
        }
        self.profile_matrix.update_profile(self.test_user_id, self.basic_profile)
    
    def test_pond_initialization_consistency(self):
        """Test that ponds initialize with consistent and valid states."""
        # Verify Harmony Pond initialization
        self.assertIsNotNone(self.harmony_pond.learning_nodes)
        self.assertTrue(all(isinstance(node, LearningPathNode) 
                          for node in self.harmony_pond.learning_nodes.values()))
        
        # Verify dimension weights are valid
        self.assertAlmostEqual(sum(self.harmony_pond.dimension_weights.values()), 1.0, 
                             places=2)
        
        # Verify required dimensions are properly configured
        for dim in self.harmony_pond.required_dimensions:
            self.assertIn(dim, self.harmony_pond.dimension_weights)
            self.assertIn(dim, self.harmony_pond.min_dimension_values)
    
    def test_cross_pond_progression(self):
        """Test progression and interactions between different ponds."""
        # Start with basic profile meeting minimum requirements
        initial_profile = self.basic_profile.copy()
        
        # Test progression through Harmony Pond
        guidance = self.harmony_pond.get_guidance_message(initial_profile)
        self.assertIsNotNone(guidance)
        
        # Simulate progress in Harmony Pond
        advanced_profile = initial_profile.copy()
        advanced_profile.update({
            ProfileDimension.EMPATHY: 0.7,
            ProfileDimension.CREATIVITY: 0.7,
            ProfileDimension.STRATEGIC_THINKING: 0.7
        })
        
        # Verify guidance changes with progress
        advanced_guidance = self.harmony_pond.get_guidance_message(advanced_profile)
        self.assertNotEqual(guidance, advanced_guidance)
        
        # Test interaction with Wisdom Pond
        wisdom_guidance = self.wisdom_pond.get_guidance_message(advanced_profile)
        self.assertIsNotNone(wisdom_guidance)
    
    def test_learning_path_validation(self):
        """Test the validity and progression of learning paths across ponds."""
        # Verify all nodes have valid next_nodes references
        for node_id, node in self.harmony_pond.learning_nodes.items():
            for next_node_id in node.next_nodes:
                self.assertIn(next_node_id, self.harmony_pond.learning_nodes)
        
        # Test node content validity
        for node in self.harmony_pond.learning_nodes.values():
            content = node.content
            self.assertIsInstance(content, ContentItem)
            self.assertTrue(0 <= content.difficulty_level <= 1.0)
            self.assertTrue(all(0 <= weight <= 1.0 
                              for weight in content.dimension_weights.values()))
    
    def test_profile_dimension_impacts(self):
        """Test how profile dimensions affect pond interactions."""
        # Test with insufficient profile
        low_profile = {dim: 0.1 for dim in self.basic_profile.keys()}
        
        # Verify guidance reflects insufficient progress
        low_guidance = self.harmony_pond.get_guidance_message(low_profile)
        self.assertIn("balance", low_guidance.lower())
        
        # Test with advanced profile
        high_profile = {dim: 0.9 for dim in self.basic_profile.keys()}
        high_guidance = self.harmony_pond.get_guidance_message(high_profile)
        
        # Verify different guidance for different profile levels
        self.assertNotEqual(low_guidance, high_guidance)
    
    def test_error_handling_and_consistency(self):
        """Test error handling and state consistency across pond operations."""
        # Test with invalid profile dimensions
        invalid_profile = {"invalid_dimension": 0.5}
        with self.assertRaises(ValueError):
            self.harmony_pond.get_guidance_message(invalid_profile)
        
        # Test with out-of-range values
        invalid_values = self.basic_profile.copy()
        invalid_values[ProfileDimension.EMPATHY] = 1.5
        with self.assertRaises(ValueError):
            self.harmony_pond.get_guidance_message(invalid_values)
        
        # Verify pond state remains consistent after errors
        self.test_pond_initialization_consistency()  # Should still pass 