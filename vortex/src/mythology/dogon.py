"""
Dogon cosmological system and relationships.
"""
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta

# Core concepts and deities
DEITIES = {
    "amma": {
        "role": "creator",
        "element": "void",
        "symbol": "egg",
        "description": "Supreme creator god",
        "sacred_number": 1
    },
    "nommo": {
        "role": "civilizer",
        "element": "water",
        "symbol": "fish",
        "description": "Ancestral spirits and teachers",
        "sacred_number": 8
    },
    "yurugu": {
        "role": "disruptor",
        "element": "earth",
        "symbol": "fox",
        "description": "Represents imperfection and incompleteness",
        "sacred_number": 7
    },
    "lebe": {
        "role": "earth_priest",
        "element": "earth",
        "symbol": "snake",
        "description": "First ancestor to die and be resurrected",
        "sacred_number": 4
    }
}

# Astronomical knowledge
CELESTIAL_BODIES = {
    "po_tolo": {  # Sirius B
        "type": "star",
        "significance": "seed of creation",
        "cycle_years": 50,
        "associated_deity": "nommo"
    },
    "sigi_tolo": {  # Sirius A
        "type": "star",
        "significance": "witness star",
        "cycle_years": 1,
        "associated_deity": "amma"
    },
    "emma_ya": {  # Sorghum star
        "type": "constellation",
        "significance": "female fertility",
        "cycle_years": 1,
        "associated_deity": "nommo"
    }
}

# Creation stages
CREATION_STAGES = [
    {
        "name": "egg_vibration",
        "symbol": "spiral",
        "element": "void",
        "significance": "initial movement"
    },
    {
        "name": "po_separation",
        "symbol": "seed",
        "element": "fire",
        "significance": "division of matter"
    },
    {
        "name": "water_creation",
        "symbol": "fish",
        "element": "water",
        "significance": "birth of nommo"
    },
    {
        "name": "earth_formation",
        "symbol": "clay",
        "element": "earth",
        "significance": "physical realm"
    }
]

# Sacred numbers and their meanings
SACRED_NUMBERS = {
    1: "unity and creation",
    2: "duality and balance",
    3: "harmony and completion",
    4: "directions and elements",
    7: "imperfection and seeking",
    8: "nommo twins and guidance"
}

class CreationPhase(Enum):
    """Enumeration of creation phases in Dogon cosmology."""
    INITIAL = "egg_vibration"
    SEPARATION = "po_separation"
    WATER = "water_creation"
    EARTH = "earth_formation"

def get_celestial_cycle(body_name: str) -> Optional[int]:
    """Get the cycle length in years for a celestial body."""
    body = CELESTIAL_BODIES.get(body_name)
    return body["cycle_years"] if body else None

def get_sacred_number_meaning(number: int) -> Optional[str]:
    """Get the significance of a sacred number."""
    return SACRED_NUMBERS.get(number)

def get_creation_stage(phase: CreationPhase) -> Optional[Dict]:
    """Get details about a specific creation stage."""
    return next(
        (stage for stage in CREATION_STAGES if stage["name"] == phase.value),
        None
    )

def get_deity_by_number(sacred_number: int) -> Optional[str]:
    """Find deity associated with a sacred number."""
    for deity_name, deity in DEITIES.items():
        if deity.get("sacred_number") == sacred_number:
            return deity_name
    return None

# Cosmological levels
COSMOS_LEVELS = {
    "to": {"meaning": "universe", "symbol": "egg"},
    "yala": {"meaning": "stars", "symbol": "sirius"},
    "tolo": {"meaning": "sun", "symbol": "copper"},
    "duno": {"meaning": "moon", "symbol": "iron"},
    "aduno": {"meaning": "earth", "symbol": "clay"}
}

# Sacred relationships and connections
RELATIONSHIPS = {
    "amma_nommo": {"type": "creation", "significance": "order"},
    "nommo_humans": {"type": "teaching", "significance": "civilization"},
    "yurugu_disorder": {"type": "disruption", "significance": "change"},
    "lebe_earth": {"type": "mediation", "significance": "renewal"}
}

# Symbolic associations
SYMBOLS = {
    "spiral": "creation and growth",
    "egg": "potential and universe",
    "sirius": "knowledge and guidance",
    "water": "purification and life",
    "fox": "disorder and incompleteness"
}

