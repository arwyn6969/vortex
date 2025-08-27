"""
Yoruba cosmological system and relationships.

This module defines the Yoruba mythological system, including Orishas,
realms, sacred cycles, and relationships. It incorporates the complex
system of divination (Ifá) and the concept of ashe (life force).
"""

from typing import Dict, List, Optional
from enum import Enum

# Core concepts and Orishas
ORISHAS = {
    "olodumare": {
        "role": "supreme_creator",
        "element": "light",
        "symbol": "sun",
        "description": "Supreme creator deity",
        "sacred_number": 1
    },
    "orunmila": {
        "role": "wisdom_divination",
        "element": "spirit",
        "symbol": "divination_board",
        "description": "Orisha of wisdom, knowledge, and divination",
        "sacred_number": 16
    },
    "eshu": {
        "role": "messenger_trickster",
        "element": "crossroads",
        "symbol": "staff",
        "description": "Divine messenger and trickster",
        "sacred_number": 3
    },
    "shango": {
        "role": "thunder_justice",
        "element": "fire",
        "symbol": "double_axe",
        "description": "Orisha of thunder, lightning, and justice",
        "sacred_number": 6
    },
    "yemoja": {
        "role": "mother_waters",
        "element": "water",
        "symbol": "waves",
        "description": "Mother of waters and motherhood",
        "sacred_number": 7
    },
    "oshun": {
        "role": "love_rivers",
        "element": "fresh_water",
        "symbol": "mirror",
        "description": "Orisha of love, fresh waters, and prosperity",
        "sacred_number": 5
    },
    "ogun": {
        "role": "iron_technology",
        "element": "metal",
        "symbol": "machete",
        "description": "Orisha of iron, technology, and war",
        "sacred_number": 7
    }
}

# Cosmic realms
REALMS = {
    "orun": {
        "type": "spirit_realm",
        "residents": "orishas",
        "symbol": "white_cloth",
        "guardian": "olodumare"
    },
    "aye": {
        "type": "physical_realm",
        "residents": "humans",
        "symbol": "earth",
        "guardian": "onile"
    },
    "ile_ife": {
        "type": "sacred_center",
        "residents": "priests",
        "symbol": "sacred_grove",
        "guardian": "orunmila"
    }
}

# Ifá divination system
IFA_SYSTEM = {
    "odu": {
        "count": 256,
        "major": 16,
        "minor": 240,
        "guardian": "orunmila"
    },
    "tools": {
        "opon_ifa": "divination_board",
        "ikin": "sacred_palm_nuts",
        "opele": "divination_chain"
    },
    "elements": {
        "earth": "ile",
        "air": "ofurufu",
        "fire": "ina",
        "water": "omi"
    }
}

# Sacred festivals and ceremonies
FESTIVALS = {
    "odun_ifa": {
        "timing": "june",
        "purpose": "wisdom_renewal",
        "deity": "orunmila",
        "offerings": ["kola_nuts", "bitter_cola"]
    },
    "odun_shango": {
        "timing": "august",
        "purpose": "thunder_justice",
        "deity": "shango",
        "offerings": ["ram", "okra"]
    },
    "odun_oshun": {
        "timing": "august",
        "purpose": "love_prosperity",
        "deity": "oshun",
        "offerings": ["honey", "yellow_fruits"]
    },
    "odun_ogun": {
        "timing": "september",
        "purpose": "technology_strength",
        "deity": "ogun",
        "offerings": ["palm_oil", "dog"]
    }
}

# Sacred sites and their significance
SACRED_SITES = {
    "oshun_grove": {
        "location": "osogbo",
        "deity": "oshun",
        "purpose": "healing_blessing",
        "sacred_objects": ["river", "shrine"]
    },
    "ogun_shrine": {
        "location": "ire_ekiti",
        "deity": "ogun",
        "purpose": "metallurgy_protection",
        "sacred_objects": ["anvil", "tools"]
    },
    "shango_temple": {
        "location": "oyo",
        "deity": "shango",
        "purpose": "justice_power",
        "sacred_objects": ["thunderstones", "drums"]
    }
}

def get_orisha_attributes(orisha_name: str) -> Optional[Dict]:
    """Get attributes of an Orisha."""
    return ORISHAS.get(orisha_name)

def get_ifa_elements() -> Dict:
    """Get the elemental correspondences in Ifá."""
    return IFA_SYSTEM["elements"]

def get_festival_offerings(festival_name: str) -> Optional[List[str]]:
    """Get the required offerings for a festival."""
    festival = FESTIVALS.get(festival_name)
    return festival["offerings"] if festival else None

def get_sacred_site_purpose(site_name: str) -> Optional[str]:
    """Get the purpose of a sacred site."""
    site = SACRED_SITES.get(site_name)
    return site["purpose"] if site else None 