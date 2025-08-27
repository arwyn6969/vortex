"""
Aztec cosmological system and relationships.

This module defines the Aztec mythological system, including deities,
realms, sacred cycles, and relationships. It incorporates the complex
calendrical system and the concept of cyclical creation and destruction.
"""

from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "huitzilopochtli": {
        "role": "sun_war",
        "element": "fire",
        "symbol": "hummingbird",
        "description": "God of sun, war, and human sacrifice",
        "sacred_number": 13
    },
    "quetzalcoatl": {
        "role": "wisdom_wind",
        "element": "air",
        "symbol": "feathered_serpent",
        "description": "God of wisdom, wind, and civilization",
        "sacred_number": 9
    },
    "tezcatlipoca": {
        "role": "night_sorcery",
        "element": "darkness",
        "symbol": "smoking_mirror",
        "description": "God of night, sorcery, and destiny",
        "sacred_number": 4
    },
    "tlaloc": {
        "role": "rain_fertility",
        "element": "water",
        "symbol": "goggle_eyes",
        "description": "God of rain, fertility, and lightning",
        "sacred_number": 7
    },
    "coatlicue": {
        "role": "earth_mother",
        "element": "earth",
        "symbol": "serpent_skirt",
        "description": "Goddess of earth, life, and death",
        "sacred_number": 2
    },
    "mictlantecuhtli": {
        "role": "death_underworld",
        "element": "earth",
        "symbol": "skull",
        "description": "God of death and the underworld",
        "sacred_number": 6
    }
}

# Cosmic realms
REALMS = {
    "topan": {
        "type": "celestial_realm",
        "levels": 13,
        "residents": "celestial_deities",
        "symbol": "sun",
        "guardian": "huitzilopochtli"
    },
    "tlalticpac": {
        "type": "earthly_realm",
        "levels": 1,
        "residents": "humans",
        "symbol": "earth_disk",
        "guardian": "tlaloc"
    },
    "mictlan": {
        "type": "underworld",
        "levels": 9,
        "residents": "dead",
        "symbol": "crossed_bones",
        "guardian": "mictlantecuhtli"
    }
}

# Creation cycles (Suns)
SUNS = {
    "nahui_ocelotl": {
        "element": "earth",
        "ruler": "tezcatlipoca",
        "destruction": "jaguars",
        "inhabitants": "giants"
    },
    "nahui_ehecatl": {
        "element": "wind",
        "ruler": "quetzalcoatl",
        "destruction": "hurricanes",
        "inhabitants": "monkeys"
    },
    "nahui_quiahuitl": {
        "element": "fire",
        "ruler": "tlaloc",
        "destruction": "fire_rain",
        "inhabitants": "turkeys"
    },
    "nahui_atl": {
        "element": "water",
        "ruler": "chalchiuhtlicue",
        "destruction": "flood",
        "inhabitants": "fish_people"
    },
    "nahui_ollin": {
        "element": "motion",
        "ruler": "huitzilopochtli",
        "destruction": "earthquakes",
        "inhabitants": "current_humans"
    }
}

# Sacred calendar cycles
CALENDAR = {
    "tonalpohualli": {
        "type": "ritual",
        "length": 260,
        "components": ["13_numbers", "20_day_signs"],
        "purpose": "divination"
    },
    "xiuhpohualli": {
        "type": "solar",
        "length": 365,
        "components": ["18_months", "5_nemontemi"],
        "purpose": "agricultural"
    },
    "xiuhmolpilli": {
        "type": "century",
        "length": 52,
        "components": ["calendar_round"],
        "purpose": "new_fire"
    }
}

# Sacred sites and their alignments
SACRED_SITES = {
    "templo_mayor": {
        "type": "pyramid",
        "alignment": "equinox",
        "deities": ["huitzilopochtli", "tlaloc"],
        "purpose": "cosmic_order"
    },
    "teotihuacan": {
        "type": "city",
        "alignment": "pleiades",
        "deities": ["quetzalcoatl"],
        "purpose": "celestial_harmony"
    },
    "malinalco": {
        "type": "temple",
        "alignment": "solar_zenith",
        "deities": ["eagle_warriors"],
        "purpose": "warrior_initiation"
    }
}

def get_sun_cycle(sun_name: str) -> Optional[Dict]:
    """Get information about a specific Sun (creation cycle)."""
    return SUNS.get(sun_name)

def get_calendar_cycle(cycle_name: str) -> Optional[Dict]:
    """Get information about a calendar cycle."""
    return CALENDAR.get(cycle_name)

def get_site_deities(site_name: str) -> List[str]:
    """Get deities associated with a sacred site."""
    site = SACRED_SITES.get(site_name)
    return site["deities"] if site else []

def calculate_tonalpohualli_date(day_number: int, day_sign: str) -> Dict:
    """Calculate a date in the ritual calendar."""
    # This would contain actual calendar calculation logic
    return {
        "day_number": day_number,
        "day_sign": day_sign,
        "trecena": (day_number - 1) // 13 + 1,
        "veintena": day_sign
    } 