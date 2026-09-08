"""
Single correspondence table for the Vortex lattice.

Every sefirah hangs a pond, two guide dialects, pillar, ledger floor,
and Watcher concerns. Zone classes and classical myth files remain the
rich text; this module is the index they should all agree with.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .sefirot import PILLARS, SefirotAttribute, get_direct_connections


@dataclass(frozen=True)
class SefirahNode:
    """One office on the tree, with every dialect that may speak it."""

    sefirah: str
    attribute: SefirotAttribute
    pillar: str
    pond: str
    zone_module: str
    classical_guide_id: str
    folk_guide_id: Optional[str]
    folk_guide_class: Optional[str]
    element: str
    color: str
    ledger_floor: bool
    creation_unlock: bool
    watcher_concerns: Tuple[str, ...]
    token_categories: Tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""


NODES: Dict[str, SefirahNode] = {
    "keter": SefirahNode(
        sefirah="keter",
        attribute=SefirotAttribute.KETER,
        pillar="balance",
        pond="Crown Pond",
        zone_module="vortex.src.zones.crown_pond",
        classical_guide_id="thoth",
        folk_guide_id=None,
        folk_guide_class=None,
        element="pure spirit",
        color="pure white",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("pacing", "overreach"),
        notes="Crown does not handle keys. Hidden beginning.",
    ),
    "chokhmah": SefirahNode(
        sefirah="chokhmah",
        attribute=SefirotAttribute.CHOKMAH,
        pillar="mercy",
        pond="Wisdom Pond",
        zone_module="vortex.src.zones.wisdom_pond",
        classical_guide_id="thoth",
        folk_guide_id="wise_pepe",
        folk_guide_class="WisePepe",
        element="zodiac",
        color="grey",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("curiosity", "scatter"),
        notes="Brain Galaxy / Wisdom. Flash of insight.",
    ),
    "binah": SefirahNode(
        sefirah="binah",
        attribute=SefirotAttribute.BINAH,
        pillar="severity",
        pond="Zen Zone",
        zone_module="vortex.src.zones.zen_zone",
        classical_guide_id="maat",
        folk_guide_id="monk_pepe",
        folk_guide_class="MonkPepe",
        element="saturn",
        color="black",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("rigidity", "stillness"),
        notes="Form, discipline, understanding.",
    ),
    "chesed": SefirahNode(
        sefirah="chesed",
        attribute=SefirotAttribute.CHESED,
        pillar="mercy",
        pond="Mercy Pond",
        zone_module="vortex.src.zones.mercy_pond",
        classical_guide_id="isis",
        folk_guide_id="cozy_pepe",
        folk_guide_class="CozyPepe",
        element="jupiter",
        color="blue",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("overgiving", "comfort-trap"),
        notes="Comfy Cabin register lives here.",
    ),
    "gevurah": SefirahNode(
        sefirah="gevurah",
        attribute=SefirotAttribute.GEVURAH,
        pillar="severity",
        pond="Severity Pond",
        zone_module="vortex.src.zones.severity_pond",
        classical_guide_id="set",
        folk_guide_id="giga_pepe",
        folk_guide_class="GigaPepe",
        element="mars",
        color="red",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("harshness", "burnout"),
        notes="Gains Grotto is the folk name for this office.",
    ),
    "tiferet": SefirahNode(
        sefirah="tiferet",
        attribute=SefirotAttribute.TIFERET,
        pillar="balance",
        pond="Vibe Temple",
        zone_module="vortex.src.zones.vibe_temple",
        classical_guide_id="horus",
        folk_guide_id="vibe_pepe",
        folk_guide_class="VibePepe",
        element="sun",
        color="yellow",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("vanity", "harmony"),
        notes="Beauty / vibe / heart. Festival register allowed.",
    ),
    "netzach": SefirahNode(
        sefirah="netzach",
        attribute=SefirotAttribute.NETZACH,
        pillar="mercy",
        pond="Boundaries Pond",
        zone_module="vortex.src.zones.boundaries_pond",
        classical_guide_id="wadjet",
        folk_guide_id=None,
        folk_guide_class=None,
        element="venus",
        color="green",
        ledger_floor=False,
        creation_unlock=False,
        watcher_concerns=("endurance", "obsession"),
        notes="Victory and edges. Folk dialect still open.",
    ),
    "hod": SefirahNode(
        sefirah="hod",
        attribute=SefirotAttribute.HOD,
        pillar="severity",
        pond="Meme Studio",
        zone_module="vortex.src.zones.meme_studio",
        classical_guide_id="thoth",
        folk_guide_id="artist_pepe",
        folk_guide_class="ArtistPepe",
        element="mercury",
        color="orange",
        ledger_floor=False,
        creation_unlock=True,
        watcher_concerns=("glibness", "signal"),
        token_categories=("PEPE", "DANK", "STAMPS"),
        notes="Language, memes, stamps as images. Creation rights begin here.",
    ),
    "yesod": SefirahNode(
        sefirah="yesod",
        attribute=SefirotAttribute.YESOD,
        pillar="balance",
        pond="Harmony Pond",
        zone_module="vortex.src.zones.harmony_pond",
        classical_guide_id="isis",
        folk_guide_id=None,
        folk_guide_class=None,
        element="moon",
        color="violet",
        ledger_floor=False,
        creation_unlock=True,
        watcher_concerns=("illusion", "foundation"),
        notes="Foundation before kingdom. Dream logic is in-bounds.",
    ),
    "malkhut": SefirahNode(
        sefirah="malkhut",
        attribute=SefirotAttribute.MALKHUT,
        pillar="balance",
        pond="Kingdom Pond",
        zone_module="vortex.src.zones.kingdom_pond",
        classical_guide_id="spider_woman",
        folk_guide_id=None,
        folk_guide_class=None,
        element="earth",
        color="russet",
        ledger_floor=True,
        creation_unlock=True,
        watcher_concerns=("materialism", "binding"),
        token_categories=("PEPE", "BOSHI", "DANK", "FAKE", "SRC20", "STAMPS", "XCP"),
        notes="Only floor that may bind an address or read holdings.",
    ),
}


PILLAR_DIMENSIONS = {
    "mercy": (
        "empathy",
        "creativity",
        "curiosity",
        "social_awareness",
    ),
    "severity": (
        "decision_making",
        "strategic_thinking",
        "persistence",
        "moral_alignment",
    ),
    "balance": (
        "self_reflection",
        "wisdom",
        "adaptability",
        "contextual_fluidity",
    ),
}


def get_node(sefirah: str) -> SefirahNode:
    key = sefirah.lower()
    if key not in NODES:
        raise KeyError(f"Unknown sefirah: {sefirah}")
    return NODES[key]


def get_node_by_pond(pond: str) -> Optional[SefirahNode]:
    target = pond.strip().lower()
    for node in NODES.values():
        if node.pond.lower() == target:
            return node
    return None


def neighbors(sefirah: str) -> List[SefirahNode]:
    return [get_node(name) for name in get_direct_connections(sefirah)]


def nodes_for_pillar(pillar: str) -> List[SefirahNode]:
    sefirot = PILLARS.get(pillar.lower(), [])
    return [get_node(name) for name in sefirot]