def get_deity_relationships(deity: str) -> List[str]:
    """Get all relationships associated with a deity."""
    return [
        rel for rel in RELATIONSHIPS.keys()
        if deity in rel
    ]

def get_cosmic_level(entity: str) -> str:
    """Get the cosmic level associated with an entity."""
    for level, details in COSMOS_LEVELS.items():
        if entity in details["symbol"]:
            return level
    return None 

def get_celestial_body_by_deity(deity_name: str) -> List[str]:
    """Get celestial bodies associated with a deity."""
    return [
        body_name for body_name, body in CELESTIAL_BODIES.items()
        if body["associated_deity"] == deity_name
    ] 

# Astronomical calculations and cycles
SIRIUS_CYCLE = {
    "po_tolo_orbit": 50,  # years
    "digitaria_cycle": 1,  # year
    "emma_ya_period": 365,  # days
    "celestial_positions": {
        "ascending": {"start_month": 6, "end_month": 8},
        "zenith": {"start_month": 9, "end_month": 10},
        "descending": {"start_month": 11, "end_month": 1},
        "nadir": {"start_month": 2, "end_month": 5}
    }
}

# Ritual and ceremony systems
CEREMONIES = {
    "sigui": {
        "cycle": 60,  # years
        "purpose": "death and rebirth",
        "elements": ["masks", "sacred_words", "dance"],
        "requirements": ["elder_presence", "sacred_space"]
    },
    "bulu": {
        "cycle": 1,  # year
        "purpose": "planting and harvest",
        "elements": ["seeds", "water", "earth"],
        "requirements": ["new_moon", "clear_sky"]
    },
    "dama": {
        "cycle": "as_needed",
        "purpose": "elevation of spirits",
        "elements": ["masks", "dance", "drums"],
        "requirements": ["death_occurrence", "community_gathering"]
    }
}

def calculate_sirius_position(date: datetime) -> Dict[str, str]:
    """Calculate the position of Sirius based on date."""
    month = date.month
    for position, period in SIRIUS_CYCLE["celestial_positions"].items():
        if period["start_month"] <= month <= period["end_month"]:
            return {
                "position": position,
                "visibility": "visible" if 21 <= date.hour or date.hour <= 4 else "hidden",
                "phase": "waxing" if date.day < 15 else "waning"
            }
    return {"position": "transitional", "visibility": "unknown", "phase": "unknown"}

def get_next_ceremony(ceremony_name: str, current_date: datetime) -> Optional[datetime]:
    """Calculate the next occurrence of a specific ceremony."""
    ceremony = CEREMONIES.get(ceremony_name)
    if not ceremony:
        return None
    
    if ceremony["cycle"] == "as_needed":
        return None  # Cannot predict as-needed ceremonies
        
    if ceremony_name == "sigui":
        # Sigui cycle started in 1967
        base_year = 1967
        current_cycle = (current_date.year - base_year) // 60
        next_cycle = current_cycle + 1
        return datetime(base_year + (next_cycle * 60), 1, 1)
    
    elif ceremony_name == "bulu":
        # Bulu happens at the first new moon of the agricultural season
        next_date = current_date
        if current_date.month >= 6:  # If past June
            next_date = next_date.replace(year=next_date.year + 1)
        return next_date.replace(month=6, day=1)  # Approximate

def get_ritual_requirements(ceremony_name: str) -> Optional[List[str]]:
    """Get the requirements for a specific ceremony."""
    ceremony = CEREMONIES.get(ceremony_name)
    return ceremony.get("requirements") if ceremony else None

def is_auspicious_time(date: datetime, ceremony_name: str) -> Tuple[bool, str]:
    """Determine if a given time is auspicious for a ceremony."""
    ceremony = CEREMONIES.get(ceremony_name)
    if not ceremony:
        return (False, "Unknown ceremony")
    
    sirius_pos = calculate_sirius_position(date)
    
    if ceremony_name == "sigui":
        if sirius_pos["position"] != "zenith":
            return (False, "Sirius must be at zenith for Sigui ceremony")
    elif ceremony_name == "bulu":
        if sirius_pos["visibility"] != "visible":
            return (False, "Sirius must be visible for Bulu ceremony")
    elif ceremony_name == "dama":
        if sirius_pos["phase"] != "waxing":
            return (False, "Sirius should be in waxing phase for Dama ceremony")
    
    return (True, "Time is auspicious") 