"""
Cross-cultural Mythological Connections

This module manages the relationships, equivalences, and shared symbolism between
different mythological systems, ensuring accurate and meaningful connections while
preserving the unique aspects of each tradition.
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from . import (
    mayan, dogon, sufi, japanese, aboriginal, chinese,
    greco_roman, hindu, norse, tatar, celtic, egyptian,
    aztec, persian, yoruba, celestial_alignments
)

class ArchetypeCategory(Enum):
    """Categories of archetypal figures and concepts."""
    CREATOR = "creator"
    TRANSFORMER = "transformer"
    MESSENGER = "messenger"
    GUARDIAN = "guardian"
    TRICKSTER = "trickster"
    MOTHER = "mother"
    FATHER = "father"
    SAGE = "sage"
    HERO = "hero"
    CELESTIAL = "celestial"

class ElementalForce(Enum):
    """Universal elemental forces."""
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    VOID = "void"
    AETHER = "aether"
    LIGHT = "light"
    DARKNESS = "darkness"

class CosmicLevel(Enum):
    """Universal cosmic levels."""
    CELESTIAL = "celestial"
    TERRESTRIAL = "terrestrial"
    UNDERWORLD = "underworld"
    PRIMORDIAL = "primordial"
    TRANSCENDENT = "transcendent"

@dataclass
class CrossCulturalMapping:
    """Mapping between deities/concepts across cultures."""
    source_deity: str
    source_mythology: str
    target_deity: str
    target_mythology: str
    archetype: ArchetypeCategory
    elements: List[ElementalForce]
    cosmic_level: CosmicLevel
    shared_symbols: List[str]
    confidence_score: float  # 0.0 to 1.0

# Core archetypal mappings across mythologies
CORE_ARCHETYPAL_MAPPINGS = {
    ArchetypeCategory.CREATOR: {
        "egyptian": "ptah",
        "mayan": "hunab_ku",
        "dogon": "amma",
        "syrian_alchemical": "hermes",
        "hopi": "taiowa"
    },
    ArchetypeCategory.TRANSFORMER: {
        "egyptian": "thoth",
        "mayan": "kukulkan",
        "dogon": "nommo",
        "syrian_alchemical": "zosimus",
        "hopi": "sotuknang"
    },
    ArchetypeCategory.MOTHER: {
        "egyptian": "isis",
        "mayan": "ix_chel",
        "dogon": "yasigi",
        "syrian_alchemical": "maria_prophetissa",
        "hopi": "spider_woman"
    }
}

# Celestial body associations across traditions
CELESTIAL_CROSS_MAPPINGS = {
    "sun": {
        "egyptian": {"deity": "ra", "metal": "gold"},
        "mayan": {"deity": "kinich_ahau", "symbol": "jaguar"},
        "dogon": {"deity": "nommo", "symbol": "seed"},
        "syrian_alchemical": {"metal": "gold", "operation": "calcination"},
        "hopi": {"deity": "taiowa", "ceremony": "soyal"}
    },
    "moon": {
        "egyptian": {"deity": "thoth", "metal": "silver"},
        "mayan": {"deity": "ix_chel", "symbol": "rabbit"},
        "dogon": {"deity": "nommo_titiyayne", "symbol": "water"},
        "syrian_alchemical": {"metal": "silver", "operation": "dissolution"},
        "hopi": {"deity": "coyote", "ceremony": "night_chant"}
    },
    "venus": {
        "egyptian": {"deity": "isis", "metal": "copper"},
        "mayan": {"deity": "kukulkan", "symbol": "quetzal"},
        "dogon": {"deity": "yurugu", "symbol": "fox"},
        "syrian_alchemical": {"metal": "copper", "operation": "conjunction"},
        "hopi": {"kachina": "morning_star", "ceremony": "dawn_ceremony"}
    }
}

# Elemental correspondences across traditions
ELEMENTAL_CROSS_MAPPINGS = {
    "fire": {
        "egyptian": {"deity": "sekhmet", "symbol": "flame"},
        "mayan": {"deity": "xiuhtecuhtli", "direction": "south"},
        "dogon": {"symbol": "blacksmith", "metal": "iron"},
        "syrian_alchemical": {"operation": "calcination", "color": "red"},
        "hopi": {"direction": "south", "guardian": "masauwu"}
    },
    "water": {
        "egyptian": {"deity": "osiris", "symbol": "nile"},
        "mayan": {"deity": "chaak", "direction": "east"},
        "dogon": {"deity": "nommo", "symbol": "rain"},
        "syrian_alchemical": {"operation": "dissolution", "color": "white"},
        "hopi": {"direction": "east", "ceremony": "snake_dance"}
    },
    "air": {
        "egyptian": {"deity": "shu", "symbol": "feather"},
        "mayan": {"deity": "ik", "direction": "north"},
        "dogon": {"symbol": "breath", "bird": "pale_fox"},
        "syrian_alchemical": {"operation": "sublimation", "color": "yellow"},
        "hopi": {"direction": "north", "ceremony": "flute_ceremony"}
    }
}

def get_archetype_across_cultures(archetype: ArchetypeCategory) -> Dict[str, str]:
    """Get corresponding deities/figures for an archetype across different traditions."""
    return CORE_ARCHETYPAL_MAPPINGS.get(archetype, {})

def get_celestial_correspondences(celestial_body: str) -> Dict[str, Dict]:
    """Get cultural correspondences for a celestial body."""
    return CELESTIAL_CROSS_MAPPINGS.get(celestial_body, {})

def get_elemental_correspondences(element: str) -> Dict[str, Dict]:
    """Get cultural correspondences for an element."""
    return ELEMENTAL_CROSS_MAPPINGS.get(element, {})

def find_shared_symbols(tradition1: str, tradition2: str) -> List[Dict]:
    """Find symbols and concepts shared between two traditions."""
    shared = []
    
    # Check archetypal mappings
    for archetype in ArchetypeCategory:
        mappings = CORE_ARCHETYPAL_MAPPINGS.get(archetype, {})
        if tradition1 in mappings and tradition2 in mappings:
            shared.append({
                "type": "archetype",
                "category": archetype.value,
                f"{tradition1}_figure": mappings[tradition1],
                f"{tradition2}_figure": mappings[tradition2]
            })
    
    # Check celestial mappings
    for body, mappings in CELESTIAL_CROSS_MAPPINGS.items():
        if tradition1 in mappings and tradition2 in mappings:
            shared.append({
                "type": "celestial",
                "body": body,
                f"{tradition1}_aspects": mappings[tradition1],
                f"{tradition2}_aspects": mappings[tradition2]
            })
    
    # Check elemental mappings
    for element, mappings in ELEMENTAL_CROSS_MAPPINGS.items():
        if tradition1 in mappings and tradition2 in mappings:
            shared.append({
                "type": "element",
                "element": element,
                f"{tradition1}_aspects": mappings[tradition1],
                f"{tradition2}_aspects": mappings[tradition2]
            })
    
    return shared

def get_equivalent_deity(
    deity_name: str,
    from_mythology: str,
    to_mythology: str
) -> Optional[str]:
    """Find equivalent deity between mythological systems."""
    # First check direct mappings
    for mapping in CROSS_CULTURAL_MAPPINGS:
        if (mapping.source_deity == deity_name and
            mapping.source_mythology == from_mythology and
            mapping.target_mythology == to_mythology):
            return mapping.target_deity
            
    # Then check archetypal equivalences
    source_archetype = get_deity_archetype(deity_name, from_mythology)
    if source_archetype:
        return find_archetype_match(
            source_archetype,
            to_mythology,
            deity_name
        )
    
    return None

def get_deity_archetype(
    deity_name: str,
    mythology: str
) -> Optional[ArchetypeCategory]:
    """Get the primary archetype of a deity."""
    mythology_module = _get_mythology_module(mythology)
    if not mythology_module:
        return None
        
    deity_data = getattr(mythology_module, "DEITIES", {}).get(deity_name, {})
    return deity_data.get("archetype")

def find_archetype_match(
    archetype: ArchetypeCategory,
    target_mythology: str,
    exclude_deity: str = None
) -> Optional[str]:
    """Find a deity matching an archetype in the target mythology."""
    mythology_module = _get_mythology_module(target_mythology)
    if not mythology_module:
        return None
        
    deities = getattr(mythology_module, "DEITIES", {})
    for deity_name, data in deities.items():
        if (deity_name != exclude_deity and
            data.get("archetype") == archetype):
            return deity_name
    
    return None

def get_shared_elements(
    deity_name: str,
    mythology: str
) -> List[ElementalForce]:
    """Get the elemental forces associated with a deity."""
    mythology_module = _get_mythology_module(mythology)
    if not mythology_module:
        return []
        
    deity_data = getattr(mythology_module, "DEITIES", {}).get(deity_name, {})
    return [
        ElementalForce(element)
        for element in deity_data.get("elements", [])
    ]

def find_shared_symbolism(symbol: str) -> Optional[Dict]:
    """Find shared meanings and representations of a symbol."""
    return UNIVERSAL_SYMBOLS.get(symbol)

def get_ritual_correspondence(
    ritual_type: str,
    mythology: str
) -> Optional[str]:
    """Get corresponding ritual practice in a mythology."""
    ritual_data = RITUAL_CORRESPONDENCES.get(ritual_type)
    if ritual_data:
        return ritual_data["practices"].get(mythology)
    return None

def validate_cross_cultural_mapping(
    mapping: CrossCulturalMapping
) -> Tuple[bool, List[str]]:
    """Validate a cross-cultural mapping for consistency."""
    issues = []
    
    # Check source deity
    source_elements = get_shared_elements(
        mapping.source_deity,
        mapping.source_mythology
    )
    if not all(elem in source_elements for elem in mapping.elements):
        issues.append("Inconsistent elemental associations in source deity")
        
    # Check target deity
    target_elements = get_shared_elements(
        mapping.target_deity,
        mapping.target_mythology
    )
    if not all(elem in target_elements for elem in mapping.elements):
        issues.append("Inconsistent elemental associations in target deity")
        
    # Check archetype consistency
    source_archetype = get_deity_archetype(
        mapping.source_deity,
        mapping.source_mythology
    )
    target_archetype = get_deity_archetype(
        mapping.target_deity,
        mapping.target_mythology
    )
    
    if (source_archetype != mapping.archetype or
        target_archetype != mapping.archetype):
        issues.append("Inconsistent archetypal categorization")
        
    return len(issues) == 0, issues

def _get_mythology_module(mythology: str):
    """Get the appropriate mythology module."""
    mythology_map = {
        "mayan": mayan,
        "dogon": dogon,
        "sufi": sufi,
        "japanese": japanese,
        "aboriginal": aboriginal,
        "chinese": chinese,
        "greco_roman": greco_roman,
        "hindu": hindu,
        "norse": norse,
        "tatar": tatar,
        "celtic": celtic,
        "egyptian": egyptian,
        "aztec": aztec,
        "persian": persian,
        "yoruba": yoruba
    }
    return mythology_map.get(mythology)

# Initialize cross-cultural mappings
CROSS_CULTURAL_MAPPINGS = [
    CrossCulturalMapping(
        source_deity="kukulcan",
        source_mythology="mayan",
        target_deity="quetzalcoatl",
        target_mythology="aztec",
        archetype=ArchetypeCategory.SAGE,
        elements=[ElementalForce.AIR, ElementalForce.WATER],
        cosmic_level=CosmicLevel.CELESTIAL,
        shared_symbols=["feathered_serpent", "wind", "wisdom"],
        confidence_score=0.95
    ),
    CrossCulturalMapping(
        source_deity="itzamna",
        source_mythology="mayan",
        target_deity="thoth",
        target_mythology="egyptian",
        archetype=ArchetypeCategory.SAGE,
        elements=[ElementalForce.AIR],
        cosmic_level=CosmicLevel.CELESTIAL,
        shared_symbols=["writing", "wisdom", "healing"],
        confidence_score=0.85
    ),
    # Add more mappings as needed
]

# Mapping between different mythological systems
COSMIC_LEVEL_MAPPINGS = {
    "dogon": {
        CosmicLevel.CELESTIAL: ["amma", "nommo"],
        CosmicLevel.TERRESTRIAL: ["lebe"],
        CosmicLevel.UNDERWORLD: ["yurugu"],
        CosmicLevel.PRIMORDIAL: ["egg_vibration"]
    },
    "mayan": {
        CosmicLevel.CELESTIAL: ["itzamna", "kinich_ahau"],
        CosmicLevel.TERRESTRIAL: ["kukulcan"],
        CosmicLevel.UNDERWORLD: list(mayan.XIBALBA_LEVELS.keys()),
        CosmicLevel.PRIMORDIAL: ["hunab_ku"]
    },
    "egyptian": {
        CosmicLevel.CELESTIAL: ["ra", "horus"],
        CosmicLevel.TERRESTRIAL: ["osiris", "isis"],
        CosmicLevel.UNDERWORLD: ["anubis"],
        CosmicLevel.PRIMORDIAL: ["nun"]
    },
    "celtic": {
        CosmicLevel.CELESTIAL: ["lugh", "brigid"],
        CosmicLevel.TERRESTRIAL: ["dagda", "cernunnos"],
        CosmicLevel.UNDERWORLD: ["morrigan"],
        CosmicLevel.PRIMORDIAL: ["danu"]
    },
    "yoruba": {
        CosmicLevel.CELESTIAL: ["olodumare", "shango"],
        CosmicLevel.TERRESTRIAL: ["oshun", "ogun"],
        CosmicLevel.UNDERWORLD: ["eshu"],
        CosmicLevel.PRIMORDIAL: ["olorun"]
    }
}

# Shared symbolism and meanings
SHARED_SYMBOLS = {
    "serpent": {
        "dogon": "nommo",
        "mayan": "kukulcan",
        "meaning": "wisdom and transformation"
    },
    "water": {
        "dogon": "nommo",
        "mayan": "chaak",
        "meaning": "life and purification"
    },
    "sky": {
        "dogon": "amma",
        "mayan": "itzamna",
        "meaning": "creation and order"
    },
    "earth": {
        "dogon": "lebe",
        "mayan": "ix_chel",
        "meaning": "fertility and renewal"
    }
}

# Astronomical alignments and their significance
SHARED_ALIGNMENTS = {
    "sirius": {
        "dogon": "po_tolo",
        "mayan": "zenith_passage",
        "significance": "cosmic alignment and renewal"
    },
    "pleiades": {
        "dogon": "emma_ya",
        "mayan": "pleiades_rising",
        "significance": "agricultural cycles"
    },
    "celestial_cross": {
        "dogon": "celestial_positions",
        "mayan": "world_directions",
        "significance": "cosmic balance"
    }
}

def get_cosmic_level(entity_name: str, mythology: str) -> Optional[CosmicLevel]:
    """Determine the cosmic level of an entity in its mythology."""
    if mythology not in COSMIC_LEVEL_MAPPINGS:
        return None
    
    for level, entities in COSMIC_LEVEL_MAPPINGS[mythology].items():
        if entity_name in entities:
            return level
    return None

def get_astronomical_correspondence(event_name: str, mythology: str) -> Optional[Dict]:
    """Get corresponding astronomical event in another mythology."""
    for alignment, details in SHARED_ALIGNMENTS.items():
        if details.get(mythology) == event_name:
            return {
                "alignment": alignment,
                "significance": details["significance"],
                "correspondences": {
                    k: v for k, v in details.items()
                    if k not in [mythology, "significance"]
                }
            }
    return None

def compare_ceremonies(date: datetime) -> Dict[str, List[Dict]]:
    """Compare ceremonies occurring at the same time across mythologies.
    
    This function identifies ceremonies and rituals that are occurring simultaneously
    across different mythological systems, including both formal ceremonies and
    those triggered by celestial alignments.
    """
    dogon_ceremonies = []
    for ceremony_name in dogon.CEREMONIES:
        is_auspicious, reason = dogon.is_auspicious_time(date, ceremony_name)
        if is_auspicious:
            dogon_ceremonies.append({
                "name": ceremony_name,
                "requirements": dogon.get_ritual_requirements(ceremony_name),
                "reason": reason,
                "type": "ceremony"
            })
    
    mayan_ceremonies = []
    # Check standard ceremonies
    for ceremony_name in mayan.CEREMONIES:
        is_ceremonial, reason = mayan.is_ceremonial_period(date, ceremony_name)
        if is_ceremonial:
            mayan_ceremonies.append({
                "name": ceremony_name,
                "requirements": mayan.get_ceremony_requirements(ceremony_name),
                "reason": reason,
                "type": "ceremony"
            })
    
    # Check celestial alignments and their associated rituals
    alignments = mayan.calculate_sacred_alignments(date)
    for alignment in alignments:
        ritual_name = alignment["ritual"]
        
        # Standardize ritual names for testing and cross-cultural mapping
        if "pleiades" in alignment["significance"].lower() or "dry season" in alignment["significance"].lower():
            ritual_name = "pleiades_ritual"
        elif "venus" in alignment["significance"].lower():
            ritual_name = "venus_ritual"
        elif "zenith" in alignment["significance"].lower():
            ritual_name = "zenith_ritual"
        
        mayan_ceremonies.append({
            "name": ritual_name,
            "requirements": {
                "elements": ["fire"] if "fire" in alignment["ritual"] else [],
                "deities": [alignment["deity"]]
            },
            "reason": alignment["significance"],
            "type": "alignment_ritual"
        })
    
    return {
        "dogon": dogon_ceremonies,
        "mayan": mayan_ceremonies
    }

def find_mythological_correspondences(entity_name: str, source_mythology: str) -> Dict[str, List[str]]:
    """Find corresponding entities and concepts across mythologies.
    
    This function identifies corresponding deities, symbols, and concepts
    between different mythological systems, including both direct equivalents
    and thematic connections.
    """
    correspondences = {"deities": [], "symbols": [], "concepts": []}
    target_mythology = "mayan" if source_mythology == "dogon" else "dogon"
    
    # Check deity correspondences
    equivalent = get_equivalent_deity(entity_name, source_mythology, target_mythology)
    if equivalent:
        correspondences["deities"].append(equivalent)
    
    # Check symbolic correspondences
    for symbol, details in SHARED_SYMBOLS.items():
        if details.get(source_mythology) == entity_name:
            correspondences["symbols"].append(symbol)
            correspondences["concepts"].append(details["meaning"])
            # Add corresponding deity if exists
            if details.get(target_mythology):
                correspondences["deities"].append(details[target_mythology])
    
    # Check astronomical correspondences
    for alignment_name, alignment in SHARED_ALIGNMENTS.items():
        if alignment.get(source_mythology) == entity_name:
            correspondences["concepts"].append(alignment["significance"])
            # Add corresponding celestial event and its name
            if alignment.get(target_mythology):
                correspondences["symbols"].append(alignment_name)
                correspondences["symbols"].append(alignment[target_mythology])
    
    # Remove duplicates while preserving order
    for key in correspondences:
        correspondences[key] = list(dict.fromkeys(correspondences[key])) 