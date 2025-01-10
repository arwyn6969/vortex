"""
Sufi mystical system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and divine attributes (Names of Allah)
DIVINE_NAMES = {
    "al_haqq": {
        "role": "truth",
        "element": "essence",
        "symbol": "light",
        "description": "The Ultimate Truth and Reality",
        "sacred_number": 108
    },
    "al_nur": {
        "role": "light",
        "element": "illumination",
        "symbol": "lamp",
        "description": "The Divine Light that guides",
        "sacred_number": 256
    },
    "al_wadud": {
        "role": "love",
        "element": "heart",
        "symbol": "rose",
        "description": "The Most Loving",
        "sacred_number": 20
    },
    "al_wahid": {
        "role": "unity",
        "element": "oneness",
        "symbol": "point",
        "description": "The Indivisible One",
        "sacred_number": 1
    }
}

# Spiritual realms (Hadharat)
REALMS = {
    "lahut": {
        "type": "divine",
        "nature": "absolute_essence",
        "symbol": "pure_light",
        "guardian": "none"
    },
    "jabarut": {
        "type": "power",
        "nature": "divine_attributes",
        "symbol": "throne",
        "guardian": "angels"
    },
    "malakut": {
        "type": "angelic",
        "nature": "spiritual_world",
        "symbol": "wings",
        "guardian": "archangels"
    },
    "nasut": {
        "type": "human",
        "nature": "physical_world",
        "symbol": "earth",
        "guardian": "prophets"
    }
}

# Spiritual stages (Maqamat)
STAGES = [
    {
        "name": "tawba",
        "symbol": "return",
        "element": "repentance",
        "significance": "beginning of path"
    },
    {
        "name": "wara",
        "symbol": "abstinence",
        "element": "detachment",
        "significance": "spiritual vigilance"
    },
    {
        "name": "zuhd",
        "symbol": "asceticism",
        "element": "renunciation",
        "significance": "worldly detachment"
    },
    {
        "name": "fana",
        "symbol": "extinction",
        "element": "annihilation",
        "significance": "dissolution of ego"
    },
    {
        "name": "baqa",
        "symbol": "permanence",
        "element": "subsistence",
        "significance": "divine union"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    1: "divine unity",
    4: "elements of nature",
    7: "levels of nafs",
    9: "spheres of existence",
    11: "initial letters",
    99: "divine names",
    1000: "stations of light"
}

class SpiritualStage(Enum):
    """Enumeration of spiritual stages in Sufi path."""
    REPENTANCE = "tawba"
    VIGILANCE = "wara"
    RENUNCIATION = "zuhd"
    ANNIHILATION = "fana"
    SUBSISTENCE = "baqa"

# Spiritual structure
SPIRITUAL_LEVELS = {
    "divine": ["essence", "attributes", "names"],
    "cosmic": ["throne", "footstool", "spheres"],
    "earthly": ["mineral", "vegetable", "animal", "human"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "sheikh_murid": {"type": "guidance", "significance": "spiritual_training"},
    "heart_divine": {"type": "gnosis", "significance": "direct_knowledge"},
    "soul_truth": {"type": "realization", "significance": "awakening"},
    "human_divine": {"type": "unity", "significance": "ultimate_goal"}
}

def get_realm_nature(realm: str) -> Optional[str]:
    """Get the nature of a specific realm."""
    realm_data = REALMS.get(realm)
    return realm_data["nature"] if realm_data else None

def get_sacred_number_meaning(number: int) -> Optional[str]:
    """Get the significance of a sacred number."""
    return SACRED_NUMBERS.get(number)

def get_spiritual_stage(phase: SpiritualStage) -> Optional[Dict]:
    """Get details about a specific spiritual stage."""
    return next(
        (stage for stage in STAGES if stage["name"] == phase.value),
        None
    )

def get_spiritual_level(state: str) -> Optional[str]:
    """Get the spiritual level where a state exists."""
    for level, states in SPIRITUAL_LEVELS.items():
        if state in states:
            return level
    return None

def is_divine_name_manifest(name: str, level: str) -> bool:
    """Check if a divine name is manifest at a particular level."""
    divine_name = DIVINE_NAMES.get(name)
    if not divine_name:
        return False
    # Divine names manifest differently at different levels
    manifestation_levels = {
        "divine": ["truth", "unity", "light"],
        "cosmic": ["light", "love", "power"],
        "earthly": ["mercy", "sustenance", "guidance"]
    }
    return divine_name["role"] in manifestation_levels.get(level, []) 