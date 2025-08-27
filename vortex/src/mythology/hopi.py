"""
Hopi Cosmological System and Relationships

This module defines the Hopi mythological system, including their unique understanding
of time cycles, emergence stories, and deep connection to celestial phenomena.
"""

from typing import Dict, List, Optional
from enum import Enum

class WorldCycle(Enum):
    """Cycles of world emergence in Hopi cosmology."""
    TOKPELA = "first_world"    # Perfect world
    TOKPA = "second_world"     # Gray world
    KUSKURZA = "third_world"   # Red world
    TUWAQACHI = "fourth_world" # Current world

class Direction(Enum):
    """Sacred directions in Hopi cosmology."""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    ABOVE = "above"
    BELOW = "below"
    CENTER = "center"

# Core concepts and deities
DEITIES = {
    "taiowa": {
        "role": "creator",
        "element": "void",
        "symbol": "sun",
        "description": "Supreme creator deity",
        "sacred_number": 1
    },
    "sotuknang": {
        "role": "world_shaper",
        "element": "air",
        "symbol": "breath",
        "description": "First being created by Taiowa",
        "sacred_number": 4
    },
    "spider_woman": {
        "role": "life_creator",
        "element": "earth",
        "symbol": "web",
        "description": "Creator of life and teacher of weaving",
        "sacred_number": 8
    },
    "masauwu": {
        "role": "earth_guardian",
        "element": "fire",
        "symbol": "face",
        "description": "Guardian of death and fire",
        "sacred_number": 7
    }
}

# Cosmic realms and their attributes
REALMS = {
    "upperworld": {
        "type": "celestial",
        "residents": "kachinas",
        "symbol": "cloud",
        "guardian": "sotuknang"
    },
    "middleworld": {
        "type": "earthly",
        "residents": "humans",
        "symbol": "corn",
        "guardian": "masauwu"
    },
    "underworld": {
        "type": "emergence",
        "residents": "ancestors",
        "symbol": "sipapu",
        "guardian": "spider_woman"
    }
}

# Celestial alignments and their significance
CELESTIAL_ALIGNMENTS = {
    "winter_solstice": {
        "ceremony": "soyal",
        "purpose": "sun_return",
        "kachinas": ["sun_kachina"],
        "duration_days": 16
    },
    "summer_solstice": {
        "ceremony": "niman",
        "purpose": "kachina_departure",
        "kachinas": ["hemis_kachina"],
        "duration_days": 8
    },
    "pleiades_rising": {
        "ceremony": "snake_antelope",
        "purpose": "rain_calling",
        "kachinas": ["snake_kachina"],
        "duration_days": 9
    },
    "orion_zenith": {
        "ceremony": "powamu",
        "purpose": "purification",
        "kachinas": ["powamu_kachina"],
        "duration_days": 8
    }
}

# Directional correspondences
DIRECTIONAL_CORRESPONDENCES = {
    Direction.NORTH: {
        "color": "yellow",
        "element": "air",
        "mineral": "crystal",
        "animal": "mountain_sheep"
    },
    Direction.SOUTH: {
        "color": "red",
        "element": "fire",
        "mineral": "turquoise",
        "animal": "antelope"
    },
    Direction.EAST: {
        "color": "white",
        "element": "water",
        "mineral": "shell",
        "animal": "eagle"
    },
    Direction.WEST: {
        "color": "blue",
        "element": "earth",
        "mineral": "coral",
        "animal": "bear"
    },
    Direction.ABOVE: {
        "color": "many_colored",
        "element": "space",
        "mineral": "sunlight",
        "animal": "eagle"
    },
    Direction.BELOW: {
        "color": "black",
        "element": "earth",
        "mineral": "salt",
        "animal": "snake"
    },
    Direction.CENTER: {
        "color": "all_colors",
        "element": "spirit",
        "mineral": "coal",
        "animal": "human"
    }
}

# Sacred cycles and ceremonies
CEREMONIES = {
    "bean_dance": {
        "timing": "february",
        "purpose": "purification",
        "elements": ["fire", "water"],
        "kachinas": ["powamu"]
    },
    "snake_dance": {
        "timing": "august",
        "purpose": "rain_bringing",
        "elements": ["water", "earth"],
        "kachinas": ["snake", "antelope"]
    },
    "flute_ceremony": {
        "timing": "august",
        "purpose": "corn_blessing",
        "elements": ["air", "water"],
        "kachinas": ["flute", "corn"]
    },
    "winter_solstice": {
        "timing": "december",
        "purpose": "sun_return",
        "elements": ["fire", "air"],
        "kachinas": ["sun", "star"]
    }
}

def get_world_cycle_attributes(cycle: WorldCycle) -> Dict:
    """Get attributes associated with a specific world cycle."""
    cycle_attributes = {
        WorldCycle.TOKPELA: {
            "color": "yellow",
            "element": "fire",
            "destruction": "destruction_by_fire"
        },
        WorldCycle.TOKPA: {
            "color": "blue",
            "element": "ice",
            "destruction": "destruction_by_ice"
        },
        WorldCycle.KUSKURZA: {
            "color": "red",
            "element": "water",
            "destruction": "destruction_by_flood"
        },
        WorldCycle.TUWAQACHI: {
            "color": "white_and_black",
            "element": "earth",
            "destruction": "pending"
        }
    }
    return cycle_attributes.get(cycle, {})

def get_ceremony_timing(celestial_event: str) -> Optional[Dict]:
    """Get ceremony details based on a celestial event."""
    for event, details in CELESTIAL_ALIGNMENTS.items():
        if event == celestial_event:
            return details
    return None

def get_directional_element(direction: Direction) -> Optional[str]:
    """Get the element associated with a direction."""
    if direction in DIRECTIONAL_CORRESPONDENCES:
        return DIRECTIONAL_CORRESPONDENCES[direction]["element"]
    return None 