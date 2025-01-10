"""
Greco-Roman cosmological system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities (with both Greek/Roman names)
DEITIES = {
    "zeus_jupiter": {
        "role": "sky_father",
        "element": "lightning",
        "symbol": "eagle",
        "description": "King of gods, ruler of sky and thunder",
        "sacred_number": 12
    },
    "poseidon_neptune": {
        "role": "sea_lord",
        "element": "water",
        "symbol": "trident",
        "description": "God of sea, earthquakes, and horses",
        "sacred_number": 3
    },
    "hades_pluto": {
        "role": "underworld_ruler",
        "element": "earth",
        "symbol": "helm",
        "description": "God of underworld and wealth",
        "sacred_number": 4
    },
    "athena_minerva": {
        "role": "wisdom",
        "element": "air",
        "symbol": "owl",
        "description": "Goddess of wisdom, war strategy, and crafts",
        "sacred_number": 7
    }
}

# Cosmic realms
REALMS = {
    "olympus": {
        "type": "divine",
        "residents": "olympians",
        "symbol": "mountain",
        "guardian": "horae"
    },
    "earth": {
        "type": "mortal",
        "residents": "humans",
        "symbol": "gaia",
        "guardian": "none"
    },
    "underworld": {
        "type": "chthonic",
        "residents": "shades",
        "symbol": "pomegranate",
        "guardian": "cerberus"
    }
}

# Creation stages
CREATION_STAGES = [
    {
        "name": "chaos",
        "symbol": "void",
        "element": "primordial",
        "significance": "original state"
    },
    {
        "name": "gaia_birth",
        "symbol": "earth",
        "element": "terra",
        "significance": "world foundation"
    },
    {
        "name": "titan_age",
        "symbol": "kronos",
        "element": "time",
        "significance": "first divine rule"
    },
    {
        "name": "olympian_age",
        "symbol": "throne",
        "element": "order",
        "significance": "current divine order"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    3: "divine triad and realms",
    4: "elements and seasons",
    7: "celestial bodies and wisdom",
    9: "muses and learning",
    12: "olympians and months"
}

class CreationPhase(Enum):
    """Enumeration of creation phases in Greco-Roman cosmology."""
    VOID = "chaos"
    EARTH = "gaia_birth"
    TITANS = "titan_age"
    OLYMPIANS = "olympian_age"

# Cosmic structure
COSMIC_LEVELS = {
    "upper": ["olympus", "aether", "celestial"],
    "middle": ["earth", "sea", "air"],
    "lower": ["tartarus", "erebus", "asphodel"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "zeus_titans": {"type": "overthrow", "significance": "new order"},
    "demeter_persephone": {"type": "seasons", "significance": "cycles"},
    "apollo_muses": {"type": "inspiration", "significance": "arts"},
    "athena_heroes": {"type": "guidance", "significance": "wisdom"}
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

def get_deity_roman_name(greek_name: str) -> Optional[str]:
    """Get the Roman name equivalent of a Greek deity."""
    for names in DEITIES.keys():
        greek, roman = names.split("_")
        if greek == greek_name:
            return roman
    return None 