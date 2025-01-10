"""
Chinese cosmological system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "jade_emperor": {
        "role": "supreme_ruler",
        "element": "jade",
        "symbol": "pearl",
        "description": "Ruler of heaven and all deities",
        "sacred_number": 9
    },
    "xiwangmu": {
        "role": "queen_mother",
        "element": "yin",
        "symbol": "peach",
        "description": "Queen Mother of the West, keeper of immortality",
        "sacred_number": 7
    },
    "guan_yin": {
        "role": "compassion",
        "element": "water",
        "symbol": "lotus",
        "description": "Bodhisattva of mercy and compassion",
        "sacred_number": 8
    },
    "pan_gu": {
        "role": "creator",
        "element": "qi",
        "symbol": "egg",
        "description": "First being who created the world",
        "sacred_number": 1
    }
}

# Cosmic realms
REALMS = {
    "tian": {
        "type": "celestial",
        "residents": "celestial_beings",
        "symbol": "jade_palace",
        "guardian": "jade_emperor"
    },
    "ren": {
        "type": "mortal",
        "residents": "humans",
        "symbol": "five_mountains",
        "guardian": "tu_di_gong"
    },
    "di": {
        "type": "underworld",
        "residents": "spirits",
        "symbol": "yellow_springs",
        "guardian": "yan_wang"
    }
}

# Creation stages
CREATION_STAGES = [
    {
        "name": "hundun",
        "symbol": "chaos",
        "element": "qi",
        "significance": "primordial chaos"
    },
    {
        "name": "separation",
        "symbol": "yin_yang",
        "element": "duality",
        "significance": "division of heaven and earth"
    },
    {
        "name": "five_elements",
        "symbol": "wuxing",
        "element": "elements",
        "significance": "creation of fundamental forces"
    },
    {
        "name": "ten_thousand",
        "symbol": "myriad",
        "element": "life",
        "significance": "creation of all things"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    1: "unity and origin",
    2: "yin and yang",
    3: "heaven earth humanity",
    4: "cardinal directions",
    5: "elements and phases",
    8: "bagua trigrams",
    9: "celestial harmony"
}

class CreationPhase(Enum):
    """Enumeration of creation phases in Chinese cosmology."""
    CHAOS = "hundun"
    DIVISION = "separation"
    ELEMENTS = "five_elements"
    MANIFESTATION = "ten_thousand"

# Cosmic structure
COSMIC_LEVELS = {
    "upper": ["jade_palace", "celestial_court", "star_realm"],
    "middle": ["mortal_realm", "five_mountains", "four_seas"],
    "lower": ["yellow_springs", "ghost_city", "ten_courts"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "heaven_earth": {"type": "cosmic_balance", "significance": "harmony"},
    "five_elements": {"type": "cycles", "significance": "transformation"},
    "yin_yang": {"type": "duality", "significance": "complementarity"},
    "human_dao": {"type": "cultivation", "significance": "enlightenment"}
}

def get_realm_guardian(realm: str) -> Optional[str]:
    """Get the guardian of a specific realm."""
    realm_data = REALMS.get(realm)
    return realm_data["guardian"] if realm_data else None

def get_sacred_number_meaning(number: int) -> Optional[str]:
    """Get the significance of a sacred number."""
    return SACRED_NUMBERS.get(number)

def get_creation_stage(phase: CreationPhase) -> Optional[Dict]:
    """Get details about a specific creation stage."""
    return next(
        (stage for stage in CREATION_STAGES if stage["name"] == phase.value),
        None
    )

def get_cosmic_level(location: str) -> Optional[str]:
    """Get the cosmic level where a location exists."""
    for level, locations in COSMIC_LEVELS.items():
        if location in locations:
            return level
    return None

def get_element_relationship(element1: str, element2: str) -> str:
    """Get the relationship between two elements in Wu Xing."""
    WUXING_CYCLES = {
        ("wood", "fire"): "generating",
        ("fire", "earth"): "generating",
        ("earth", "metal"): "generating",
        ("metal", "water"): "generating",
        ("water", "wood"): "generating",
        ("wood", "metal"): "controlling",
        ("metal", "fire"): "controlling",
        ("fire", "water"): "controlling",
        ("water", "earth"): "controlling",
        ("earth", "wood"): "controlling"
    }
    return WUXING_CYCLES.get((element1.lower(), element2.lower()), "neutral") 