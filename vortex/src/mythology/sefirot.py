"""
Sefirot paths and connections definitions.
"""
from typing import Dict, List, Tuple

# Path definitions with Hebrew letters
PATHS = {
    # Middle Column (Pillar of Balance)
    11: {"letter": "aleph", "from": "keter", "to": "chokhmah", "name": "Hidden Intelligence"},
    13: {"letter": "gimel", "from": "keter", "to": "tiferet", "name": "Uniting Intelligence"},
    21: {"letter": "kaph", "from": "chokhmah", "to": "tiferet", "name": "Intelligence of Conciliation"},
    22: {"letter": "lamed", "from": "binah", "to": "tiferet", "name": "Faithful Intelligence"},
    29: {"letter": "qoph", "from": "netzach", "to": "yesod", "name": "Corporeal Intelligence"},
    30: {"letter": "resh", "from": "hod", "to": "yesod", "name": "Collecting Intelligence"},
    32: {"letter": "tav", "from": "yesod", "to": "malkhut", "name": "Administrative Intelligence"},
    
    # Right Column (Pillar of Mercy)
    12: {"letter": "beth", "from": "keter", "to": "binah", "name": "Intelligence of Transparency"},
    14: {"letter": "daleth", "from": "chokhmah", "to": "binah", "name": "Illuminating Intelligence"},
    15: {"letter": "he", "from": "chokhmah", "to": "chesed", "name": "Constitutive Intelligence"},
    17: {"letter": "zain", "from": "binah", "to": "chesed", "name": "Disposition Intelligence"},
    23: {"letter": "mem", "from": "chesed", "to": "gevurah", "name": "Stable Intelligence"},
    24: {"letter": "nun", "from": "chesed", "to": "netzach", "name": "Imaginative Intelligence"},
    27: {"letter": "peh", "from": "gevurah", "to": "hod", "name": "Exciting Intelligence"},
    28: {"letter": "tzaddi", "from": "netzach", "to": "hod", "name": "Natural Intelligence"},
    
    # Left Column (Pillar of Severity)
    10: {"letter": "yod", "from": "keter", "to": "chokhmah", "name": "Hidden Essence"},
    16: {"letter": "vav", "from": "chokhmah", "to": "gevurah", "name": "Triumphant Intelligence"},
    18: {"letter": "chet", "from": "binah", "to": "gevurah", "name": "House of Influence"},
    20: {"letter": "yod", "from": "chesed", "to": "tiferet", "name": "Intelligence of Will"},
    25: {"letter": "samekh", "from": "gevurah", "to": "tiferet", "name": "Intelligence of Trial"},
    26: {"letter": "ayin", "from": "gevurah", "to": "netzach", "name": "Renewing Intelligence"},
    31: {"letter": "shin", "from": "hod", "to": "malkhut", "name": "Perpetual Intelligence"}
}

# Helper function to get all paths connected to a Sefirah
def get_connected_paths(sefirah: str) -> List[int]:
    """Get all path numbers that connect to or from the given Sefirah."""
    return [
        path_num for path_num, path in PATHS.items()
        if path["from"] == sefirah or path["to"] == sefirah
    ]

# Helper function to get direct connections between Sefirot
def get_direct_connections(sefirah: str) -> List[str]:
    """Get all Sefirot directly connected to the given Sefirah."""
    connections = []
    for path in PATHS.values():
        if path["from"] == sefirah:
            connections.append(path["to"])
        elif path["to"] == sefirah:
            connections.append(path["from"])
    return list(set(connections))  # Remove duplicates

# The three pillars of the Tree of Life
PILLARS = {
    "mercy": ["chokhmah", "chesed", "netzach"],
    "severity": ["binah", "gevurah", "hod"],
    "balance": ["keter", "tiferet", "yesod", "malkhut"]
}

# Symbolic associations
SYMBOLS = {
    "keter": {"element": "pure spirit", "color": "pure white"},
    "chokhmah": {"element": "zodiac", "color": "grey"},
    "binah": {"element": "saturn", "color": "black"},
    "chesed": {"element": "jupiter", "color": "blue"},
    "gevurah": {"element": "mars", "color": "red"},
    "tiferet": {"element": "sun", "color": "yellow"},
    "netzach": {"element": "venus", "color": "green"},
    "hod": {"element": "mercury", "color": "orange"},
    "yesod": {"element": "moon", "color": "violet"},
    "malkhut": {"element": "earth", "color": "russet-brown"}
} 