"""
Test suite for cross-cultural mythological validation.
"""

import pytest
from datetime import datetime
from vortex.src.mythology.cross_cultural import (
    ArchetypeCategory,
    ElementalForce,
    CosmicLevel,
    CrossCulturalMapping,
    get_equivalent_deity,
    get_deity_archetype,
    find_archetype_match,
    get_shared_elements,
    find_shared_symbolism,
    get_ritual_correspondence,
    validate_cross_cultural_mapping
)

class TestArchetypalMapping:
    """Test suite for archetypal mapping functionality."""
    
    def test_creator_deity_mapping(self):
        """Test mapping between creator deities."""
        # Test Mayan Hunab Ku to Dogon Amma
        mayan_creator = get_equivalent_deity("hunab_ku", "mayan", "dogon")
        assert mayan_creator == "amma"
        
        # Test archetype consistency
        mayan_archetype = get_deity_archetype("hunab_ku", "mayan")
        dogon_archetype = get_deity_archetype("amma", "dogon")
        assert mayan_archetype == ArchetypeCategory.CREATOR
        assert mayan_archetype == dogon_archetype
        
    def test_sage_deity_mapping(self):
        """Test mapping between sage deities."""
        # Test Mayan Itzamna to Egyptian Thoth
        equivalent = get_equivalent_deity("itzamna", "mayan", "egyptian")
        assert equivalent == "thoth"
        
        # Verify shared attributes
        mayan_elements = get_shared_elements("itzamna", "mayan")
        egyptian_elements = get_shared_elements("thoth", "egyptian")
        assert ElementalForce.AIR in mayan_elements
        assert ElementalForce.AIR in egyptian_elements
        
    def test_invalid_deity_mapping(self):
        """Test mapping with non-existent deity."""
        result = get_equivalent_deity("nonexistent", "mayan", "dogon")
        assert result is None

class TestSymbolicMapping:
    """Test suite for symbolic mapping functionality."""
    
    def test_world_tree_symbolism(self):
        """Test world tree symbolism across cultures."""
        world_tree = find_shared_symbolism("world_tree")
        assert world_tree is not None
        assert "mayan" in world_tree
        assert "norse" in world_tree
        assert "hindu" in world_tree
        
        # Verify elements
        elements = world_tree["elements"]
        assert ElementalForce.EARTH in elements
        assert ElementalForce.AIR in elements
        
    def test_cosmic_serpent_symbolism(self):
        """Test cosmic serpent symbolism across cultures."""
        serpent = find_shared_symbolism("cosmic_serpent")
        assert serpent is not None
        assert serpent["mayan"] == "kukulcan"
        assert serpent["hindu"] == "ananta_shesha"
        assert serpent["norse"] == "jormungandr"
        
        # Verify water element
        assert ElementalForce.WATER in serpent["elements"]
        
    def test_invalid_symbol(self):
        """Test lookup of non-existent symbol."""
        result = find_shared_symbolism("nonexistent")
        assert result is None

class TestRitualCorrespondence:
    """Test suite for ritual correspondence functionality."""
    
    def test_purification_rituals(self):
        """Test purification ritual correspondences."""
        mayan_ritual = get_ritual_correspondence("purification", "mayan")
        hindu_ritual = get_ritual_correspondence("purification", "hindu")
        japanese_ritual = get_ritual_correspondence("purification", "japanese")
        
        assert mayan_ritual == "temazcal"
        assert hindu_ritual == "abhisheka"
        assert japanese_ritual == "misogi"
        
    def test_cosmic_alignment_rituals(self):
        """Test cosmic alignment ritual correspondences."""
        mayan_ritual = get_ritual_correspondence("cosmic_alignment", "mayan")
        egyptian_ritual = get_ritual_correspondence("cosmic_alignment", "egyptian")
        
        assert mayan_ritual == "zenith_passage"
        assert egyptian_ritual == "solar_alignment"
        
    def test_invalid_ritual(self):
        """Test lookup of non-existent ritual."""
        result = get_ritual_correspondence("nonexistent", "mayan")
        assert result is None

