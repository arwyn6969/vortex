"""
Sefirot paths and connections definitions.

Travel uses PATH_LETTERS in paths.py (22 undirected streams).
The numbered PATHS dict below is the older named-intelligence table;
get_direct_connections reads the 22-letter table so the lattice agrees
with the playable layer.
"""
from typing import Dict, List
from enum import Enum

from .paths import PATH_LETTERS


class SefirotAttribute(Enum):
    """Enum for the ten Sefirot attributes."""
    KETER = "keter"
    CHOKMAH = "chokhmah"
    BINAH = "binah"
    CHESED = "chesed"
    GEVURAH = "gevurah"
    TIFERET = "tiferet"
    NETZACH = "netzach"
    HOD = "hod"
    YESOD = "yesod"
    MALKHUT = "malkhut"


# Path definitions with Hebrew letters (historical numbering; letters may duplicate).
PATHS = {
    11: {"letter": "aleph", "from": "keter", "to": "chokhmah", "name": "Hidden Intelligence"},
    13: {"letter": "gimel", "from": "keter", "to": "tiferet", "name": "Uniting Intelligence"},
    21: {"letter": "kaph", "from": "chokhmah", "to": "tiferet", "name": "Intelligence of Conciliation"},
    22: {"letter": "lamed", "from": "binah", "to": "tiferet", "name": "Faithful Intelligence"},
    29: {"letter": "qoph", "from": "netzach", "to": "yesod", "name": "Corporeal Intelligence"},
    30: {"letter": "resh", "from": "hod", "to": "yesod", "name": "Collecting Intelligence"},
    32: {"letter": "tav", "from": "yesod", "to": "malkhut", "name": "Administrative Intelligence"},
    12: {"letter": "beth", "from": "keter", "to": "binah", "name": "Intelligence of Transparency"},
    14: {"letter": "daleth", "from": "chokhmah", "to": "binah", "name": "Illuminating Intelligence"},
    15: {"letter": "he", "from": "chokhmah", "to": "chesed", "name": "Constitutive Intelligence"},
    17: {"letter": "zain", "from": "binah", "to": "chesed", "name": "Disposition Intelligence"},
    23: {"letter": "mem", "from": "chesed", "to": "gevurah", "name": "Stable Intelligence"},
    24: {"letter": "nun", "from": "chesed", "to": "netzach", "name": "Imaginative Intelligence"},
    27: {"letter": "peh", "from": "gevurah", "to": "hod", "name": "Exciting Intelligence"},
    28: {"letter": "tzaddi", "from": "netzach", "to": "hod", "name": "Natural Intelligence"},
    10: {"letter": "yod", "from": "keter", "to": "chokhmah", "name": "Hidden Essence"},
    16: {"letter": "vav", "from": "chokhmah", "to": "gevurah", "name": "Triumphant Intelligence"},
    18: {"letter": "chet", "from": "binah", "to": "gevurah", "name": "House of Influence"},
    20: {"letter": "yod", "from": "chesed", "to": "tiferet", "name": "Intelligence of Will"},
    25: {"letter": "samekh", "from": "gevurah", "to": "tiferet", "name": "Intelligence of Trial"},
    26: {"letter": "ayin", "from": "gevurah", "to": "netzach", "name": "Renewing Intelligence"},
    31: {"letter": "shin", "from": "hod", "to": "malkhut", "name": "Perpetual Intelligence"},
}


def get_connected_paths(sefirah: str) -> List[int]:
    """Get all path numbers that connect to or from the given Sefirah."""
    return [
        path_num for path_num, path in PATHS.items()
        if path["from"] == sefirah or path["to"] == sefirah
    ]


def get_direct_connections(sefirah: str) -> List[str]:
    """Get all Sefirot directly connected to the given Sefirah (22-letter table)."""
    key = sefirah.lower()
    connections: List[str] = []
    for src, dst, _letter, _title in PATH_LETTERS:
        if src == key:
            connections.append(dst)
        elif dst == key:
            connections.append(src)
    return list(dict.fromkeys(connections))


PILLARS = {
    "mercy": ["chokhmah", "chesed", "netzach"],
    "severity": ["binah", "gevurah", "hod"],
    "balance": ["keter", "tiferet", "yesod", "malkhut"],
}

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
    "malkhut": {"element": "earth", "color": "russet-brown"},
}
