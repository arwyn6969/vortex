"""
Celestial Bodies and their Cross-Cultural Mythological Associations

This module manages the relationships between celestial bodies (stars, planets, constellations)
and their significance across different mythological systems.
"""

from typing import Dict, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from .celestial_alignments import CelestialBody

class CelestialType(Enum):
    """Types of celestial bodies."""
    STAR = "star"
    PLANET = "planet"
    CONSTELLATION = "constellation"
    SATELLITE = "satellite"  # e.g., moons
    ASTERISM = "asterism"    # recognizable star patterns
    NEBULA = "nebula"
    COMET = "comet"

class CelestialDomain(Enum):
    """Domains or aspects of influence for celestial bodies."""
    WISDOM = "wisdom"
    WAR = "war"
    LOVE = "love"
    FERTILITY = "fertility"
    TIME = "time"
    FATE = "fate"
    TRANSFORMATION = "transformation"
    CREATION = "creation"
    DESTRUCTION = "destruction"
    REBIRTH = "rebirth"
    NAVIGATION = "navigation"
    AGRICULTURE = "agriculture"
    PROPHECY = "prophecy"

@dataclass
class CelestialAssociation:
    """Association between a celestial body and its mythological significance."""
    mythology: str
    deity_name: str
    domains: List[CelestialDomain]
    sacred_times: List[str]
    rituals: List[str]
    symbols: List[str]
    description: str

# Comprehensive mapping of celestial bodies and their associations
CELESTIAL_MAPPINGS = {
    CelestialBody.SUN: {
        "egyptian": CelestialAssociation(
            mythology="egyptian",
            deity_name="ra",
            domains=[CelestialDomain.CREATION, CelestialDomain.TIME],
            sacred_times=["dawn", "noon", "dusk"],
            rituals=["solar_barque_journey", "morning_praise"],
            symbols=["solar_disk", "falcon", "eye_of_ra"],
            description="Supreme solar deity representing creation and daily renewal"
        ),
        "greco_roman": CelestialAssociation(
            mythology="greco_roman",
            deity_name="apollo",
            domains=[CelestialDomain.WISDOM, CelestialDomain.PROPHECY],
            sacred_times=["summer_solstice", "noon"],
            rituals=["pythian_games", "oracle_consultation"],
            symbols=["lyre", "laurel", "bow"],
            description="God of sun, prophecy, music, and healing"
        ),
        "mayan": CelestialAssociation(
            mythology="mayan",
            deity_name="kinich_ahau",
            domains=[CelestialDomain.TIME, CelestialDomain.CREATION],
            sacred_times=["zenith_passage", "solstices"],
            rituals=["fire_ceremony", "solar_renewal"],
            symbols=["four_ahau", "solar_face"],
            description="Solar deity governing time and royal power"
        )
    },
    CelestialBody.MOON: {
        "egyptian": CelestialAssociation(
            mythology="egyptian",
            deity_name="khonsu",
            domains=[CelestialDomain.TIME, CelestialDomain.FERTILITY],
            sacred_times=["new_moon", "full_moon"],
            rituals=["lunar_healing", "time_keeping"],
            symbols=["crescent", "lunar_disk"],
            description="Lunar deity of time and healing"
        ),
        "chinese": CelestialAssociation(
            mythology="chinese",
            deity_name="chang_e",
            domains=[CelestialDomain.FERTILITY, CelestialDomain.TIME],
            sacred_times=["mid_autumn", "full_moon"],
            rituals=["moon_festival", "offerings"],
            symbols=["jade_rabbit", "cassia_tree"],
            description="Lunar goddess dwelling in the moon palace"
        )
    },
    CelestialBody.VENUS: {
        "aztec": CelestialAssociation(
            mythology="aztec",
            deity_name="quetzalcoatl",
            domains=[CelestialDomain.WAR, CelestialDomain.TRANSFORMATION],
            sacred_times=["heliacal_rising", "heliacal_setting"],
            rituals=["venus_cycle_ceremonies", "warrior_initiations"],
            symbols=["feathered_serpent", "morning_star"],
            description="Venus as morning/evening star deity"
        ),
        "greco_roman": CelestialAssociation(
            mythology="greco_roman",
            deity_name="aphrodite_venus",
            domains=[CelestialDomain.LOVE, CelestialDomain.FERTILITY],
            sacred_times=["evening_star", "morning_star"],
            rituals=["love_offerings", "beauty_rituals"],
            symbols=["dove", "myrtle", "scallop_shell"],
            description="Goddess of love and beauty associated with planet Venus"
        )
    },
    CelestialBody.SIRIUS: {
        "egyptian": CelestialAssociation(
            mythology="egyptian",
            deity_name="isis",
            domains=[CelestialDomain.FERTILITY, CelestialDomain.REBIRTH],
            sacred_times=["heliacal_rising"],
            rituals=["new_year_festival", "nilometer_readings"],
            symbols=["throne", "ankh", "star"],
            description="Heliacal rising marked the annual Nile flood"
        ),
        "dogon": CelestialAssociation(
            mythology="dogon",
            deity_name="nommo",
            domains=[CelestialDomain.CREATION, CelestialDomain.WISDOM],
            sacred_times=["sirius_cycle"],
            rituals=["sigui_ceremony", "water_rituals"],
            symbols=["fish", "twin", "egg"],
            description="Sacred star system central to creation mythology"
        )
    }
}

def get_celestial_associations(body: CelestialBody, mythology: Optional[str] = None) -> Dict:
    """Get mythological associations for a celestial body.
    
    Args:
        body: The celestial body to look up
        mythology: Optional specific mythology to filter by
    
    Returns:
        Dictionary of mythological associations
    """
    associations = CELESTIAL_MAPPINGS.get(body, {})
    if mythology:
        return {mythology: associations.get(mythology)} if mythology in associations else {}
    return associations

def get_sacred_times(body: CelestialBody, mythology: str) -> List[str]:
    """Get sacred times associated with a celestial body in a specific mythology.
    
    Args:
        body: The celestial body to look up
        mythology: The specific mythology to query
    
    Returns:
        List of sacred times
    """
    association = CELESTIAL_MAPPINGS.get(body, {}).get(mythology)
    return association.sacred_times if association else []

def get_rituals(body: CelestialBody, mythology: str) -> List[str]:
    """Get rituals associated with a celestial body in a specific mythology.
    
    Args:
        body: The celestial body to look up
        mythology: The specific mythology to query
    
    Returns:
        List of associated rituals
    """
    association = CELESTIAL_MAPPINGS.get(body, {}).get(mythology)
    return association.rituals if association else []

def get_domains(body: CelestialBody, mythology: str) -> List[CelestialDomain]:
    """Get domains of influence for a celestial body in a specific mythology.
    
    Args:
        body: The celestial body to look up
        mythology: The specific mythology to query
    
    Returns:
        List of domains
    """
    association = CELESTIAL_MAPPINGS.get(body, {}).get(mythology)
    return association.domains if association else [] 