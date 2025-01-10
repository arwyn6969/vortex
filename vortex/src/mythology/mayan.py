"""
Mayan calendar system, deities, and cosmic relationships.
"""
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from enum import Enum

# Major deities and their domains
DEITIES = {
    "itzamna": {
        "role": "creator",
        "element": "sky",
        "symbol": "dragon",
        "domain": "knowledge and writing"
    },
    "kukulcan": {
        "role": "teacher",
        "element": "wind",
        "symbol": "feathered serpent",
        "domain": "wisdom and learning"
    },
    "chaak": {
        "role": "sustainer",
        "element": "water",
        "symbol": "axe",
        "domain": "rain and thunder"
    },
    "kinich_ahau": {
        "role": "sun_god",
        "element": "fire",
        "symbol": "sun",
        "domain": "daylight and warmth"
    },
    "ix_chel": {
        "role": "moon_goddess",
        "element": "water",
        "symbol": "rainbow",
        "domain": "medicine and weaving"
    }
}

# Calendar systems
TZOLKIN = {
    "day_signs": [
        "imix", "ik", "akbal", "kan", "chicchan",
        "cimi", "manik", "lamat", "muluc", "oc",
        "chuen", "eb", "ben", "ix", "men",
        "cib", "caban", "etznab", "cauac", "ahau"
    ],
    "numbers": list(range(1, 14)),  # 1-13
    "cycle_length": 260  # 20 * 13
}

HAAB = {
    "months": [
        "pop", "uo", "zip", "zotz", "tzec",
        "xul", "yaxkin", "mol", "chen", "yax",
        "zac", "ceh", "mac", "kankin", "muan",
        "pax", "kayab", "cumku", "uayeb"
    ],
    "days": list(range(0, 20)),  # 0-19
    "cycle_length": 365  # (18 * 20) + 5
}

# World directions and associations
DIRECTIONS = {
    "east": {
        "color": "red",
        "element": "fire",
        "deity": "kinich_ahau",
        "symbol": "sunrise"
    },
    "north": {
        "color": "white",
        "element": "air",
        "deity": "itzamna",
        "symbol": "wisdom"
    },
    "west": {
        "color": "black",
        "element": "earth",
        "deity": "ix_chel",
        "symbol": "transformation"
    },
    "south": {
        "color": "yellow",
        "element": "water",
        "deity": "chaak",
        "symbol": "growth"
    },
    "center": {
        "color": "blue-green",
        "element": "void",
        "deity": "kukulcan",
        "symbol": "balance"
    }
}

# Underworld levels (Xibalba)
XIBALBA_LEVELS = {
    "metnal": {
        "lord": "ah_puch",
        "trial": "decay",
        "symbol": "bones",
        "element": "void"
    },
    "xuxulim_ha": {
        "lord": "one_death",
        "trial": "cold",
        "symbol": "ice",
        "element": "water"
    },
    "olhuacan": {
        "lord": "seven_death",
        "trial": "blades",
        "symbol": "knife",
        "element": "metal"
    },
    "mictlan": {
        "lord": "blood_gatherer",
        "trial": "blood",
        "symbol": "jaguar",
        "element": "fire"
    },
    "aghalom": {
        "lord": "skull_staff",
        "trial": "darkness",
        "symbol": "bat",
        "element": "air"
    }
}

# Sacred geometry patterns
SACRED_GEOMETRY = {
    "kan_cross": {
        "points": 4,
        "meaning": "four directions",
        "element": "earth",
        "usage": "temple alignment"
    },
    "quincunx": {
        "points": 5,
        "meaning": "cosmic center",
        "element": "void",
        "usage": "city planning"
    },
    "hexagon": {
        "points": 6,
        "meaning": "heaven and earth",
        "element": "air",
        "usage": "ritual spaces"
    },
    "octagon": {
        "points": 8,
        "meaning": "cosmic balance",
        "element": "water",
        "usage": "observatory design"
    }
}

# Celestial alignments
ALIGNMENTS = {
    "zenith_passage": {
        "significance": "sun directly overhead",
        "ritual": "fire ceremony",
        "deity": "kinich_ahau"
    },
    "pleiades_rising": {
        "significance": "start of dry season",
        "ritual": "first fruits",
        "deity": "itzamna"
    },
    "venus_heliacal": {
        "significance": "war and sacrifice",
        "ritual": "bloodletting",
        "deity": "kukulcan"
    }
}

class WorldLevel(Enum):
    """Levels of the Mayan universe."""
    CELESTIAL = "heavens"
    EARTHLY = "middle_world"
    UNDERWORLD = "xibalba"

