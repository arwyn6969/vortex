"""
Persian cosmological system and relationships.

This module defines the Persian mythological system, including deities,
realms, sacred cycles, and relationships. It incorporates both Zoroastrian
and pre-Zoroastrian elements of Persian mythology.
"""

from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "ahura_mazda": {
        "role": "supreme_creator",
        "element": "light",
        "symbol": "faravahar",
        "description": "Supreme deity of wisdom and creation",
        "sacred_number": 1
    },
    "mithra": {
        "role": "sun_covenant",
        "element": "fire",
        "symbol": "sun_chariot",
        "description": "God of sun, justice, and contracts",
        "sacred_number": 7
    },
    "anahita": {
        "role": "water_fertility",
        "element": "water",
        "symbol": "star",
        "description": "Goddess of water, fertility, and wisdom",
        "sacred_number": 4
    },
    "verethragna": {
        "role": "victory_warrior",
        "element": "air",
        "symbol": "boar",
        "description": "God of victory and warrior spirit",
        "sacred_number": 10
    },
    "atar": {
        "role": "sacred_fire",
        "element": "fire",
        "symbol": "eternal_flame",
        "description": "Divine fire and purification",
        "sacred_number": 3
    },
    "vayu": {
        "role": "wind_breath",
        "element": "air",
        "symbol": "wind",
        "description": "God of wind and atmosphere",
        "sacred_number": 5
    }
}

# Cosmic realms
REALMS = {
    "garothman": {
        "type": "highest_heaven",
        "residents": "righteous_souls",
        "symbol": "endless_light",
        "guardian": "ahura_mazda"
    },
    "garodemana": {
        "type": "house_of_song",
        "residents": "blessed_ones",
        "symbol": "golden_throne",
        "guardian": "mithra"
    },
    "misvan_gatu": {
        "type": "intermediate",
        "residents": "mixed_souls",
        "symbol": "balance",
        "guardian": "rashnu"
    },
    "duzakh": {
        "type": "underworld",
        "residents": "wicked_souls",
        "symbol": "darkness",
        "guardian": "angra_mainyu"
    }
}

# Sacred times and festivals
FESTIVALS = {
    "nowruz": {
        "timing": "spring_equinox",
        "element": "fire",
        "purpose": "new_year",
        "deities": ["ahura_mazda"]
    },
    "tirgan": {
        "timing": "summer_solstice",
        "element": "water",
        "purpose": "water_celebration",
        "deities": ["tishtrya", "anahita"]
    },
    "mehrgan": {
        "timing": "autumn_equinox",
        "element": "air",
        "purpose": "harvest_thanksgiving",
        "deities": ["mithra"]
    },
    "yalda": {
        "timing": "winter_solstice",
        "element": "earth",
        "purpose": "light_triumph",
        "deities": ["mithra", "ahura_mazda"]
    }
}

# Sacred sites and their alignments
SACRED_SITES = {
    "persepolis": {
        "type": "ceremonial_capital",
        "alignment": "spring_equinox",
        "guardian_deity": "ahura_mazda",
        "purpose": "nowruz_celebration"
    },
    "takht_e_soleyman": {
        "type": "fire_temple",
        "alignment": "pole_star",
        "guardian_deity": "anahita",
        "purpose": "water_fire_worship"
    },
    "pasargadae": {
        "type": "royal_complex",
        "alignment": "winter_solstice",
        "guardian_deity": "mithra",
        "purpose": "royal_legitimacy"
    }
}

# Sacred elements and their attributes
SACRED_ELEMENTS = {
    "fire": {
        "guardian": "atar",
        "symbol": "eternal_flame",
        "purification": "highest",
        "temples": "atashkadeh"
    },
    "water": {
        "guardian": "anahita",
        "symbol": "sacred_spring",
        "purification": "physical",
        "temples": "ab_anbar"
    },
    "earth": {
        "guardian": "spenta_armaiti",
        "symbol": "fertile_soil",
        "purification": "burial",
        "temples": "dakhmeh"
    },
    "air": {
        "guardian": "vayu",
        "symbol": "wind",
        "purification": "breath",
        "temples": "open_shrines"
    }
}

def get_festival_deity(festival_name: str) -> List[str]:
    """Get deities associated with a festival."""
    festival = FESTIVALS.get(festival_name)
    return festival["deities"] if festival else []

def get_sacred_element(element_name: str) -> Optional[Dict]:
    """Get information about a sacred element."""
    return SACRED_ELEMENTS.get(element_name)

def get_site_alignment(site_name: str) -> Optional[str]:
    """Get the astronomical alignment of a sacred site."""
    site = SACRED_SITES.get(site_name)
    return site["alignment"] if site else None 