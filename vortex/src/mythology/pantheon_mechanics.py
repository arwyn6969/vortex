"""
Advanced pantheon mechanics and deity interaction system.
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math
from enum import Enum

from . import dogon, mayan, sacred_geometry, chinese_astronomy

class AspectType(Enum):
    """Types of aspects (relationships) between deities."""
    CONJUNCTION = "conjunction"  # Harmonious alignment
    OPPOSITION = "opposition"    # Conflicting forces
    TRINE = "trine"             # Creative flow
    SQUARE = "square"           # Challenge and growth
    SEXTILE = "sextile"        # Opportunity

class DomainType(Enum):
    """Types of divine domains and spheres of influence."""
    CELESTIAL = "celestial"
    TERRESTRIAL = "terrestrial"
    UNDERWORLD = "underworld"
    WISDOM = "wisdom"
    CREATION = "creation"
    TRANSFORMATION = "transformation"
    HEAVEN = "heaven"         # Chinese: 天
    DIRECTIONAL = "cardinal"  # Chinese: 方位

# Deity domain mappings
DEITY_DOMAINS = {
    # Dogon deities
    "amma": {
        "primary": DomainType.CREATION,
        "secondary": [DomainType.CELESTIAL],
        "elements": ["void"],
        "power_base": 1.0
    },
    "nommo": {
        "primary": DomainType.WISDOM,
        "secondary": [DomainType.CELESTIAL, DomainType.TERRESTRIAL],
        "elements": ["water"],
        "power_base": 0.8
    },
    "yurugu": {
        "primary": DomainType.TRANSFORMATION,
        "secondary": [DomainType.UNDERWORLD],
        "elements": ["earth"],
        "power_base": 0.7
    },
    "lebe": {
        "primary": DomainType.TERRESTRIAL,
        "secondary": [DomainType.TRANSFORMATION],
        "elements": ["earth"],
        "power_base": 0.6
    },
    
    # Mayan deities
    "itzamna": {
        "primary": DomainType.WISDOM,
        "secondary": [DomainType.CREATION],
        "elements": ["sky"],
        "power_base": 1.0
    },
    "kukulcan": {
        "primary": DomainType.TRANSFORMATION,
        "secondary": [DomainType.WISDOM],
        "elements": ["wind"],
        "power_base": 0.9
    },
    "chaak": {
        "primary": DomainType.TERRESTRIAL,
        "secondary": [DomainType.CELESTIAL],
        "elements": ["water"],
        "power_base": 0.8
    },
    "kinich_ahau": {
        "primary": DomainType.CELESTIAL,
        "secondary": [DomainType.CREATION],
        "elements": ["fire"],
        "power_base": 0.9
    },
    "ix_chel": {
        "primary": DomainType.TRANSFORMATION,
        "secondary": [DomainType.WISDOM],
        "elements": ["water"],
        "power_base": 0.8
    },
    # Chinese deities
    "jade_emperor": {
        "primary": DomainType.HEAVEN,
        "secondary": [DomainType.CELESTIAL],
        "elements": ["metal"],
        "power_base": 1.0
    },
    "xuan_wu": {
        "primary": DomainType.DIRECTIONAL,
        "secondary": [DomainType.WISDOM],
        "elements": ["water"],
        "power_base": 0.9
    },
    "zhu_que": {
        "primary": DomainType.DIRECTIONAL,
        "secondary": [DomainType.CELESTIAL],
        "elements": ["fire"],
        "power_base": 0.9
    },
    "qing_long": {
        "primary": DomainType.DIRECTIONAL,
        "secondary": [DomainType.TRANSFORMATION],
        "elements": ["wood"],
        "power_base": 0.9
    },
    "bai_hu": {
        "primary": DomainType.DIRECTIONAL,
        "secondary": [DomainType.WISDOM],
        "elements": ["metal"],
        "power_base": 0.9
    }
}

# Aspect influence weights
ASPECT_WEIGHTS = {
    AspectType.CONJUNCTION: 1.0,
    AspectType.OPPOSITION: -0.5,
    AspectType.TRINE: 0.8,
    AspectType.SQUARE: 0.2,
    AspectType.SEXTILE: 0.4
}

def calculate_deity_power(deity_name: str, date: datetime) -> Dict[str, float]:
    """Calculate a deity's current power level based on celestial alignments.
    
    Args:
        deity_name: Name of the deity
        date: Current date and time
    
    Returns:
        Dictionary containing power levels and influences
    """
    if deity_name not in DEITY_DOMAINS:
        raise ValueError(f"Unknown deity: {deity_name}")
    
    deity = DEITY_DOMAINS[deity_name]
    base_power = deity["power_base"]
    celestial_power = 0.0
    domain_power = 0.0
    
    # Calculate Chinese celestial influence
    if deity_name in chinese_astronomy.CELESTIAL_DEITIES:
        chinese_power = chinese_astronomy.calculate_deity_power(deity_name, date)
        celestial_power += chinese_power["mansion_influence"]
        celestial_power += chinese_power["season_influence"]
        
        # Additional power for Chinese deities
        current_mansion = chinese_astronomy.calculate_lunar_mansion(date)
        if current_mansion:
            if current_mansion["element"] == chinese_astronomy.ElementType(deity["elements"][0]):
                celestial_power += 0.3
            celestial_power += 0.1  # Base celestial influence
    
    # Calculate Dogon influence
    elif deity_name in dogon.DEITIES:
        sirius_pos = dogon.calculate_sirius_position(date)
        if sirius_pos["position"] == "zenith":
            celestial_power += 0.3
        elif sirius_pos["visibility"] == "visible":
            celestial_power += 0.1
    
    # Calculate Mayan influence
    elif deity_name in mayan.DEITIES:
        alignments = mayan.calculate_sacred_alignments(date)
        for alignment in alignments:
            if alignment["deity"] == deity_name:
                celestial_power += 0.2
    
    # Calculate domain influence
    if deity["primary"] in [DomainType.CELESTIAL, DomainType.HEAVEN]:
        domain_power += celestial_power * 1.5
    elif DomainType.CELESTIAL in deity["secondary"]:
        domain_power += celestial_power
    
    # Calculate element influence for Chinese deities
    if deity_name in chinese_astronomy.CELESTIAL_DEITIES:
        current_mansion = chinese_astronomy.calculate_lunar_mansion(date)
        if current_mansion and current_mansion["element"].value in deity["elements"]:
            domain_power += 0.2
    
    total_power = base_power + celestial_power + domain_power
    
    return {
        "base_power": base_power,
        "celestial_influence": celestial_power,
        "domain_influence": domain_power,
        "total_power": total_power
    }

def calculate_deity_aspect(deity1: str, deity2: str, date: datetime) -> Optional[Tuple[AspectType, float]]:
    """Calculate the aspect (relationship) between two deities.
    
    Args:
        deity1: Name of first deity
        deity2: Name of second deity
        date: Current date and time
    
    Returns:
        Tuple of (AspectType, strength) if aspect exists, None otherwise
    """
    if deity1 not in DEITY_DOMAINS or deity2 not in DEITY_DOMAINS:
        return None
    
    d1 = DEITY_DOMAINS[deity1]
    d2 = DEITY_DOMAINS[deity2]
    
    # Special case for opposing deities
    if (deity1 == "amma" and deity2 == "yurugu") or (deity2 == "amma" and deity1 == "yurugu"):
        return (AspectType.OPPOSITION, 1.0)
    
    # Check for same element first
    if d1["elements"] == d2["elements"]:
        if d1["primary"] == d2["primary"]:
            aspect = AspectType.CONJUNCTION
        else:
            aspect = AspectType.SEXTILE
    
    # Check Chinese element relationships for Chinese deities
    elif deity1 in chinese_astronomy.CELESTIAL_DEITIES and deity2 in chinese_astronomy.CELESTIAL_DEITIES:
        d1_element = chinese_astronomy.ElementType(d1["elements"][0])
        d2_element = chinese_astronomy.ElementType(d2["elements"][0])
        relationship = chinese_astronomy.get_element_relationship(d1_element, d2_element)
        
        if relationship == "generating":
            aspect = AspectType.TRINE
        elif relationship == "overcoming":
            aspect = AspectType.SQUARE
        else:
            aspect = AspectType.OPPOSITION
    
    # Calculate base aspect based on domains for other cases
    elif d1["primary"] == d2["primary"]:
        aspect = AspectType.CONJUNCTION
    elif d1["primary"] in d2["secondary"] or d2["primary"] in d1["secondary"]:
        aspect = AspectType.TRINE
    else:
        # Cross-cultural aspects
        if (d1["primary"] == DomainType.HEAVEN and d2["primary"] == DomainType.CELESTIAL) or \
           (d2["primary"] == DomainType.HEAVEN and d1["primary"] == DomainType.CELESTIAL):
            aspect = AspectType.CONJUNCTION
        elif any(domain in [DomainType.WISDOM, DomainType.CREATION] for domain in [d1["primary"], d2["primary"]]):
            aspect = AspectType.TRINE
        else:
            aspect = AspectType.SQUARE
    
    # Calculate aspect strength
    base_strength = ASPECT_WEIGHTS[aspect]
    
    # Modify strength based on celestial positions
    d1_power = calculate_deity_power(deity1, date)
    d2_power = calculate_deity_power(deity2, date)
    power_ratio = min(d1_power["total_power"], d2_power["total_power"]) / max(d1_power["total_power"], d2_power["total_power"])
    
    final_strength = base_strength * power_ratio
    
    return (aspect, final_strength)

def find_harmonious_deities(deity_name: str, date: datetime, min_strength: float = 0.5) -> List[Dict[str, any]]:
    """Find deities that have harmonious relationships with the given deity.
    
    Args:
        deity_name: Name of the deity to find relationships for
        date: Current date and time
        min_strength: Minimum aspect strength to consider
    
    Returns:
        List of dictionaries containing deity names and their aspects
    """
    harmonious = []
    
    for other_deity in DEITY_DOMAINS:
        if other_deity == deity_name:
            continue
        
        aspect = calculate_deity_aspect(deity_name, other_deity, date)
        if aspect is None:
            continue
        
        aspect_type, strength = aspect
        if aspect_type in [AspectType.CONJUNCTION, AspectType.TRINE, AspectType.SEXTILE] and strength >= min_strength:
            harmonious.append({
                "deity": other_deity,
                "aspect": aspect_type,
                "strength": strength
            })
    
    return sorted(harmonious, key=lambda x: x["strength"], reverse=True)

def generate_divine_challenge(deity_name: str, date: datetime) -> Dict[str, any]:
    """Generate a challenge or trial based on a deity's domains and current power.
    
    Args:
        deity_name: Name of the deity
        date: Current date and time
    
    Returns:
        Dictionary containing challenge details
    """
    if deity_name not in DEITY_DOMAINS:
        raise ValueError(f"Unknown deity: {deity_name}")
    
    deity = DEITY_DOMAINS[deity_name]
    power = calculate_deity_power(deity_name, date)
    
    # Base challenge difficulty on deity's current power
    difficulty = math.ceil(power["total_power"] * 10)  # 1-10 scale
    
    # Generate challenge elements based on domain
    elements = []
    if deity["primary"] in [DomainType.CELESTIAL, DomainType.HEAVEN]:
        elements.append("astronomical_observation")
    if deity["primary"] == DomainType.WISDOM:
        elements.append("riddle_solving")
    if deity["primary"] == DomainType.TRANSFORMATION:
        elements.append("pattern_recognition")
    if deity["primary"] == DomainType.DIRECTIONAL:
        elements.append("directional_alignment")
    if DomainType.TERRESTRIAL in [deity["primary"]] + deity["secondary"]:
        elements.append("physical_task")
    
    # Add Chinese-specific elements for Chinese deities
    if deity_name in chinese_astronomy.CELESTIAL_DEITIES:
        current_mansion = chinese_astronomy.calculate_lunar_mansion(date)
        if current_mansion:
            mansion_key = list(chinese_astronomy.LUNAR_MANSIONS.keys())[0]  # Get the first mansion key
            elements.append(f"lunar_mansion_{mansion_key}")
            elements.append(f"element_{deity['elements'][0]}")  # Use deity's primary element
    
    # Add sacred geometry component if appropriate
    if power["celestial_influence"] > 0.2:
        pattern = "octagon" if difficulty > 7 else "kan_cross"
        geometry = sacred_geometry.calculate_temple_alignment(pattern, 23.5, True)
        elements.append(f"sacred_geometry_{pattern}")
    
    return {
        "deity": deity_name,
        "difficulty": difficulty,
        "elements": elements,
        "power_level": power["total_power"],
        "domain": deity["primary"].value,
        "requirements": {
            "celestial_alignment": power["celestial_influence"] > 0,
            "sacred_space": difficulty > 5,
            "offerings": list(deity["elements"])
        }
    } 