def get_tzolkin_date(day_number: int) -> Tuple[int, str]:
    """Convert a day number to Tzolkin date (number and day sign).
    
    The Tzolkin calendar is a 260-day cycle combining 13 numbers with 20 day signs.
    The cycle repeats after 260 days (13 x 20).
    """
    # Adjust for 1-based counting
    adjusted_day = ((day_number - 1) % 260) + 1
    
    # Calculate number (1-13)
    number = ((adjusted_day - 1) % 13) + 1
    
    # Calculate day sign (0-19)
    sign_index = (adjusted_day - 1) % 20
    sign = TZOLKIN["day_signs"][sign_index]
    
    return (number, sign)

def get_haab_date(day_number: int) -> Tuple[int, str]:
    """Convert a day number to Haab date (day and month).
    
    The Haab calendar consists of 18 months of 20 days each,
    plus a 5-day period called Uayeb at the end of the year.
    Total cycle is 365 days.
    """
    # Adjust for 1-based counting and get position in year
    adjusted_day = (day_number - 1) % 365
    
    # Handle Uayeb period (last 5 days)
    if adjusted_day >= 360:
        return (adjusted_day - 360, "uayeb")
    
    # Regular month calculation
    month_idx = adjusted_day // 20
    day = adjusted_day % 20
    month = HAAB["months"][month_idx]
    
    return (day, month)

def get_deity_by_direction(direction: str) -> str:
    """Get the deity associated with a cardinal direction."""
    return DIRECTIONS[direction]["deity"] if direction in DIRECTIONS else None

def get_direction_properties(direction: str) -> Dict:
    """Get all properties associated with a cardinal direction."""
    return DIRECTIONS.get(direction, {}) 

def get_xibalba_level(level_name: str) -> Optional[Dict]:
    """Get details about an underworld level."""
    return XIBALBA_LEVELS.get(level_name)

def get_geometric_pattern(pattern_name: str) -> Optional[Dict]:
    """Get details about a sacred geometric pattern."""
    return SACRED_GEOMETRY.get(pattern_name)

def get_celestial_alignment(alignment_name: str) -> Optional[Dict]:
    """Get details about a celestial alignment."""
    return ALIGNMENTS.get(alignment_name)

def get_associated_rituals(deity_name: str) -> List[str]:
    """Get rituals associated with a deity."""
    rituals = []
    for alignment in ALIGNMENTS.values():
        if alignment["deity"] == deity_name:
            rituals.append(alignment["ritual"])
    return rituals

def is_sacred_date(tzolkin_number: int, tzolkin_sign: str) -> bool:
    """Determine if a Tzolkin date has special significance."""
    sacred_combinations = {
        (4, "ahau"),  # Creation date
        (8, "cumku"),  # World renewal
        (13, "kan")   # Sacred tree
    }
    return (tzolkin_number, tzolkin_sign) in sacred_combinations

def get_world_level(entity_name: str) -> Optional[WorldLevel]:
    """Determine which cosmic level an entity belongs to."""
    if entity_name in DEITIES:
        return WorldLevel.CELESTIAL
    elif entity_name in XIBALBA_LEVELS:
        return WorldLevel.UNDERWORLD
    return WorldLevel.EARTHLY if entity_name in DIRECTIONS else None 

# Enhanced calendar calculations
CALENDAR_ROUNDS = {
    "tzolkin_haab": 18980,  # 52 years (73 tzolkin x 52 haab)
    "long_count": {
        "baktun": 144000,   # 20 katun
        "katun": 7200,      # 20 tun
        "tun": 360,         # 18 uinal
        "uinal": 20,        # 20 kin
        "kin": 1            # 1 day
    }
}

# Ceremony and ritual systems
CEREMONIES = {
    "new_fire": {
        "cycle": 52,  # years
        "timing": "calendar_round_completion",
        "elements": ["fire", "incense", "offerings"],
        "deities": ["xiuhtecuhtli", "huehueteotl"]
    },
    "wayeb": {
        "cycle": 1,  # year
        "timing": "haab_end",
        "elements": ["fasting", "silence", "offerings"],
        "deities": ["chaak", "ix_chel"]
    },
    "tzolkin_renewal": {
        "cycle": 260,  # days
        "timing": "tzolkin_completion",
        "elements": ["dance", "music", "sacrifice"],
        "deities": ["itzamna", "kukulcan"]
    }
}

