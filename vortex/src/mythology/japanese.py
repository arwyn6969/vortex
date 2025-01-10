"""
Japanese cosmological system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities (Kami)
DEITIES = {
    "amaterasu": {
        "role": "sun_goddess",
        "element": "light",
        "symbol": "mirror",
        "description": "Supreme goddess of the sun and universe",
        "sacred_number": 8
    },
    "susanoo": {
        "role": "storm_god",
        "element": "storm",
        "symbol": "sword",
        "description": "God of storms and the sea",
        "sacred_number": 5
    },
    "tsukuyomi": {
        "role": "moon_god",
        "element": "darkness",
        "symbol": "moon",
        "description": "God of the moon and night",
        "sacred_number": 3
    },
    "izanagi": {
        "role": "creator",
        "element": "yang",
        "symbol": "spear",
        "description": "Male creator of Japan",
        "sacred_number": 1
    }
}

# Cosmic realms
REALMS = {
    "takamagahara": {
        "type": "celestial",
        "residents": "heavenly_kami",
        "symbol": "high_plain",
        "guardian": "amaterasu"
    },
    "nakatsukuni": {
        "type": "mortal",
        "residents": "humans",
        "symbol": "land_reed",
        "guardian": "okuninushi"
    },
    "yomi": {
        "type": "underworld",
        "residents": "dead",
        "symbol": "darkness",
        "guardian": "izanami"
    }
}

# Creation stages
CREATION_STAGES = [
    {
        "name": "kotoamatsukami",
        "symbol": "emergence",
        "element": "void",
        "significance": "first deities"
    },
    {
        "name": "kuniumi",
        "symbol": "islands",
        "element": "earth",
        "significance": "birth of lands"
    },
    {
        "name": "kamiumi",
        "symbol": "deities",
        "element": "spirit",
        "significance": "birth of kami"
    },
    {
        "name": "tenson_korin",
        "symbol": "descent",
        "element": "light",
        "significance": "divine descent"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    1: "unity and creation",
    3: "three treasures",
    4: "cardinal directions",
    5: "elements",
    8: "perfect abundance",
    12: "zodiac cycle"
}

class CreationPhase(Enum):
    """Enumeration of creation phases in Japanese cosmology."""
    EMERGENCE = "kotoamatsukami"
    LAND_BIRTH = "kuniumi"
    KAMI_BIRTH = "kamiumi"
    DESCENT = "tenson_korin"

# Cosmic structure
COSMIC_LEVELS = {
    "upper": ["takamagahara", "ama_no_hashidate", "ama_no_ukihashi"],
    "middle": ["ashihara", "yamato", "four_seas"],
    "lower": ["yomi", "ne_no_kuni", "watatsumi"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "amaterasu_susanoo": {"type": "sibling_conflict", "significance": "order_chaos"},
    "izanagi_izanami": {"type": "creation_pair", "significance": "duality"},
    "kami_human": {"type": "reverence", "significance": "harmony"},
    "matsuri_kami": {"type": "ritual", "significance": "communion"}
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

def is_kami_enshrined(kami_name: str, location: str) -> bool:
    """Check if a kami is enshrined in a particular location."""
    # This would be implemented with actual shrine data
    kami = DEITIES.get(kami_name)
    return bool(kami and location in COSMIC_LEVELS["middle"]) 