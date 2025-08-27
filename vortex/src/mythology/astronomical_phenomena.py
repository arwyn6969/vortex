"""
Astronomical Phenomena and their Mythological Significance

This module provides utilities for calculating astronomical phenomena and their
mythological significance across different cultures.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from .celestial_alignments import CelestialBody, AlignmentType
from .celestial_bodies import CelestialDomain, get_celestial_associations

class PhenomenonType(Enum):
    """Types of astronomical phenomena."""
    ECLIPSE = "eclipse"
    METEOR_SHOWER = "meteor_shower"
    COMET = "comet"
    NOVA = "nova"
    CONJUNCTION = "conjunction"
    OPPOSITION = "opposition"
    RETROGRADE = "retrograde"
    STATION = "station"
    HELIACAL_RISING = "heliacal_rising"
    HELIACAL_SETTING = "heliacal_setting"
    CULMINATION = "culmination"

class SignificanceLevel(Enum):
    """Levels of mythological significance."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"
    TRANSFORMATIVE = "transformative"

@dataclass
class AstronomicalPhenomenon:
    """Represents an astronomical phenomenon and its mythological significance."""
    type: PhenomenonType
    bodies: List[CelestialBody]
    start_time: datetime
    duration: timedelta
    peak_time: Optional[datetime]
    visibility_regions: List[str]
    significance_level: SignificanceLevel
    cultural_interpretations: Dict[str, str]
    associated_deities: Dict[str, List[str]]
    recommended_rituals: Dict[str, List[str]]

# Major meteor showers and their mythological associations
METEOR_SHOWERS = {
    "perseids": {
        "peak": "August 12-13",
        "radiant": "Perseus",
        "mythologies": {
            "greco_roman": {
                "deities": ["perseus", "medusa"],
                "significance": "tears of St. Lawrence, golden rain of Zeus",
                "rituals": ["star_gazing", "wish_making"]
            },
            "chinese": {
                "deities": ["chi_xi", "zhi_nu"],
                "significance": "reunion of the weaver girl and cowherd",
                "rituals": ["offerings", "love_prayers"]
            }
        }
    },
    "leonids": {
        "peak": "November 17-18",
        "radiant": "Leo",
        "mythologies": {
            "egyptian": {
                "deities": ["sekhmet", "horus"],
                "significance": "tears of the lion goddess",
                "rituals": ["protection_ceremonies", "renewal_rites"]
            },
            "persian": {
                "deities": ["mithra"],
                "significance": "celestial fire arrows",
                "rituals": ["fire_ceremonies", "warrior_initiations"]
            }
        }
    }
}

# Eclipse significance across cultures
ECLIPSE_SIGNIFICANCE = {
    "chinese": {
        "solar": {
            "meaning": "celestial dragon devouring sun",
            "deities": ["dragon_king"],
            "rituals": ["drum_beating", "dragon_appeasement"],
            "significance_level": SignificanceLevel.CRITICAL
        },
        "lunar": {
            "meaning": "harmony disruption between yin and yang",
            "deities": ["chang_e"],
            "rituals": ["moon_viewing", "balance_restoration"],
            "significance_level": SignificanceLevel.MAJOR
        }
    },
    "aztec": {
        "solar": {
            "meaning": "cosmic battle between light and darkness",
            "deities": ["huitzilopochtli", "coyolxauhqui"],
            "rituals": ["sun_offering", "warrior_ceremonies"],
            "significance_level": SignificanceLevel.TRANSFORMATIVE
        },
        "lunar": {
            "meaning": "divine transformation",
            "deities": ["tecciztecatl"],
            "rituals": ["night_vigils", "purification_rites"],
            "significance_level": SignificanceLevel.MAJOR
        }
    },
    "norse": {
        "solar": {
            "meaning": "wolf Skoll catching the sun",
            "deities": ["skoll", "sol"],
            "rituals": ["protection_chants", "sun_calling"],
            "significance_level": SignificanceLevel.CRITICAL
        },
        "lunar": {
            "meaning": "wolf Hati catching the moon",
            "deities": ["hati", "mani"],
            "rituals": ["moon_howling", "warding_rituals"],
            "significance_level": SignificanceLevel.MAJOR
        }
    }
}