def calculate_long_count(days_since_epoch: int) -> Dict[str, int]:
    """Convert days since epoch to Long Count date."""
    remaining = days_since_epoch
    result = {}
    
    for unit, length in CALENDAR_ROUNDS["long_count"].items():
        result[unit] = remaining // length
        remaining %= length
    
    return result

def get_calendar_round_position(days_since_epoch: int) -> Dict[str, Tuple[int, str]]:
    """Calculate position in both Tzolkin and Haab calendars."""
    tzolkin_day = get_tzolkin_date(days_since_epoch)
    haab_day = get_haab_date(days_since_epoch)
    
    return {
        "tzolkin": tzolkin_day,
        "haab": haab_day,
        "round_number": days_since_epoch // CALENDAR_ROUNDS["tzolkin_haab"]
    }

def calculate_next_ceremony(ceremony_name: str, current_date: datetime) -> Optional[datetime]:
    """Calculate the next occurrence of a specific ceremony."""
    ceremony = CEREMONIES.get(ceremony_name)
    if not ceremony:
        return None
    
    # Convert current date to days since epoch
    epoch = datetime(2000, 1, 1)  # Using 2000 as reference point
    days_since_epoch = (current_date - epoch).days
    
    if ceremony_name == "new_fire":
        current_round = days_since_epoch // CALENDAR_ROUNDS["tzolkin_haab"]
        next_round_start = epoch + timedelta(days=(current_round + 1) * CALENDAR_ROUNDS["tzolkin_haab"])
        return next_round_start
    
    elif ceremony_name == "wayeb":
        haab_position = get_haab_date(days_since_epoch)
        days_until_wayeb = (365 - (haab_position[0] + haab_position[1] * 20)) % 365
        return current_date + timedelta(days=days_until_wayeb)
    
    elif ceremony_name == "tzolkin_renewal":
        tzolkin_position = get_tzolkin_date(days_since_epoch)
        days_until_completion = (260 - ((tzolkin_position[0] - 1) * 20 + TZOLKIN["day_signs"].index(tzolkin_position[1]))) % 260
        return current_date + timedelta(days=days_until_completion)

def is_ceremonial_period(date: datetime, ceremony_name: str) -> Tuple[bool, str]:
    """Determine if a given date falls within a ceremonial period."""
    ceremony = CEREMONIES.get(ceremony_name)
    if not ceremony:
        return (False, "Unknown ceremony")
    
    epoch = datetime(2000, 1, 1)
    days_since_epoch = (date - epoch).days
    
    if ceremony_name == "new_fire":
        position = get_calendar_round_position(days_since_epoch)
        if position["round_number"] * CALENDAR_ROUNDS["tzolkin_haab"] == days_since_epoch:
            return (True, "New Fire ceremony period")
    
    elif ceremony_name == "wayeb":
        total_days = days_since_epoch % 365
        if total_days >= 360:  # Last 5 days of Haab year
            return (True, "Wayeb period")
    
    elif ceremony_name == "tzolkin_renewal":
        tzolkin_position = get_tzolkin_date(days_since_epoch)
        if tzolkin_position == (13, "ahau"):
            return (True, "Tzolkin renewal period")
    
    return (False, "Not a ceremonial period")

def get_ceremony_requirements(ceremony_name: str) -> Optional[Dict[str, List[str]]]:
    """Get the requirements and elements needed for a ceremony."""
    ceremony = CEREMONIES.get(ceremony_name)
    if not ceremony:
        return None
    
    return {
        "elements": ceremony["elements"],
        "deities": ceremony["deities"]
    }

def calculate_sacred_alignments(date: datetime) -> List[Dict[str, str]]:
    """Calculate active celestial alignments for a given date."""
    alignments_active = []
    
    # Check zenith passage (more precise calculation)
    if 4 <= date.month <= 8 and (date.month in [6, 7] or (date.month == 5 and date.day >= 15) or (date.month == 8 and date.day <= 15)):
        alignments_active.append(ALIGNMENTS["zenith_passage"])
    
    # Check Pleiades rising (more precise timing)
    if date.month == 6 and 1 <= date.day <= 15:
        alignments_active.append(ALIGNMENTS["pleiades_rising"])
    
    # Check Venus heliacal rising (more accurate cycle calculation)
    venus_cycle = 584  # days
    epoch = datetime(2000, 1, 1)
    days_since_epoch = (date - epoch).days
    
    # Venus visibility windows
    cycle_position = days_since_epoch % venus_cycle
    if cycle_position < 7 or cycle_position >= 577:  # First and last week of cycle
        alignments_active.append(ALIGNMENTS["venus_heliacal"])
    
    return alignments_active 