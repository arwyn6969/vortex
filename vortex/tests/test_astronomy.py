"""
Tests for astronomical calculations in Dogon and Mayan mythological systems.
"""
import unittest
from datetime import datetime, timedelta
from src.mythology import dogon, mayan, cross_cultural

class TestDogonAstronomy(unittest.TestCase):
    """Test cases for Dogon astronomical calculations."""
    
    def setUp(self):
        """Set up test cases with known dates."""
        self.sirius_zenith = datetime(2024, 9, 15)  # During zenith period
        self.sirius_nadir = datetime(2024, 3, 15)   # During nadir period
        self.night_time = datetime(2024, 9, 15, 22, 0)  # 10 PM
        self.day_time = datetime(2024, 9, 15, 14, 0)    # 2 PM

    def test_sirius_position_calculation(self):
        """Test Sirius position calculations."""
        # Test zenith period
        zenith_pos = dogon.calculate_sirius_position(self.sirius_zenith)
        self.assertEqual(zenith_pos["position"], "zenith")
        
        # Test nadir period
        nadir_pos = dogon.calculate_sirius_position(self.sirius_nadir)
        self.assertEqual(nadir_pos["position"], "nadir")
        
        # Test visibility during night
        night_pos = dogon.calculate_sirius_position(self.night_time)
        self.assertEqual(night_pos["visibility"], "visible")
        
        # Test visibility during day
        day_pos = dogon.calculate_sirius_position(self.day_time)
        self.assertEqual(day_pos["visibility"], "hidden")

    def test_ceremony_timing(self):
        """Test ceremony timing calculations."""
        # Test Sigui ceremony timing (60-year cycle from 1967)
        current_date = datetime(2024, 1, 1)
        next_sigui = dogon.get_next_ceremony("sigui", current_date)
        self.assertEqual(next_sigui.year, 2027)  # Next cycle after 1967
        
        # Test Bulu ceremony (annual)
        next_bulu = dogon.get_next_ceremony("bulu", current_date)
        self.assertTrue(next_bulu.month == 6)  # Should be in June
        
        # Test as-needed ceremony
        next_dama = dogon.get_next_ceremony("dama", current_date)
        self.assertIsNone(next_dama)  # Cannot predict as-needed ceremonies

    def test_auspicious_timing(self):
        """Test auspicious timing calculations."""
        # Test Sigui ceremony during zenith
        is_auspicious, _ = dogon.is_auspicious_time(self.sirius_zenith, "sigui")
        self.assertTrue(is_auspicious)
        
        # Test Sigui ceremony during nadir (should not be auspicious)
        is_auspicious, _ = dogon.is_auspicious_time(self.sirius_nadir, "sigui")
        self.assertFalse(is_auspicious)

class TestMayanAstronomy(unittest.TestCase):
    """Test cases for Mayan astronomical calculations."""
    
    def setUp(self):
        """Set up test cases with known dates."""
        self.epoch = datetime(2000, 1, 1)
        self.test_date = datetime(2024, 6, 10)  # During Pleiades rising
        self.venus_cycle_start = self.epoch + timedelta(days=584)  # One Venus cycle

    def test_calendar_calculations(self):
        """Test Mayan calendar calculations."""
        # Test Tzolkin date calculation for full cycle
        tzolkin_number, tzolkin_sign = mayan.get_tzolkin_date(260)
        self.assertEqual(tzolkin_number, 13)
        self.assertEqual(tzolkin_sign, "ahau")
        
        # Test Haab date calculation for new year
        haab_day, haab_month = mayan.get_haab_date(1)
        self.assertEqual(haab_day, 0)
        self.assertEqual(haab_month, "pop")
        
        # Test Long Count calculation
        days = 144000  # One baktun
        long_count = mayan.calculate_long_count(days)
        self.assertEqual(long_count["baktun"], 1)
        self.assertEqual(long_count["katun"], 0)

    def test_celestial_alignments(self):
        """Test celestial alignment calculations."""
        # Test during Pleiades rising period
        alignments = mayan.calculate_sacred_alignments(self.test_date)
        pleiades_alignment = next(
            (a for a in alignments if a["significance"] == "start of dry season"),
            None
        )
        self.assertIsNotNone(pleiades_alignment)
        
        # Test Venus cycle
        alignments = mayan.calculate_sacred_alignments(self.venus_cycle_start)
        venus_alignment = next(
            (a for a in alignments if "war and sacrifice" in a["significance"].lower()),
            None
        )
        self.assertIsNotNone(venus_alignment)

    def test_ceremonial_periods(self):
        """Test ceremonial period calculations."""
        # Test New Fire ceremony (52-year cycle)
        days_in_calendar_round = mayan.CALENDAR_ROUNDS["tzolkin_haab"]
        calendar_round_date = self.epoch + timedelta(days=days_in_calendar_round)
        is_ceremonial, _ = mayan.is_ceremonial_period(calendar_round_date, "new_fire")
        self.assertTrue(is_ceremonial)
        
        # Test Wayeb period
        wayeb_date = self.epoch + timedelta(days=360)  # End of Haab year
        is_ceremonial, _ = mayan.is_ceremonial_period(wayeb_date, "wayeb")
        self.assertTrue(is_ceremonial)

class TestCrossCulturalAstronomy(unittest.TestCase):
    """Test cases for cross-cultural astronomical correspondences."""
    
    def setUp(self):
        """Set up test cases with known dates."""
        self.test_date = datetime(2024, 6, 10)  # During shared agricultural period

    def test_astronomical_correspondences(self):
        """Test astronomical correspondence mappings."""
        # Test Sirius correspondence
        sirius_corr = cross_cultural.get_astronomical_correspondence("po_tolo", "dogon")
        self.assertEqual(sirius_corr["alignment"], "sirius")
        self.assertEqual(sirius_corr["correspondences"]["mayan"], "zenith_passage")
        
        # Test Pleiades correspondence
        pleiades_corr = cross_cultural.get_astronomical_correspondence("pleiades_rising", "mayan")
        self.assertEqual(pleiades_corr["alignment"], "pleiades")
        self.assertEqual(pleiades_corr["correspondences"]["dogon"], "emma_ya")

    def test_simultaneous_ceremonies(self):
        """Test detection of simultaneously occurring ceremonies."""
        ceremonies = cross_cultural.compare_ceremonies(self.test_date)
        
        # Should have ceremonies during agricultural period
        self.assertTrue(any(c["name"] == "bulu" for c in ceremonies["dogon"]))
        self.assertTrue(any(
            c["name"] == "pleiades_ritual"
            for c in ceremonies["mayan"]
        ))

if __name__ == '__main__':
    unittest.main() 