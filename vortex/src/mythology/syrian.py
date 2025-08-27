"""
Syrian Alchemical and Cosmological System

This module defines the Syrian alchemical tradition, particularly focusing on
Zosimus of Panopolis and related Hellenistic-Egyptian alchemical systems.
It incorporates both practical alchemical operations and their spiritual symbolism.
"""

from typing import Dict, List, Optional
from enum import Enum

class AlchemicalStage(Enum):
    """Stages of alchemical transformation."""
    MELANOSIS = "blackening"
    LEUKOSIS = "whitening"
    XANTHOSIS = "yellowing"
    IOSIS = "reddening"

class AlchemicalElement(Enum):
    """Primary alchemical elements."""
    MERCURY = "mercury"
    SULFUR = "sulfur"
    SALT = "salt"
    WATER = "water"
    FIRE = "fire"
    AIR = "air"
    EARTH = "earth"
    QUINTESSENCE = "quintessence"

# Core concepts and deities/principles
DEITIES = {
    "hermes_trismegistus": {
        "role": "wisdom_revealer",
        "element": AlchemicalElement.MERCURY.value,
        "symbol": "caduceus",
        "description": "Divine teacher of alchemical wisdom",
        "sacred_number": 3
    },
    "agathodaimon": {
        "role": "spiritual_guide",
        "element": AlchemicalElement.QUINTESSENCE.value,
        "symbol": "serpent",
        "description": "Good spirit guiding alchemical transformation",
        "sacred_number": 7
    },
    "isis_prophetess": {
        "role": "wisdom_keeper",
        "element": AlchemicalElement.WATER.value,
        "symbol": "veil",
        "description": "Keeper of alchemical secrets",
        "sacred_number": 9
    },
    "ostanes": {
        "role": "persian_master",
        "element": AlchemicalElement.FIRE.value,
        "symbol": "furnace",
        "description": "Persian sage of alchemical arts",
        "sacred_number": 4
    }
}

# Alchemical operations and their spiritual significance
OPERATIONS = {
    "dissolution": {
        "element": AlchemicalElement.WATER.value,
        "stage": AlchemicalStage.MELANOSIS.value,
        "symbol": "black_sea",
        "spiritual_meaning": "dissolution of ego",
        "celestial_timing": "moon_dark"
    },
    "calcination": {
        "element": AlchemicalElement.FIRE.value,
        "stage": AlchemicalStage.LEUKOSIS.value,
        "symbol": "white_ash",
        "spiritual_meaning": "purification through fire",
        "celestial_timing": "sun_zenith"
    },
    "sublimation": {
        "element": AlchemicalElement.AIR.value,
        "stage": AlchemicalStage.XANTHOSIS.value,
        "symbol": "ascending_vapor",
        "spiritual_meaning": "spiritual ascension",
        "celestial_timing": "mercury_rising"
    },
    "coagulation": {
        "element": AlchemicalElement.EARTH.value,
        "stage": AlchemicalStage.IOSIS.value,
        "symbol": "red_stone",
        "spiritual_meaning": "integration of spirit and matter",
        "celestial_timing": "saturn_culmination"
    }
}

# Sacred vessels and their symbolism
VESSELS = {
    "kerotakis": {
        "purpose": "sublimation",
        "material": "copper",
        "symbol": "feminine_receptacle",
        "planetary_association": "venus"
    },
    "tribikos": {
        "purpose": "distillation",
        "material": "glass",
        "symbol": "trinity_vessel",
        "planetary_association": "mercury"
    },
    "bain_marie": {
        "purpose": "gentle_heating",
        "material": "water_bath",
        "symbol": "womb_vessel",
        "planetary_association": "moon"
    },
    "athanor": {
        "purpose": "continuous_heat",
        "material": "clay",
        "symbol": "philosophical_furnace",
        "planetary_association": "saturn"
    }
}

# Stages of spiritual transformation
TRANSFORMATION_STAGES = [
    {
        "name": "black_dragon",
        "stage": AlchemicalStage.MELANOSIS.value,
        "symbol": "ouroboros",
        "element": AlchemicalElement.MERCURY.value,
        "significance": "initial chaos and dissolution"
    },
    {
        "name": "white_eagle",
        "stage": AlchemicalStage.LEUKOSIS.value,
        "symbol": "dove",
        "element": AlchemicalElement.SALT.value,
        "significance": "purification and clarity"
    },
    {
        "name": "yellow_lion",
        "stage": AlchemicalStage.XANTHOSIS.value,
        "symbol": "sun",
        "element": AlchemicalElement.SULFUR.value,
        "significance": "animation and vitalization"
    },
    {
        "name": "red_phoenix",
        "stage": AlchemicalStage.IOSIS.value,
        "symbol": "phoenix",
        "element": AlchemicalElement.QUINTESSENCE.value,
        "significance": "final transformation and immortality"
    }
]

# Sacred numbers and their alchemical meanings
SACRED_NUMBERS = {
    1: "unity of matter",
    2: "polarity of forces",
    3: "stages of work",
    4: "elements and directions",
    7: "planetary metals",
    9: "celestial spheres"
}

def get_stage_symbolism(stage: AlchemicalStage) -> Dict:
    """Get the symbolism associated with an alchemical stage."""
    for transform in TRANSFORMATION_STAGES:
        if transform["stage"] == stage.value:
            return transform
    return {}

def get_vessel_association(planet: str) -> Optional[Dict]:
    """Get the vessel associated with a planetary force."""
    for vessel_name, vessel_data in VESSELS.items():
        if vessel_data["planetary_association"] == planet:
            return {vessel_name: vessel_data}
    return None

def get_operation_timing(operation: str) -> Optional[str]:
    """Get the celestial timing for an alchemical operation."""
    if operation in OPERATIONS:
        return OPERATIONS[operation]["celestial_timing"]
    return None 