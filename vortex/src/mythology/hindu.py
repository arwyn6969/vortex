"""
Hindu cosmological system and relationships.
"""
from typing import Dict, List, Optional
from enum import Enum

# Core concepts and deities
DEITIES = {
    "brahma": {
        "role": "creator",
        "element": "ether",
        "symbol": "lotus",
        "description": "Creator of the universe",
        "sacred_number": 4
    },
    "vishnu": {
        "role": "preserver",
        "element": "water",
        "symbol": "chakra",
        "description": "Preserver of creation",
        "sacred_number": 7
    },
    "shiva": {
        "role": "destroyer",
        "element": "fire",
        "symbol": "trishul",
        "description": "Destroyer and transformer",
        "sacred_number": 3
    },
    "devi": {
        "role": "divine_mother",
        "element": "earth",
        "symbol": "lotus",
        "description": "Supreme feminine power",
        "sacred_number": 9
    }
}

# Cosmic realms (Lokas)
LOKAS = {
    "satya_loka": {
        "type": "highest",
        "residents": "brahma",
        "symbol": "truth",
        "guardian": "brahma"
    },
    "bhu_loka": {
        "type": "physical",
        "residents": "humans",
        "symbol": "earth",
        "guardian": "indra"
    },
    "patala_loka": {
        "type": "subterranean",
        "residents": "nagas",
        "symbol": "serpent",
        "guardian": "vasuki"
    }
}

# Creation stages (Yugas)
YUGAS = [
    {
        "name": "satya_yuga",
        "symbol": "truth",
        "element": "gold",
        "significance": "perfect age"
    },
    {
        "name": "treta_yuga",
        "symbol": "fire",
        "element": "silver",
        "significance": "three-quarters virtue"
    },
    {
        "name": "dwapara_yuga",
        "symbol": "doubt",
        "element": "copper",
        "significance": "half virtue"
    },
    {
        "name": "kali_yuga",
        "symbol": "discord",
        "element": "iron",
        "significance": "current age of darkness"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    1: "supreme consciousness",
    3: "trimurti and gunas",
    4: "vedas and ages",
    7: "chakras and realms",
    9: "planets and powers",
    108: "ultimate completion"
}

class YugaPhase(Enum):
    """Enumeration of Yuga phases in Hindu cosmology."""
    SATYA = "satya_yuga"
    TRETA = "treta_yuga"
    DWAPARA = "dwapara_yuga"
    KALI = "kali_yuga"

# Cosmic structure
COSMIC_STRUCTURE = {
    "upper": ["satya_loka", "jana_loka", "tapo_loka"],
    "middle": ["svar_loka", "bhuvar_loka", "bhu_loka"],
    "lower": ["atala", "vitala", "patala"]
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "brahma_vishnu": {"type": "creation_preservation", "significance": "existence"},
    "vishnu_shiva": {"type": "preservation_destruction", "significance": "cycles"},
    "shiva_shakti": {"type": "consciousness_energy", "significance": "unity"},
    "guru_disciple": {"type": "knowledge", "significance": "transmission"}
}

def get_loka_guardian(loka: str) -> Optional[str]:
    """Get the guardian of a specific loka."""
    loka_data = LOKAS.get(loka)
    return loka_data["guardian"] if loka_data else None

def get_sacred_number_meaning(number: int) -> Optional[str]:
    """Get the significance of a sacred number."""
    return SACRED_NUMBERS.get(number)

def get_yuga_stage(phase: YugaPhase) -> Optional[Dict]:
    """Get details about a specific yuga stage."""
    return next(
        (stage for stage in YUGAS if stage["name"] == phase.value),
        None
    )

def get_cosmic_level(location: str) -> Optional[str]:
    """Get the cosmic level where a location exists."""
    for level, locations in COSMIC_STRUCTURE.items():
        if location in locations:
            return level
    return None

def get_deity_aspect(deity_name: str) -> Optional[str]:
    """Get the primary aspect/role of a deity."""
    deity = DEITIES.get(deity_name)
    return deity["role"] if deity else None 