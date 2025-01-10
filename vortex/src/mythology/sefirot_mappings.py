"""
Cross-cultural mappings and correspondences for the Sefirot system.
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass

@dataclass
class SefirotCorrespondence:
    """Dataclass for holding complete Sefirot correspondences."""
    deadly_sin: str
    egyptian_deities: List[str]
    egyptian_notes: str
    greek_deity: str
    greek_notes: str
    roman_deity: str
    roman_notes: str
    planets: List[str]
    constellation: str
    tarot_card: str
    colors: List[str]

# Complete Sefirot mappings
SEFIROT_MAPPINGS = {
    "keter": SefirotCorrespondence(
        deadly_sin="pride",
        egyptian_deities=["atum", "ra", "amun"],
        egyptian_notes="Supreme creator god; dawn of divine authority. Amun as 'the hidden one' represents transcendent aspect",
        greek_deity="uranus",
        greek_notes="Primordial sky god, sometimes associated with Kronos",
        roman_deity="jupiter",
        roman_notes="King of gods, merged aspect of hidden power (Dius Fidius)",
        planets=["sun", "neptune"],
        constellation="corona_borealis",
        tarot_card="the_world",
        colors=["white", "gold"]
    ),
    "chokhmah": SefirotCorrespondence(
        deadly_sin="misguided_lust",
        egyptian_deities=["thoth", "naunet", "nun"],
        egyptian_notes="God of wisdom and knowledge. Naunet represents primordial waters of creation",
        greek_deity="apollo",
        greek_notes="God of knowledge, arts, and prophecy",
        roman_deity="mercury",
        roman_notes="Messenger and intellect",
        planets=["uranus", "mercury"],
        constellation="gemini",
        tarot_card="the_magician",
        colors=["yellow"]
    ),
    # ... continuing with all other Sefirot
}

# Ogdoad connections
OGDOAD_MAPPINGS = {
    "amun_amaunet": {
        "principle": "hiddenness",
        "sefirot_connections": ["keter", "yesod"],
        "significance": "transcendent divine power"
    },
    "nun_naunet": {
        "principle": "primordial_waters",
        "sefirot_connections": ["chokhmah", "malkhut"],
        "significance": "potential and manifestation"
    },
    "kuk_kauket": {
        "principle": "darkness",
        "sefirot_connections": ["gevurah", "hod"],
        "significance": "transformation and form"
    },
    "huh_hauhet": {
        "principle": "infinity",
        "sefirot_connections": ["binah", "netzach"],
        "significance": "boundless potential"
    }
}

# Planetary associations
PLANETARY_CORRESPONDENCES = {
    "sun": ["keter", "tiferet"],
    "moon": ["yesod"],
    "mercury": ["hod", "netzach"],
    "venus": ["netzach", "tiferet"],
    "mars": ["gevurah"],
    "jupiter": ["chesed"],
    "saturn": ["binah"],
    "uranus": ["chokhmah"],
    "neptune": ["keter"],
    "pluto": ["yesod"]
}

# Deadly sins and their remedies
SINS_AND_REMEDIES = {
    "pride": {
        "sefirot": ["keter", "hod"],
        "remedy": "humility",
        "practice": "self_reflection"
    },
    "lust": {
        "sefirot": ["chokhmah", "yesod"],
        "remedy": "chastity",
        "practice": "sublimation"
    },
    "envy": {
        "sefirot": ["binah"],
        "remedy": "gratitude",
        "practice": "appreciation"
    },
    "greed": {
        "sefirot": ["chesed"],
        "remedy": "charity",
        "practice": "giving"
    },
    "wrath": {
        "sefirot": ["gevurah"],
        "remedy": "patience",
        "practice": "meditation"
    },
    "gluttony": {
        "sefirot": ["tiferet"],
        "remedy": "temperance",
        "practice": "moderation"
    },
    "sloth": {
        "sefirot": ["netzach", "malkhut"],
        "remedy": "diligence",
        "practice": "consistent_action"
    }
}

def get_sefirot_correspondence(sefirah: str) -> Optional[SefirotCorrespondence]:
    """Get all correspondences for a specific Sefirah."""
    return SEFIROT_MAPPINGS.get(sefirah.lower())

def get_planetary_sefirot(planet: str) -> List[str]:
    """Get all Sefirot associated with a planet."""
    return PLANETARY_CORRESPONDENCES.get(planet.lower(), [])

def get_ogdoad_connections(sefirah: str) -> List[str]:
    """Get Ogdoad principles connected to a Sefirah."""
    connections = []
    for ogdoad, details in OGDOAD_MAPPINGS.items():
        if sefirah.lower() in details["sefirot_connections"]:
            connections.append(ogdoad)
    return connections

def get_sin_remedy(sin: str) -> Dict:
    """Get the remedy and practices for a specific deadly sin."""
    return SINS_AND_REMEDIES.get(sin.lower(), {})

def get_sefirot_by_sin(sin: str) -> List[str]:
    """Get all Sefirot associated with a specific deadly sin."""
    sin_data = SINS_AND_REMEDIES.get(sin.lower())
    return sin_data["sefirot"] if sin_data else [] 