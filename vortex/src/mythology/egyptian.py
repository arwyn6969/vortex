"""
Egyptian cosmological system and relationships.

This module defines the ancient Egyptian mythological system, including deities,
realms, sacred cycles, and relationships. It incorporates both the Heliopolitan
and Hermopolitan creation myths, as well as later syncretic developments.
"""

from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "ra": {
        "role": "sun_creator",
        "element": "light",
        "symbol": "solar_disk",
        "description": "Supreme solar deity and creator",
        "sacred_number": 1
    },
    "osiris": {
        "role": "death_rebirth",
        "element": "earth",
        "symbol": "djed_pillar",
        "description": "God of death, resurrection, and fertility",
        "sacred_number": 7
    },
    "isis": {
        "role": "magic_motherhood",
        "element": "water",
        "symbol": "throne",
        "description": "Goddess of magic, motherhood, and healing",
        "sacred_number": 3
    },
    "horus": {
        "role": "sky_kingship",
        "element": "air",
        "symbol": "falcon",
        "description": "God of sky and divine kingship",
        "sacred_number": 2
    },
    "thoth": {
        "role": "wisdom_writing",
        "element": "air",
        "symbol": "ibis",
        "description": "God of wisdom, writing, and magic",
        "sacred_number": 8
    },
    "anubis": {
        "role": "death_protection",
        "element": "earth",
        "symbol": "jackal",
        "description": "God of death, mummification, and afterlife",
        "sacred_number": 5
    },
    "maat": {
        "role": "truth_order",
        "element": "aether",
        "symbol": "feather",
        "description": "Goddess of truth, justice, and cosmic order",
        "sacred_number": 4
    }
}

# Cosmic realms
REALMS = {
    "duat": {
        "type": "underworld",
        "residents": "deceased",
        "symbol": "stars",
        "guardian": "osiris"
    },
    "nun": {
        "type": "primordial_waters",
        "residents": "potential_beings",
        "symbol": "watery_abyss",
        "guardian": "hapi"
    },
    "manu": {
        "type": "western_mountain",
        "residents": "setting_sun",
        "symbol": "western_horizon",
        "guardian": "hathor"
    },
    "bakhu": {
        "type": "eastern_mountain",
        "residents": "rising_sun",
        "symbol": "eastern_horizon",
        "guardian": "khepri"
    }
}

# Sacred cycles and festivals
FESTIVALS = {
    "wepet_renpet": {
        "timing": "sirius_rising",
        "element": "water",
        "purpose": "new_year",
        "deities": ["isis", "osiris"]
    },
    "opet": {
        "timing": "second_month_akhet",
        "element": "air",
        "purpose": "divine_kingship_renewal",
        "deities": ["amun", "mut", "khonsu"]
    },
    "beautiful_feast_valley": {
        "timing": "second_month_shemu",
        "element": "earth",
        "purpose": "ancestor_communion",
        "deities": ["amun", "hathor"]
    },
    "heb_sed": {
        "timing": "thirty_year_reign",
        "element": "fire",
        "purpose": "royal_renewal",
        "deities": ["horus", "osiris"]
    }
}

# Sacred sites and their alignments
SACRED_SITES = {
    "great_pyramid": {
        "type": "pyramid",
        "alignment": "orion_belt",
        "guardian_deity": "osiris",
        "purpose": "royal_ascension"
    },
    "karnak": {
        "type": "temple_complex",
        "alignment": "winter_solstice",
        "guardian_deity": "amun_ra",
        "purpose": "divine_marriage"
    },
    "abu_simbel": {
        "type": "rock_temple",
        "alignment": "solar_alignment",
        "guardian_deity": "ra",
        "purpose": "solar_worship"
    }
}

# Sacred objects and their powers
SACRED_OBJECTS = {
    "ankh": {
        "type": "symbol",
        "power": "eternal_life",
        "element": "spirit"
    },
    "was_scepter": {
        "type": "staff",
        "power": "dominion",
        "element": "air"
    },
    "eye_of_horus": {
        "type": "amulet",
        "power": "protection",
        "element": "light"
    }
}

def get_festival_timing(festival_name: str) -> Optional[str]:
    """Get the timing of a festival."""
    festival = FESTIVALS.get(festival_name)
    return festival["timing"] if festival else None

def get_site_purpose(site_name: str) -> Optional[str]:
    """Get the purpose of a sacred site."""
    site = SACRED_SITES.get(site_name)
    return site["purpose"] if site else None

def get_object_power(object_name: str) -> Optional[str]:
    """Get the power of a sacred object."""
    obj = SACRED_OBJECTS.get(object_name)
    return obj["power"] if obj else None 