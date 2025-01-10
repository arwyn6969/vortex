"""
Tests for sacred geometry visualization and calculations.
"""
import unittest
import math
from src.mythology import sacred_geometry

class TestSacredGeometry(unittest.TestCase):
    """Test cases for sacred geometry functionality."""
    
    def test_pattern_visualization(self):
        """Test ASCII art pattern generation."""
        # Test Kan Cross
        kan_cross = sacred_geometry.get_pattern_visualization("kan_cross")
        self.assertEqual(len(kan_cross), 7)  # Should have 7 lines
        self.assertTrue(any("†" in line for line in kan_cross))  # Should contain crosses
        
        # Test Quincunx
        quincunx = sacred_geometry.get_pattern_visualization("quincunx")
        self.assertEqual(len(quincunx), 5)  # Should have 5 lines
        self.assertTrue(any("◊" in line for line in quincunx))  # Should contain diamond
        
        # Test invalid pattern
        with self.assertRaises(ValueError):
            sacred_geometry.get_pattern_visualization("invalid_pattern")
    
    def test_temple_alignment(self):
        """Test temple alignment calculations."""
        # Test at equator
        equator_align = sacred_geometry.calculate_temple_alignment("kan_cross", 0.0)
        self.assertEqual(equator_align["main_angle"], 90.0)  # Should face east
        self.assertEqual(len(equator_align["cardinal_angles"]), 4)  # Should have 4 points
        
        # Test at significant latitude
        tropic_align = sacred_geometry.calculate_temple_alignment("quincunx", 23.5, True)
        self.assertGreater(tropic_align["latitude_adjustment"], 0)  # Should have positive adjustment
        self.assertEqual(len(tropic_align["cardinal_angles"]), 5)  # Should have 5 points
    
    def test_observatory_points(self):
        """Test observatory point calculations."""
        center = (0.0, 0.0)
        radius = 1.0
        
        # Test Kan Cross (4 points)
        kan_points = sacred_geometry.calculate_observatory_points("kan_cross", center, radius)
        self.assertEqual(len(kan_points), 4)
        # Check if points form a square
        self.assertAlmostEqual(kan_points[0][0], 1.0)  # East point
        self.assertAlmostEqual(kan_points[2][0], -1.0)  # West point
        
        # Test Octagon (8 points)
        oct_points = sacred_geometry.calculate_observatory_points("octagon", center, radius)
        self.assertEqual(len(oct_points), 8)
        # Check 45-degree point
        self.assertAlmostEqual(oct_points[1][0], math.cos(math.radians(45)))
        self.assertAlmostEqual(oct_points[1][1], math.sin(math.radians(45)))
    
    def test_sacred_proportions(self):
        """Test sacred proportion calculations."""
        # Test Kan Cross proportions
        kan_props = sacred_geometry.calculate_sacred_proportions("kan_cross")
        self.assertEqual(kan_props["width_to_height"], 1.0)  # Should be square
        
        # Test Quincunx proportions (Golden Ratio)
        quincunx_props = sacred_geometry.calculate_sacred_proportions("quincunx")
        self.assertAlmostEqual(quincunx_props["width_to_height"], (1 + math.sqrt(5)) / 2)
        
        # Test Hexagon proportions
        hex_props = sacred_geometry.calculate_sacred_proportions("hexagon")
        self.assertAlmostEqual(hex_props["width_to_height"], math.sqrt(3)/2)
        
        # Test invalid pattern
        with self.assertRaises(ValueError):
            sacred_geometry.calculate_sacred_proportions("invalid_pattern")

if __name__ == '__main__':
    unittest.main() 