"""
Tests for advanced pantheon mechanics and deity interactions.
"""
import unittest
from datetime import datetime
from src.mythology import pantheon_mechanics as pm

class TestPantheonMechanics(unittest.TestCase):
    """Test cases for pantheon mechanics functionality."""
    
    def setUp(self):
        """Set up test cases with known dates."""
        self.test_date = datetime(2024, 6, 10)  # During Pleiades rising
        self.zenith_date = datetime(2024, 9, 15)  # Sirius at zenith
        self.nadir_date = datetime(2024, 3, 15)   # Sirius at nadir

    def test_deity_power_calculation(self):
        """Test deity power level calculations."""
        # Test Dogon creator deity during zenith
        amma_power = pm.calculate_deity_power("amma", self.zenith_date)
        self.assertGreater(amma_power["total_power"], amma_power["base_power"])
        self.assertGreater(amma_power["celestial_influence"], 0)
        
        # Test Mayan sun deity during celestial alignment
        kinich_power = pm.calculate_deity_power("kinich_ahau", self.test_date)
        self.assertGreater(kinich_power["total_power"], kinich_power["base_power"])
        
        # Test invalid deity
        with self.assertRaises(ValueError):
            pm.calculate_deity_power("invalid_deity", self.test_date)

    def test_deity_aspects(self):
        """Test deity relationship calculations."""
        # Test harmonious relationship (same domain)
        aspect = pm.calculate_deity_aspect("amma", "itzamna", self.test_date)
        self.assertIsNotNone(aspect)
        self.assertEqual(aspect[0], pm.AspectType.TRINE)
        
        # Test opposing relationship
        aspect = pm.calculate_deity_aspect("amma", "yurugu", self.test_date)
        self.assertIsNotNone(aspect)
        self.assertEqual(aspect[0], pm.AspectType.OPPOSITION)
        
        # Test invalid deity combination
        aspect = pm.calculate_deity_aspect("invalid_deity", "amma", self.test_date)
        self.assertIsNone(aspect)

    def test_harmonious_deities(self):
        """Test finding harmonious deity relationships."""
        # Test finding allies for Dogon deity
        nommo_allies = pm.find_harmonious_deities("nommo", self.test_date)
        self.assertTrue(len(nommo_allies) > 0)
        self.assertTrue(any(ally["deity"] == "itzamna" for ally in nommo_allies))
        
        # Test minimum strength filter
        strong_allies = pm.find_harmonious_deities("nommo", self.test_date, min_strength=0.9)
        self.assertTrue(len(strong_allies) <= len(nommo_allies))
        
        # Test invalid deity
        with self.assertRaises(ValueError):
            pm.calculate_deity_power("invalid_deity", self.test_date)

    def test_divine_challenge_generation(self):
        """Test divine challenge generation."""
        # Test celestial deity challenge
        kinich_challenge = pm.generate_divine_challenge("kinich_ahau", self.test_date)
        self.assertIn("astronomical_observation", kinich_challenge["elements"])
        self.assertTrue(kinich_challenge["requirements"]["celestial_alignment"])
        
        # Test wisdom deity challenge
        itzamna_challenge = pm.generate_divine_challenge("itzamna", self.test_date)
        self.assertIn("riddle_solving", itzamna_challenge["elements"])
        
        # Test challenge difficulty scaling
        hard_challenge = pm.generate_divine_challenge("amma", self.zenith_date)
        easy_challenge = pm.generate_divine_challenge("lebe", self.nadir_date)
        self.assertGreater(hard_challenge["difficulty"], easy_challenge["difficulty"])
        
        # Test invalid deity
        with self.assertRaises(ValueError):
            pm.generate_divine_challenge("invalid_deity", self.test_date)

    def test_domain_types(self):
        """Test domain type assignments and relationships."""
        # Test primary domain assignment
        self.assertEqual(pm.DEITY_DOMAINS["amma"]["primary"], pm.DomainType.CREATION)
        self.assertEqual(pm.DEITY_DOMAINS["kinich_ahau"]["primary"], pm.DomainType.CELESTIAL)
        
        # Test secondary domain lists
        self.assertIn(pm.DomainType.CELESTIAL, pm.DEITY_DOMAINS["amma"]["secondary"])
        self.assertIn(pm.DomainType.CREATION, pm.DEITY_DOMAINS["itzamna"]["secondary"])
        
        # Test element assignments
        self.assertEqual(pm.DEITY_DOMAINS["nommo"]["elements"], ["water"])
        self.assertEqual(pm.DEITY_DOMAINS["kinich_ahau"]["elements"], ["fire"])

    def test_aspect_weights(self):
        """Test aspect weight system."""
        # Test positive aspects
        self.assertGreater(pm.ASPECT_WEIGHTS[pm.AspectType.CONJUNCTION], 
                          pm.ASPECT_WEIGHTS[pm.AspectType.TRINE])
        self.assertGreater(pm.ASPECT_WEIGHTS[pm.AspectType.TRINE],
                          pm.ASPECT_WEIGHTS[pm.AspectType.SEXTILE])
        
        # Test negative aspects
        self.assertLess(pm.ASPECT_WEIGHTS[pm.AspectType.OPPOSITION], 0)
        self.assertGreater(pm.ASPECT_WEIGHTS[pm.AspectType.SQUARE],
                          pm.ASPECT_WEIGHTS[pm.AspectType.OPPOSITION])

    def test_chinese_deity_power(self):
        """Test power calculation for Chinese deities."""
        # Test Jade Emperor's power
        jade_power = pm.calculate_deity_power("jade_emperor", self.test_date)
        self.assertGreater(jade_power["total_power"], 1.0)
        self.assertGreater(jade_power["celestial_influence"], 0)
        
        # Test directional deity power
        xuan_wu_power = pm.calculate_deity_power("xuan_wu", self.test_date)
        self.assertGreater(xuan_wu_power["total_power"], 0.9)
        self.assertIn("domain_influence", xuan_wu_power)
    
    def test_chinese_deity_aspects(self):
        """Test aspect calculations between Chinese deities."""
        # Test generating cycle relationship
        wood_metal_aspect = pm.calculate_deity_aspect("qing_long", "bai_hu", self.test_date)
        self.assertIsNotNone(wood_metal_aspect)
        self.assertEqual(wood_metal_aspect[0], pm.AspectType.SQUARE)
        
        # Test same element relationship
        metal_metal_aspect = pm.calculate_deity_aspect("jade_emperor", "bai_hu", self.test_date)
        self.assertIsNotNone(metal_metal_aspect)
        self.assertIn(metal_metal_aspect[0], [pm.AspectType.CONJUNCTION, pm.AspectType.SEXTILE])
    
    def test_chinese_challenges(self):
        """Test challenge generation for Chinese deities."""
        # Test directional deity challenge
        xuan_wu_challenge = pm.generate_divine_challenge("xuan_wu", self.test_date)
        self.assertIn("directional_alignment", xuan_wu_challenge["elements"])
        self.assertIn("water", xuan_wu_challenge["requirements"]["offerings"])
        
        # Test celestial deity challenge
        jade_emperor_challenge = pm.generate_divine_challenge("jade_emperor", self.test_date)
        self.assertIn("astronomical_observation", jade_emperor_challenge["elements"])
        self.assertEqual(jade_emperor_challenge["domain"], "heaven")
    
    def test_cross_cultural_aspects(self):
        """Test aspects between deities from different cultures."""
        # Test Chinese-Dogon aspect
        chinese_dogon_aspect = pm.calculate_deity_aspect("jade_emperor", "amma", self.test_date)
        self.assertIsNotNone(chinese_dogon_aspect)
        self.assertIn(chinese_dogon_aspect[0], [pm.AspectType.CONJUNCTION, pm.AspectType.TRINE])
        
        # Test Chinese-Mayan aspect
        chinese_mayan_aspect = pm.calculate_deity_aspect("xuan_wu", "chaak", self.test_date)
        self.assertIsNotNone(chinese_mayan_aspect)
        self.assertGreater(chinese_mayan_aspect[1], 0)  # Check aspect strength
    
    def test_element_based_challenges(self):
        """Test element-specific challenge generation."""
        # Test water element challenge
        water_challenge = pm.generate_divine_challenge("xuan_wu", self.test_date)
        self.assertTrue(any(e.startswith("element_water") for e in water_challenge["elements"]))
        
        # Test metal element challenge
        metal_challenge = pm.generate_divine_challenge("bai_hu", self.test_date)
        self.assertTrue(any(e.startswith("element_metal") for e in metal_challenge["elements"]))

if __name__ == '__main__':
    unittest.main() 