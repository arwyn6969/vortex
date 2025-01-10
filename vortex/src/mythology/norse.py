"""
Norse cosmological system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "odin": {
        "role": "all_father",
        "element": "air",
        "symbol": "raven",
        "description": "God of wisdom, poetry, death, and magic",
        "sacred_number": 9
    },
    "thor": {
        "role": "protector",
        "element": "thunder",
        "symbol": "hammer",
        "description": "God of thunder and protection",
        "sacred_number": 2
    },
    "freya": {
        "role": "fertility",
        "element": "earth",
        "symbol": "falcon",
        "description": "Goddess of love, fertility, and magic",
        "sacred_number": 13
    },
    "ymir": {
        "role": "progenitor",
        "element": "ice",
        "symbol": "giant",
        "description": "First being and ancestor of giants",
        "sacred_number": 1
    }
}

# Cosmological realms
REALMS = {
    "asgard": {
        "type": "divine",
        "residents": "aesir",
        "symbol": "golden_hall",
        "guardian": "heimdall"
    },
    "midgard": {
        "type": "mortal",
        "residents": "humans",
        "symbol": "world_tree_trunk",
        "guardian": "thor"
    },
    "jotunheim": {
        "type": "giant",
        "residents": "jotnar",
        "symbol": "mountains",
        "guardian": "none"
    }
}

# Creation stages
CREATION_STAGES = [
    {
        "name": "ginnungagap",
        "symbol": "void",
        "element": "chaos",
        "significance": "primordial void"
    },
    {
        "name": "ymir_birth",
        "symbol": "frost",
        "element": "ice",
        "significance": "first being"
    },
    {
        "name": "world_creation",
        "symbol": "ymir_body",
        "element": "flesh",
        "significance": "world formation"
    },
    {
        "name": "yggdrasil_growth",
        "symbol": "tree",
        "element": "wood",
        "significance": "cosmic structure"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    1: "creation and solitude",
    2: "duality and balance",
    3: "completion and harmony",
    8: "dimensions of cosmos",
    9: "worlds of yggdrasil",
    13: "lunar cycles and magic"
}

class CreationPhase(Enum):
    """Enumeration of creation phases in Norse cosmology."""
    VOID = "ginnungagap"
    FIRST_BEING = "ymir_birth"
    WORLD_FORMING = "world_creation"
    TREE_GROWING = "yggdrasil_growth"

# World tree levels
YGGDRASIL_LEVELS = {
    "upper": ["asgard", "alfheim", "vanaheim"],
    "middle": ["midgard", "jotunheim", "nidavellir"],
    "lower": ["niflheim", "muspelheim", "helheim"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "odin_ymir": {"type": "destruction", "significance": "creation from chaos"},
    "thor_midgard": {"type": "protection", "significance": "order"},
    "freya_vanir": {"type": "alliance", "significance": "peace"},
    "norns_yggdrasil": {"type": "fate", "significance": "destiny"}
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

def get_yggdrasil_level(realm: str) -> Optional[str]:
    """Get the level of Yggdrasil where a realm exists."""
    for level, realms in YGGDRASIL_LEVELS.items():
        if realm in realms:
            return level
    return None 