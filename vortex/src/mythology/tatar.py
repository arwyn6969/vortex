"""
Tatar cosmological system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "tengri": {
        "role": "sky_god",
        "element": "air",
        "symbol": "blue_sky",
        "description": "Supreme deity of the heavens",
        "sacred_number": 9
    },
    "umai": {
        "role": "earth_mother",
        "element": "earth",
        "symbol": "womb",
        "description": "Goddess of fertility and children",
        "sacred_number": 3
    },
    "erlik": {
        "role": "underworld_ruler",
        "element": "darkness",
        "symbol": "black_bull",
        "description": "Lord of the underworld",
        "sacred_number": 7
    },
    "su_iyesi": {
        "role": "water_spirit",
        "element": "water",
        "symbol": "wave",
        "description": "Master of waters",
        "sacred_number": 4
    }
}

# Cosmic realms
REALMS = {
    "upper_world": {
        "type": "celestial",
        "residents": "good_spirits",
        "symbol": "world_tree_top",
        "guardian": "tengri"
    },
    "middle_world": {
        "type": "physical",
        "residents": "humans",
        "symbol": "world_tree_trunk",
        "guardian": "umai"
    },
    "lower_world": {
        "type": "underworld",
        "residents": "evil_spirits",
        "symbol": "world_tree_roots",
        "guardian": "erlik"
    }
}

# Creation stages
CREATION_STAGES = [
    {
        "name": "primordial_waters",
        "symbol": "ocean",
        "element": "water",
        "significance": "original state"
    },
    {
        "name": "world_creation",
        "symbol": "earth_dive",
        "element": "earth",
        "significance": "land formation"
    },
    {
        "name": "world_tree",
        "symbol": "tree",
        "element": "wood",
        "significance": "cosmic axis"
    },
    {
        "name": "human_creation",
        "symbol": "clay",
        "element": "earth",
        "significance": "humanity begins"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    3: "cosmic levels",
    4: "cardinal directions",
    7: "underworld levels",
    9: "heavenly levels"
}

class CreationPhase(Enum):
    """Enumeration of creation phases in Tatar cosmology."""
    WATERS = "primordial_waters"
    EARTH = "world_creation"
    TREE = "world_tree"
    HUMANS = "human_creation"

# Cosmic structure
COSMIC_LEVELS = {
    "upper": ["ninth_sky", "eighth_sky", "seventh_sky"],
    "middle": ["earth", "mountains", "waters"],
    "lower": ["first_level", "second_level", "third_level"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "tengri_umai": {"type": "sky_earth", "significance": "balance"},
    "shaman_spirits": {"type": "mediation", "significance": "healing"},
    "human_nature": {"type": "harmony", "significance": "respect"},
    "ancestor_descendant": {"type": "lineage", "significance": "tradition"}
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

def is_spirit_path_open(level1: str, level2: str) -> bool:
    """Check if there is a spirit path between two cosmic levels."""
    # In Tatar mythology, shamans could travel between levels
    levels = list(COSMIC_LEVELS.keys())
    level1_idx = next((i for i, locs in enumerate(levels) if level1 in COSMIC_LEVELS[locs]), -1)
    level2_idx = next((i for i, locs in enumerate(levels) if level2 in COSMIC_LEVELS[locs]), -1)
    return level1_idx != -1 and level2_idx != -1 