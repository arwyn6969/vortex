"""
Test module for validating the newly added mythological systems and their
cross-cultural mappings, ensuring proper integration with the existing framework.
"""

import pytest
from vortex.src.mythology import (
    celtic, egyptian, aztec, persian, yoruba,
    cross_cultural, archetype_manager
)
from vortex.src.mythology.cross_cultural import (
    CrossCulturalMapping, ElementalForce, CosmicLevel, ArchetypeCategory
)

def test_creator_deities():
    """Test creator deities across new mythological systems."""
    creators = cross_cultural.CREATOR_DEITIES
    
    # Test Egyptian Ra
    assert "egyptian" in creators
    assert creators["egyptian"]["deity"] == "ra"
    assert creators["egyptian"]["attributes"]["archetype"] == ArchetypeCategory.CREATOR
    assert ElementalForce.LIGHT in creators["egyptian"]["attributes"]["elements"]
    
    # Test Celtic Dagda
    assert "celtic" in creators
    assert creators["celtic"]["deity"] == "dagda"
    assert creators["celtic"]["attributes"]["archetype"] == ArchetypeCategory.CREATOR
    assert ElementalForce.EARTH in creators["celtic"]["attributes"]["elements"]
    
    # Test Persian Ahura Mazda
    assert "persian" in creators
    assert creators["persian"]["deity"] == "ahura_mazda"
    assert creators["persian"]["attributes"]["archetype"] == ArchetypeCategory.CREATOR
    assert ElementalForce.LIGHT in creators["persian"]["attributes"]["elements"]
    
    # Test Yoruba Olodumare
    assert "yoruba" in creators
    assert creators["yoruba"]["deity"] == "olodumare"
    assert creators["yoruba"]["attributes"]["archetype"] == ArchetypeCategory.CREATOR
    assert ElementalForce.LIGHT in creators["yoruba"]["attributes"]["elements"]

def test_universal_symbols():
    """Test universal symbols and their cross-cultural representations."""
    symbols = cross_cultural.UNIVERSAL_SYMBOLS
    
    # Test Thunder Deity symbol
    assert "thunder_deity" in symbols
    assert symbols["thunder_deity"]["celtic"] == "taranis"
    assert symbols["thunder_deity"]["yoruba"] == "shango"
    assert symbols["thunder_deity"]["aztec"] == "tlaloc"
    assert ElementalForce.AIR in symbols["thunder_deity"]["elements"]
    assert ElementalForce.FIRE in symbols["thunder_deity"]["elements"]
    
    # Test Mother Goddess symbol
    assert "mother_goddess" in symbols
    assert symbols["mother_goddess"]["egyptian"] == "isis"
    assert symbols["mother_goddess"]["celtic"] == "brigid"
    assert symbols["mother_goddess"]["persian"] == "anahita"
    assert symbols["mother_goddess"]["yoruba"] == "yemoja"
    assert ElementalForce.EARTH in symbols["mother_goddess"]["elements"]
    assert ElementalForce.WATER in symbols["mother_goddess"]["elements"]

def test_ritual_correspondences():
    """Test ritual correspondences across new mythological systems."""
    rituals = cross_cultural.RITUAL_CORRESPONDENCES
    
    # Test Solar Worship
    assert "solar_worship" in rituals
    assert rituals["solar_worship"]["practices"]["egyptian"] == "ra_adoration"
    assert rituals["solar_worship"]["practices"]["persian"] == "mithra_ritual"
    assert rituals["solar_worship"]["practices"]["aztec"] == "eagle_warrior_rite"
    assert rituals["solar_worship"]["practices"]["celtic"] == "beltane_fire"
    assert ElementalForce.FIRE in rituals["solar_worship"]["elements"]
    assert ElementalForce.LIGHT in rituals["solar_worship"]["elements"]
    
    # Test Divine Justice
    assert "divine_justice" in rituals
    assert rituals["divine_justice"]["practices"]["yoruba"] == "shango_ritual"
    assert rituals["divine_justice"]["practices"]["egyptian"] == "maat_weighing"
    assert rituals["divine_justice"]["practices"]["persian"] == "mithra_judgment"
    assert ElementalForce.FIRE in rituals["divine_justice"]["elements"]
    assert ElementalForce.AIR in rituals["divine_justice"]["elements"]