class TestCrossCulturalValidation:
    """Test suite for cross-cultural validation functionality."""
    
    def test_valid_mapping(self):
        """Test validation of correct mapping."""
        mapping = CrossCulturalMapping(
            source_deity="kukulcan",
            source_mythology="mayan",
            target_deity="quetzalcoatl",
            target_mythology="aztec",
            archetype=ArchetypeCategory.SAGE,
            elements=[ElementalForce.AIR, ElementalForce.WATER],
            cosmic_level=CosmicLevel.CELESTIAL,
            shared_symbols=["feathered_serpent", "wind", "wisdom"],
            confidence_score=0.95
        )
        
        is_valid, issues = validate_cross_cultural_mapping(mapping)
        assert is_valid
        assert not issues
        
    def test_invalid_elements(self):
        """Test validation with incorrect elemental associations."""
        mapping = CrossCulturalMapping(
            source_deity="kukulcan",
            source_mythology="mayan",
            target_deity="quetzalcoatl",
            target_mythology="aztec",
            archetype=ArchetypeCategory.SAGE,
            elements=[ElementalForce.FIRE],  # Incorrect element
            cosmic_level=CosmicLevel.CELESTIAL,
            shared_symbols=["feathered_serpent"],
            confidence_score=0.95
        )
        
        is_valid, issues = validate_cross_cultural_mapping(mapping)
        assert not is_valid
        assert "Inconsistent elemental associations" in issues[0]
        
    def test_invalid_archetype(self):
        """Test validation with incorrect archetype."""
        mapping = CrossCulturalMapping(
            source_deity="kukulcan",
            source_mythology="mayan",
            target_deity="quetzalcoatl",
            target_mythology="aztec",
            archetype=ArchetypeCategory.TRICKSTER,  # Incorrect archetype
            elements=[ElementalForce.AIR, ElementalForce.WATER],
            cosmic_level=CosmicLevel.CELESTIAL,
            shared_symbols=["feathered_serpent"],
            confidence_score=0.95
        )
        
        is_valid, issues = validate_cross_cultural_mapping(mapping)
        assert not is_valid
        assert "Inconsistent archetypal categorization" in issues[0]

class TestElementalAssociations:
    """Test suite for elemental associations functionality."""
    
    def test_deity_elements(self):
        """Test retrieval of deity elemental associations."""
        kukulcan_elements = get_shared_elements("kukulcan", "mayan")
        assert ElementalForce.AIR in kukulcan_elements
        assert ElementalForce.WATER in kukulcan_elements
        
    def test_invalid_deity_elements(self):
        """Test elements for non-existent deity."""
        elements = get_shared_elements("nonexistent", "mayan")
        assert not elements
        
    def test_cross_cultural_elements(self):
        """Test elemental consistency across cultures."""
        mayan_elements = get_shared_elements("kukulcan", "mayan")
        aztec_elements = get_shared_elements("quetzalcoatl", "aztec")
        
        # Both should have air and water associations
        assert ElementalForce.AIR in mayan_elements
        assert ElementalForce.WATER in mayan_elements
        assert ElementalForce.AIR in aztec_elements
        assert ElementalForce.WATER in aztec_elements

class TestCosmicLevels:
    """Test suite for cosmic level functionality."""
    
    def test_creator_deity_level(self):
        """Test cosmic level of creator deities."""
        hunab_ku_level = get_cosmic_level("hunab_ku", "mayan")
        amma_level = get_cosmic_level("amma", "dogon")
        
        assert hunab_ku_level == CosmicLevel.TRANSCENDENT
        assert amma_level == CosmicLevel.TRANSCENDENT
        
    def test_terrestrial_deity_level(self):
        """Test cosmic level of terrestrial deities."""
        kukulcan_level = get_cosmic_level("kukulcan", "mayan")
        assert kukulcan_level == CosmicLevel.TERRESTRIAL
        
    def test_invalid_deity_level(self):
        """Test cosmic level for non-existent deity."""
        level = get_cosmic_level("nonexistent", "mayan")
        assert level is None 