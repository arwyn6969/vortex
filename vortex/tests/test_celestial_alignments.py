"""
Tests for the celestial alignment system.
"""
import pytest
from ..src.mythology.celestial_alignments import AlignmentManager, AlignmentType, CelestialAlignment
from ..src.mythology.archetype_manager import ArchetypeManager
from ..src.mythology.alignment_data import populate_alignment_data

@pytest.fixture
def archetype_manager():
    return ArchetypeManager()

@pytest.fixture
def alignment_manager(archetype_manager):
    manager = AlignmentManager(archetype_manager)
    populate_alignment_data(manager)
    return manager

def test_get_alignment(alignment_manager):
    """Test retrieving specific site alignments."""
    newgrange = alignment_manager.get_alignment("newgrange")
    assert newgrange is not None
    assert newgrange.site_name == "Newgrange"
    assert newgrange.alignment_type == AlignmentType.SOLSTICE_WINTER
    assert newgrange.is_verified == True
    assert newgrange.deviation_degrees == 0.42

def test_get_sites_by_archetype(alignment_manager):
    """Test filtering sites by archetypal force."""
    wisdom_sites = alignment_manager.get_sites_by_archetype("wisdom_teacher")
    assert len(wisdom_sites) > 0
    assert any(site.site_name == "Newgrange" for site in wisdom_sites)
    assert any(site.site_name == "Great Pyramid of Giza" for site in wisdom_sites)

def test_get_sites_by_alignment_type(alignment_manager):
    """Test filtering sites by alignment type."""
    winter_solstice_sites = alignment_manager.get_sites_by_alignment_type(AlignmentType.SOLSTICE_WINTER)
    assert len(winter_solstice_sites) > 0
    assert any(site.site_name == "Newgrange" for site in winter_solstice_sites)

def test_get_verified_sites(alignment_manager):
    """Test filtering for verified sites only."""
    verified_sites = alignment_manager.get_verified_sites()
    assert len(verified_sites) > 0
    assert all(site.is_verified for site in verified_sites)
    assert any(site.site_name == "Stonehenge" for site in verified_sites)

def test_get_sites_by_precision(alignment_manager):
    """Test filtering sites by alignment precision."""
    precise_sites = alignment_manager.get_sites_by_precision(0.5)
    assert len(precise_sites) > 0
    assert all(site.deviation_degrees <= 0.5 for site in precise_sites)

def test_get_sites_by_period(alignment_manager):
    """Test filtering sites by historical period."""
    ancient_sites = alignment_manager.get_sites_by_period(-10000, -3000)
    assert len(ancient_sites) > 0
    assert all(-10000 <= site.year_of_alignment <= -3000 for site in ancient_sites)
    assert any(site.site_name == "Gobekli Tepe" for site in ancient_sites)

def test_get_archetypal_resonance(alignment_manager):
    """Test calculating archetypal resonance for sites."""
    resonance = alignment_manager.get_archetypal_resonance("great_pyramid_of_giza")
    assert len(resonance) > 0
    assert "wisdom_teacher" in resonance
    assert "divine_warrior" in resonance
    assert all(0.0 <= value <= 1.2 for value in resonance.values()) 