"""
Celtic cosmological system and relationships.

This module defines the Celtic mythological system, including deities,
realms, sacred cycles, and relationships. It incorporates both Goidelic
(Irish, Scottish, Manx) and Brythonic (Welsh, Cornish, Breton) traditions.
"""

from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "dagda": {
        "role": "father_figure",
        "element": "earth",
        "symbol": "cauldron",
        "description": "The Good God, master of time, seasons, and abundance",
        "sacred_number": 4
    },
    "brigid": {
        "role": "triple_goddess",
        "element": "fire",
        "symbol": "sacred_flame",
        "description": "Goddess of poetry, healing, and smithcraft",
        "sacred_number": 3
    },
    "morrigan": {
        "role": "war_fate",
        "element": "air",
        "symbol": "crow",
        "description": "Goddess of war, fate, and sovereignty",
        "sacred_number": 3
    },
    "lugh": {
        "role": "master_skills",
        "element": "light",
        "symbol": "spear",
        "description": "God of all skills and arts",
        "sacred_number": 12
    },
    "cernunnos": {
        "role": "nature_lord",
        "element": "earth",
        "symbol": "antlers",
        "description": "Lord of nature, animals, and the wild",
        "sacred_number": 7
    },
    "manannan": {
        "role": "sea_psychopomp",
        "element": "water",
        "symbol": "waves",
        "description": "God of the sea and guide to Otherworld",
        "sacred_number": 9
    }
}

# Cosmic realms
REALMS = {
    "tir_na_nog": {
        "type": "otherworld",
        "residents": "tuatha_de_danann",
        "symbol": "eternal_youth",
        "guardian": "manannan"
    },
    "mag_mell": {
        "type": "paradise",
        "residents": "blessed_dead",
        "symbol": "apple_branch",
        "guardian": "lugh"
    },
    "tech_duinn": {
        "type": "afterlife",
        "residents": "dead",
        "symbol": "western_isle",
        "guardian": "donn"
    },
    "this_world": {
        "type": "mortal",
        "residents": "humans",
        "symbol": "sacred_tree",
        "guardian": "dagda"
    }
}

# Sacred cycles and festivals
FESTIVALS = {
    "samhain": {
        "timing": "october_31",
        "element": "earth",
        "purpose": "year_end_otherworld_opening",
        "deities": ["morrigan", "dagda"]
    },
    "imbolc": {
        "timing": "february_1",
        "element": "fire",
        "purpose": "spring_awakening",
        "deities": ["brigid"]
    },
    "beltane": {
        "timing": "may_1",
        "element": "fire",
        "purpose": "summer_beginning",
        "deities": ["cernunnos", "dagda"]
    },
    "lughnasadh": {
        "timing": "august_1",
        "element": "earth",
        "purpose": "harvest_games",
        "deities": ["lugh"]
    }
}

# Sacred sites and their alignments
SACRED_SITES = {
    "newgrange": {
        "type": "passage_tomb",
        "alignment": "winter_solstice_sunrise",
        "guardian_deity": "dagda",
        "purpose": "rebirth_ritual"
    },
    "tara": {
        "type": "sacred_hill",
        "alignment": "samhain_sunset",
        "guardian_deity": "morrigan",
        "purpose": "kingship_ritual"
    },
    "uisneach": {
        "type": "sacred_center",
        "alignment": "beltane_sunrise",
        "guardian_deity": "brigid",
        "purpose": "fire_festival"
    }
}

# Magical items and their powers
SACRED_ITEMS = {
    "dagdas_cauldron": {
        "owner": "dagda",
        "power": "abundance",
        "element": "water"
    },
    "spear_of_lugh": {
        "owner": "lugh",
        "power": "victory",
        "element": "fire"
    },
    "morrigan_cloak": {
        "owner": "morrigan",
        "power": "shapeshifting",
        "element": "air"
    }
}

def get_festival_deities(festival_name: str) -> List[str]:
    """Get deities associated with a festival."""
    festival = FESTIVALS.get(festival_name)
    return festival["deities"] if festival else []

def get_sacred_site_alignment(site_name: str) -> Optional[str]:
    """Get the astronomical alignment of a sacred site."""
    site = SACRED_SITES.get(site_name)
    return site["alignment"] if site else None

def get_item_power(item_name: str) -> Optional[str]:
    """Get the power of a sacred item."""
    item = SACRED_ITEMS.get(item_name)
    return item["power"] if item else None 