def test_cross_cultural_mappings():
    """Test specific cross-cultural deity mappings."""
    mappings = cross_cultural.CROSS_CULTURAL_MAPPINGS
    
    # Find Thoth-Orunmila mapping
    thoth_mapping = next(
        m for m in mappings 
        if m.source_deity == "thoth" and m.target_deity == "orunmila"
    )
    assert thoth_mapping.source_mythology == "egyptian"
    assert thoth_mapping.target_mythology == "yoruba"
    assert thoth_mapping.archetype == ArchetypeCategory.SAGE
    assert "wisdom" in thoth_mapping.shared_symbols
    assert "divination" in thoth_mapping.shared_symbols
    
    # Find Quetzalcoatl-Mithra mapping
    quetzal_mapping = next(
        m for m in mappings 
        if m.source_deity == "quetzalcoatl" and m.target_deity == "mithra"
    )
    assert quetzal_mapping.source_mythology == "aztec"
    assert quetzal_mapping.target_mythology == "persian"
    assert quetzal_mapping.archetype == ArchetypeCategory.SAGE
    assert "wisdom" in quetzal_mapping.shared_symbols
    assert "sun" in quetzal_mapping.shared_symbols

def test_cosmic_levels():
    """Test cosmic level mappings for new mythological systems."""
    levels = cross_cultural.COSMIC_LEVEL_MAPPINGS
    
    # Test Egyptian cosmic levels
    assert "egyptian" in levels
    assert "ra" in levels["egyptian"][CosmicLevel.CELESTIAL]
    assert "osiris" in levels["egyptian"][CosmicLevel.TERRESTRIAL]
    assert "anubis" in levels["egyptian"][CosmicLevel.UNDERWORLD]
    
    # Test Celtic cosmic levels
    assert "celtic" in levels
    assert "lugh" in levels["celtic"][CosmicLevel.CELESTIAL]
    assert "dagda" in levels["celtic"][CosmicLevel.TERRESTRIAL]
    assert "morrigan" in levels["celtic"][CosmicLevel.UNDERWORLD]
    
    # Test Yoruba cosmic levels
    assert "yoruba" in levels
    assert "olodumare" in levels["yoruba"][CosmicLevel.CELESTIAL]
    assert "oshun" in levels["yoruba"][CosmicLevel.TERRESTRIAL]
    assert "eshu" in levels["yoruba"][CosmicLevel.UNDERWORLD]

def test_archetype_manager_integration():
    """Test integration of new systems with the archetype manager."""
    manager = archetype_manager.ArchetypeManager()
    
    # Test creator archetype mappings
    creator_mappings = manager.archetype_mappings["creator"]
    assert archetype_manager.CulturalSystem.EGYPTIAN in creator_mappings
    assert archetype_manager.CulturalSystem.CELTIC in creator_mappings
    assert archetype_manager.CulturalSystem.AZTEC in creator_mappings
    assert archetype_manager.CulturalSystem.PERSIAN in creator_mappings
    assert archetype_manager.CulturalSystem.YORUBA in creator_mappings
    
    # Test elemental mappings
    egyptian_elements = manager.elemental_mappings[archetype_manager.CulturalSystem.EGYPTIAN]
    assert "ra" in egyptian_elements["fire"]
    assert "isis" in egyptian_elements["water"]
    
    celtic_elements = manager.elemental_mappings[archetype_manager.CulturalSystem.CELTIC]
    assert "brigid" in celtic_elements["fire"]
    assert "manannan" in celtic_elements["water"]
    
    yoruba_elements = manager.elemental_mappings[archetype_manager.CulturalSystem.YORUBA]
    assert "shango" in yoruba_elements["fire"]
    assert "yemoja" in yoruba_elements["water"] 