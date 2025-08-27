import unittest
from unittest.mock import Mock, patch
from vortex.src.zones.harmony_pond import HarmonyPond
from vortex.src.core.player import Player
from vortex.src.core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from vortex.src.core.exceptions import NodeSetupError

class TestHarmonyPond(unittest.TestCase):
    def setUp(self):
        self.pond = HarmonyPond()
        
    def test_node_validation_weights(self):
        """Test node validation for dimension weights."""
        mock_node = Mock()
        mock_node.node_id = "test_node"
        mock_node.content.dimension_weights = {
            ProfileDimension.EMPATHY: 0.3,
            ProfileDimension.CREATIVITY: 0.3,
            ProfileDimension.STRATEGIC_THINKING: 0.3
        }
        mock_node.required_dimensions = {
            ProfileDimension.EMPATHY: 0.5
        }
        mock_node.next_nodes = []
        
        with self.assertRaises(NodeSetupError) as context:
            self.pond._validate_node(mock_node)
        self.assertIn("sum to 0.9", str(context.exception))
        
    def test_node_validation_missing_dimensions(self):
        """Test node validation for missing required dimensions."""
        mock_node = Mock()
        mock_node.node_id = "test_node"
        mock_node.content.dimension_weights = {
            ProfileDimension.EMPATHY: 0.5,
            ProfileDimension.CREATIVITY: 0.5
        }
        mock_node.required_dimensions = {
            ProfileDimension.STRATEGIC_THINKING: 0.5
        }
        mock_node.next_nodes = []
        
        with self.assertRaises(NodeSetupError) as context:
            self.pond._validate_node(mock_node)
        self.assertIn("not found in weights", str(context.exception))
        
    def test_node_validation_next_nodes(self):
        """Test node validation for next_nodes type."""
        mock_node = Mock()
        mock_node.node_id = "test_node"
        mock_node.content.dimension_weights = {
            ProfileDimension.EMPATHY: 0.5,
            ProfileDimension.CREATIVITY: 0.5
        }
        mock_node.required_dimensions = {
            ProfileDimension.EMPATHY: 0.5
        }
        mock_node.next_nodes = "invalid"
        
        with self.assertRaises(NodeSetupError) as context:
            self.pond._validate_node(mock_node)
        self.assertIn("must be a list", str(context.exception))
        
    def test_setup_learning_nodes(self):
        """Test successful learning nodes setup."""
        self.pond._setup_learning_nodes()
        
        # Verify all expected nodes are created
        expected_nodes = [
            "harmony_initial",
            "harmony_integration",
            "harmony_flow",
            "harmony_resonance"
        ]
        
        for node_id in expected_nodes:
            self.assertIn(node_id, self.pond.learning_nodes)
            
        # Verify node connections
        initial_node = self.pond.learning_nodes["harmony_initial"]
        self.assertIn("harmony_integration", initial_node.next_nodes)
        self.assertIn("harmony_flow", initial_node.next_nodes)
        
    @patch('logging.Logger.error')
    def test_setup_learning_nodes_error(self, mock_error):
        """Test error handling in learning nodes setup."""
        # Mock _validate_node to raise an error
        self.pond._validate_node = Mock(side_effect=NodeSetupError("Test error"))
        
        with self.assertRaises(NodeSetupError):
            self.pond._setup_learning_nodes()
            
        mock_error.assert_called_with("Failed to set up learning nodes: Test error")
        
    def test_node_dimension_weights(self):
        """Test dimension weights validation for all nodes."""
        self.pond._setup_learning_nodes()
        
        for node_id, node in self.pond.learning_nodes.items():
            weights_sum = sum(node.content.dimension_weights.values())
            self.assertAlmostEqual(
                weights_sum,
                1.0,
                places=2,
                msg=f"Node {node_id} weights do not sum to 1.0"
            ) 