def calculate_phenomenon_power(phenomenon: AstronomicalPhenomenon, location: Tuple[float, float], time: datetime) -> float:
    """Calculate the power/significance of an astronomical phenomenon.
    
    Args:
        phenomenon: The astronomical phenomenon
        location: (latitude, longitude) tuple
        time: Time of observation
        
    Returns:
        Float value representing the phenomenon's power (0.0 to 1.0)
    """
    base_power = 0.5  # Start with moderate significance
    
    # Adjust for phenomenon type
    type_multipliers = {
        PhenomenonType.ECLIPSE: 1.5,
        PhenomenonType.METEOR_SHOWER: 1.2,
        PhenomenonType.COMET: 1.4,
        PhenomenonType.NOVA: 1.3,
        PhenomenonType.CONJUNCTION: 1.1,
        PhenomenonType.OPPOSITION: 1.1,
        PhenomenonType.RETROGRADE: 0.9,
        PhenomenonType.STATION: 0.8,
        PhenomenonType.HELIACAL_RISING: 1.2,
        PhenomenonType.HELIACAL_SETTING: 1.2,
        PhenomenonType.CULMINATION: 1.0
    }
    base_power *= type_multipliers.get(phenomenon.type, 1.0)
    
    # Adjust for significance level
    significance_multipliers = {
        SignificanceLevel.MINOR: 0.7,
        SignificanceLevel.MODERATE: 1.0,
        SignificanceLevel.MAJOR: 1.3,
        SignificanceLevel.CRITICAL: 1.6,
        SignificanceLevel.TRANSFORMATIVE: 2.0
    }
    base_power *= significance_multipliers.get(phenomenon.significance_level, 1.0)
    
    # Adjust for timing relative to peak
    if phenomenon.peak_time:
        time_diff = abs((time - phenomenon.peak_time).total_seconds())
        time_factor = 1.0 - (time_diff / (phenomenon.duration.total_seconds() / 2))
        base_power *= max(0.1, time_factor)
    
    return min(1.0, base_power)

def get_cultural_interpretation(phenomenon: AstronomicalPhenomenon, mythology: str) -> Optional[Dict]:
    """Get the cultural interpretation of a phenomenon for a specific mythology.
    
    Args:
        phenomenon: The astronomical phenomenon
        mythology: The mythology to get interpretation for
        
    Returns:
        Dictionary containing cultural interpretation details if found
    """
    if mythology in phenomenon.cultural_interpretations:
        interpretation = {
            "meaning": phenomenon.cultural_interpretations[mythology],
            "deities": phenomenon.associated_deities.get(mythology, []),
            "rituals": phenomenon.recommended_rituals.get(mythology, [])
        }
        
        # Add celestial associations
        for body in phenomenon.bodies:
            associations = get_celestial_associations(body, mythology)
            if associations:
                interpretation["celestial_associations"] = associations
                
        return interpretation
    return None

def get_recommended_practices(phenomenon: AstronomicalPhenomenon, mythology: str) -> List[str]:
    """Get recommended spiritual practices for a phenomenon in a specific tradition.
    
    Args:
        phenomenon: The astronomical phenomenon
        mythology: The mythology to get practices for
        
    Returns:
        List of recommended practices
    """
    practices = phenomenon.recommended_rituals.get(mythology, [])
    
    # Add general practices based on phenomenon type
    if phenomenon.type == PhenomenonType.ECLIPSE:
        practices.extend(["meditation", "fasting", "prayer"])
    elif phenomenon.type == PhenomenonType.METEOR_SHOWER:
        practices.extend(["star_gazing", "wish_making", "contemplation"])
    elif phenomenon.type == PhenomenonType.RETROGRADE:
        practices.extend(["reflection", "review", "patience"])
        
    return list(set(practices))  # Remove duplicates

def is_auspicious_time(phenomenon: AstronomicalPhenomenon, mythology: str) -> bool:
    """Determine if a phenomenon represents an auspicious time in a tradition.
    
    Args:
        phenomenon: The astronomical phenomenon
        mythology: The mythology to check
        
    Returns:
        Boolean indicating if the time is considered auspicious
    """
    # This would involve more complex cultural and astronomical calculations
    # For now, return a simplified check
    return phenomenon.significance_level in [SignificanceLevel.MAJOR, SignificanceLevel.TRANSFORMATIVE] 