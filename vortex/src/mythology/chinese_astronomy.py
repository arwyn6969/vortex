"""Chinese astronomy and mythology module."""
from enum import Enum
from typing import Dict, Optional
from datetime import datetime

class ElementType(Enum):
    """The Five Elements (Wu Xing) in Chinese philosophy."""
    WOOD = "wood"
    FIRE = "fire"
    EARTH = "earth"
    METAL = "metal"
    WATER = "water"

class Direction(Enum):
    """Cardinal directions with center."""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    CENTER = "center"

# Mapping of the Twenty-Eight Mansions
LUNAR_MANSIONS = {
    "horn": {
        "chinese_name": "角",
        "element": ElementType.WOOD,
        "direction": Direction.EAST,
        "degrees": 12,
        "stars": ["Alpha Virginis"]
    },
    "neck": {
        "chinese_name": "亢",
        "element": ElementType.METAL,
        "direction": Direction.EAST,
        "degrees": 9,
        "stars": ["Kappa Virginis"]
    },
    "base": {
        "chinese_name": "氐",
        "element": ElementType.EARTH,
        "direction": Direction.EAST,
        "degrees": 15,
        "stars": ["Alpha Librae"]
    },
    "room": {
        "chinese_name": "房",
        "element": ElementType.FIRE,
        "direction": Direction.SOUTH,
        "degrees": 5,
        "stars": ["Pi Scorpii"]
    },
    "heart": {
        "chinese_name": "心",
        "element": ElementType.FIRE,
        "direction": Direction.SOUTH,
        "degrees": 5,
        "stars": ["Sigma Scorpii"]
    }
}

# Element cycle relationships
ELEMENT_CYCLES = {
    "generating": {  # Each element generates the next
        ElementType.WOOD: ElementType.FIRE,
        ElementType.FIRE: ElementType.EARTH,
        ElementType.EARTH: ElementType.METAL,
        ElementType.METAL: ElementType.WATER,
        ElementType.WATER: ElementType.WOOD
    },
    "overcoming": {  # Each element overcomes another
        ElementType.METAL: ElementType.WOOD,  # Metal cuts Wood
        ElementType.WOOD: ElementType.EARTH,  # Wood breaks Earth
        ElementType.EARTH: ElementType.WATER, # Earth dams Water
        ElementType.WATER: ElementType.FIRE,  # Water extinguishes Fire
        ElementType.FIRE: ElementType.METAL   # Fire melts Metal
    }
}

# Celestial deities and their attributes
CELESTIAL_DEITIES = {
    "jade_emperor": {
        "domain": "heaven",
        "element": ElementType.METAL,
        "direction": Direction.CENTER,
        "stars": ["Polaris"],
        "power_base": 1.0
    },
    "xuan_wu": {
        "domain": "north",
        "element": ElementType.WATER,
        "direction": Direction.NORTH,
        "stars": ["Alpha Ophiuchi"],
        "power_base": 0.9
    },
    "zhu_que": {
        "domain": "south",
        "element": ElementType.FIRE,
        "direction": Direction.SOUTH,
        "stars": ["Alpha Hydrae"],
        "power_base": 0.9
    },
    "qing_long": {
        "domain": "east",
        "element": ElementType.WOOD,
        "direction": Direction.EAST,
        "stars": ["Alpha Scorpii"],
        "power_base": 0.9
    },
    "bai_hu": {
        "domain": "west",
        "element": ElementType.METAL,
        "direction": Direction.WEST,
        "stars": ["Alpha Tauri"],
        "power_base": 0.9
    }
}

def calculate_lunar_mansion(date: datetime) -> Optional[Dict]:
    """Calculate the current lunar mansion based on date.
    
    Args:
        date: Current date and time
    
    Returns:
        Dictionary containing mansion details if found, None otherwise
    """
    # Simplified calculation for demonstration
    day_of_year = date.timetuple().tm_yday
    mansion_index = (day_of_year % len(LUNAR_MANSIONS))
    mansion_name = list(LUNAR_MANSIONS.keys())[mansion_index]
    return LUNAR_MANSIONS[mansion_name]

def get_element_relationship(element1: ElementType, element2: ElementType) -> str:
    """Get the relationship between two elements.
    
    Args:
        element1: First element
        element2: Second element
    
    Returns:
        Relationship type: "generating", "overcoming", or "neutral"
    """
    if ELEMENT_CYCLES["generating"][element1] == element2:
        return "generating"
    elif ELEMENT_CYCLES["overcoming"][element1] == element2:
        return "overcoming"
    elif ELEMENT_CYCLES["overcoming"][element2] == element1:
        return "overcoming"  # Element2 overcomes Element1
    return "neutral"

def calculate_deity_power(deity_name: str, date: datetime) -> Dict[str, float]:
    """Calculate a deity's current power level based on celestial alignments.
    
    Args:
        deity_name: Name of the deity
        date: Current date and time
    
    Returns:
        Dictionary containing power levels and influences
    """
    if deity_name not in CELESTIAL_DEITIES:
        raise ValueError(f"Unknown deity: {deity_name}")
    
    deity = CELESTIAL_DEITIES[deity_name]
    current_mansion = calculate_lunar_mansion(date)
    
    # Base power from deity's attributes
    power = deity["power_base"]
    
    # Calculate mansion influence
    mansion_influence = 0.0
    if current_mansion:
        if current_mansion["element"] == deity["element"]:
            mansion_influence += 0.2
        if current_mansion["direction"] == deity["direction"]:
            mansion_influence += 0.1
    
    # Calculate seasonal influence
    month = date.month
    season_influence = 0.0
    if (month in [3,4,5] and deity["element"] == ElementType.WOOD) or \
       (month in [6,7,8] and deity["element"] == ElementType.FIRE) or \
       (month in [9,10,11] and deity["element"] == ElementType.METAL) or \
       (month in [12,1,2] and deity["element"] == ElementType.WATER):
        season_influence = 0.15
    
    return {
        "base_power": power,
        "mansion_influence": mansion_influence,
        "season_influence": season_influence,
        "total_power": power + mansion_influence + season_influence
    } 