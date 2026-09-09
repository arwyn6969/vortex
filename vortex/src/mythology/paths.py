"""The 22 streams of the Tree: letter, title, endpoints.

Travel is undirected. Lookup with path_between(a, b).
Keep this table in lockstep with the playable web lattice.
Meanings are revealed on a second walk of the same stream.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

Path = Tuple[str, str, str, str]  # from, to, letter, title

PATH_LETTERS: List[Path] = [
    ("keter", "chokhmah", "Aleph", "Ox / Air"),
    ("keter", "binah", "Beth", "House"),
    ("keter", "tiferet", "Gimel", "Camel / Moon"),
    ("chokhmah", "binah", "Daleth", "Door"),
    ("chokhmah", "tiferet", "Heh", "Window"),
    ("chokhmah", "chesed", "Vav", "Nail"),
    ("binah", "tiferet", "Zain", "Sword"),
    ("binah", "gevurah", "Cheth", "Fence"),
    ("chesed", "gevurah", "Teth", "Serpent"),
    ("chesed", "tiferet", "Yod", "Hand"),
    ("chesed", "netzach", "Kaph", "Palm"),
    ("gevurah", "tiferet", "Lamed", "Ox-goad"),
    ("gevurah", "hod", "Mem", "Water"),
    ("tiferet", "netzach", "Nun", "Fish"),
    ("tiferet", "hod", "Samekh", "Prop"),
    ("tiferet", "yesod", "Ayin", "Eye"),
    ("netzach", "hod", "Peh", "Mouth"),
    ("netzach", "yesod", "Tzaddi", "Fish-hook"),
    ("netzach", "malkhut", "Qoph", "Back of head"),
    ("hod", "yesod", "Resh", "Head / Sun"),
    ("hod", "malkhut", "Shin", "Tooth / Fire"),
    ("yesod", "malkhut", "Tav", "Mark / Saturn"),
]

PATH_MEANINGS: Dict[str, str] = {
    "Aleph": "Breath before a name. The ox pulls what has no words yet.",
    "Beth": "A house is a boundary you live in. Form begins as a roof.",
    "Gimel": "The camel crosses the empty stretch. Crown and heart do not touch without a journey.",
    "Daleth": "Flash meets form. A door that only opens one way at a time.",
    "Heh": "Insight looking at beauty. Do not climb through. Look.",
    "Vav": "A nail joins. Wisdom that cannot hold is only weather.",
    "Zain": "Understanding cuts. Beauty survives the honest blade.",
    "Cheth": "Discipline is a fence, not a wall. Severity lives inside it.",
    "Teth": "Mercy and severity coil. Neither eats the other if the spine is true.",
    "Yod": "Kindness offered as a hand, not a flood.",
    "Kaph": "The open palm that can still close. Endurance begins as a gift.",
    "Lamed": "A goad teaches the heart to walk straight.",
    "Mem": "Severity poured into language. Water takes the shape of the vessel.",
    "Nun": "Beauty that swims. Victory is not a pose.",
    "Samekh": "The heart props the mouth. Speech that cannot stand falls.",
    "Ayin": "The eye of the tree. Foundation is what the heart is willing to see.",
    "Peh": "Endurance speaking. A mouth without a fence is a flood.",
    "Tzaddi": "Victory hooks the foundation. Do not land every fish.",
    "Qoph": "The unconscious descent. Kingdom can be reached without looking forward.",
    "Resh": "Language becoming ground. The sun of the mouth sets into the moon.",
    "Shin": "A word that can burn into the floor of the world.",
    "Tav": "The mark. Foundation writes itself into form.",
}


def path_key(a: str, b: str) -> str:
    return ":".join(sorted((a.lower(), b.lower())))


def path_between(a: str, b: str) -> Optional[Dict[str, str]]:
    a, b = a.lower(), b.lower()
    for src, dst, letter, title in PATH_LETTERS:
        if {src, dst} == {a, b}:
            return {
                "from": src,
                "to": dst,
                "letter": letter,
                "title": title,
                "meaning": PATH_MEANINGS[letter],
            }
    return None


def all_letters() -> List[str]:
    return [p[2] for p in PATH_LETTERS]


def path_meaning(letter: str) -> str:
    return PATH_MEANINGS[letter]
