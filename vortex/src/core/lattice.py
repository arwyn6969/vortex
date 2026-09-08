"""
Lattice service — the staircase between psyche, tree, guides, and ledger.

Game, LocationManager, and The Watcher should call this instead of
hard-coding Hub / Grove / Library or asking Crown for a WIF.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from ..mythology.correspondences import (
    NODES,
    PILLAR_DIMENSIONS,
    SefirahNode,
    get_node,
    get_node_by_pond,
    neighbors,
)
from ..mythology.sefirot import get_direct_connections
from .watcher_directives import DirectiveKind, WatcherDirective

ProfileMap = Dict[Union[str, object], float]


@dataclass(frozen=True)
class Placement:
    node: SefirahNode
    pillar_scores: Dict[str, float]
    dialect: str
    guide_id: str
    reason: str


class LatticeError(ValueError):
    """Illegal movement or ledger use on the tree."""


class Lattice:
    """Read-only rules for walking the tree."""

    DEFAULT_ENTRY = "tiferet"
    FOLK_THRESHOLD = 0.55

    def pillar_scores(self, profile: ProfileMap) -> Dict[str, float]:
        scores = {pillar: 0.0 for pillar in PILLAR_DIMENSIONS}
        counts = {pillar: 0 for pillar in PILLAR_DIMENSIONS}
        normalized = _normalize_profile(profile)
        for pillar, dim_names in PILLAR_DIMENSIONS.items():
            for name in dim_names:
                if name in normalized:
                    scores[pillar] += normalized[name]
                    counts[pillar] += 1
        for pillar in scores:
            if counts[pillar]:
                scores[pillar] /= counts[pillar]
            else:
                scores[pillar] = 0.5
        return scores

    def place(self, profile: ProfileMap, prefer_folk: bool = False) -> Placement:
        scores = self.pillar_scores(profile)
        dominant = max(scores, key=scores.get)
        entry = {
            "mercy": "chokhmah",
            "severity": "binah",
            "balance": "tiferet",
        }[dominant]
        if max(scores.values()) < 0.15:
            entry = self.DEFAULT_ENTRY
        node = get_node(entry)
        dialect, guide_id = self.pick_dialect(node, profile, prefer_folk)
        reason = (
            f"dominant pillar {dominant} "
            f"({scores[dominant]:.2f}) -> {node.pond}"
        )
        return Placement(
            node=node,
            pillar_scores=scores,
            dialect=dialect,
            guide_id=guide_id,
            reason=reason,
        )

    def pick_dialect(
        self,
        node: SefirahNode,
        profile: ProfileMap,
        prefer_folk: bool = False,
    ) -> Tuple[str, str]:
        normalized = _normalize_profile(profile)
        folk_signal = max(
            normalized.get("creativity", 0.0),
            normalized.get("emergent_creativity", 0.0),
            normalized.get("metaphorical_thinking", 0.0),
            normalized.get("humor", 0.0),
        )
        want_folk = prefer_folk or folk_signal >= self.FOLK_THRESHOLD
        if want_folk and node.folk_guide_id:
            return "folk", node.folk_guide_id
        return "classical", node.classical_guide_id

    def can_travel(self, current: str, destination: str) -> bool:
        current_node = _coerce_node(current)
        dest_node = _coerce_node(destination)
        if current_node.sefirah == dest_node.sefirah:
            return True
        return dest_node.sefirah in get_direct_connections(current_node.sefirah)

    def travel(self, current: str, destination: str) -> SefirahNode:
        dest_node = _coerce_node(destination)
        if not self.can_travel(current, destination):
            raise LatticeError(
                f"No path from {_coerce_node(current).pond} "
                f"to {dest_node.pond}. Streams follow sefirot paths only."
            )
        return dest_node

    def exits(self, current: str) -> List[SefirahNode]:
        node = _coerce_node(current)
        return neighbors(node.sefirah)

    def ledger_effects_allowed(self, current: str) -> bool:
        return _coerce_node(current).ledger_floor

    def assert_ledger_floor(self, current: str) -> None:
        node = _coerce_node(current)
        if not node.ledger_floor:
            raise LatticeError(
                f"{node.pond} is not Malkhut. "
                "Do not bind addresses or read holdings here."
            )

    def creation_allowed(self, current: str) -> bool:
        return _coerce_node(current).creation_unlock

    def location_graph(self) -> Dict[str, List[str]]:
        graph: Dict[str, List[str]] = {}
        for sefirah, node in NODES.items():
            graph[node.pond] = [n.pond for n in neighbors(sefirah)]
        return graph

    def describe(self, current: str) -> str:
        node = _coerce_node(current)
        exits = ", ".join(n.pond for n in self.exits(current)) or "none"
        floor = "ledger floor" if node.ledger_floor else "inner floor"
        return (
            f"{node.pond} ({node.sefirah}, pillar of {node.pillar}, {floor}). "
            f"Paths: {exits}."
        )

    def interpret_directive(
        self,
        current: str,
        directive: WatcherDirective,
    ) -> Optional[str]:
        node = _coerce_node(current)
        if directive.kind == DirectiveKind.HOLD:
            return node.pond
        if directive.kind == DirectiveKind.OPEN_PATH and directive.sefirah:
            target = get_node(directive.sefirah)
            if self.can_travel(node.sefirah, target.sefirah):
                return target.pond
            return None
        if directive.kind == DirectiveKind.SWITCH_PILLAR and directive.pillar:
            for candidate in self.exits(node.sefirah):
                if candidate.pillar == directive.pillar:
                    return candidate.pond
            return None
        if directive.kind == DirectiveKind.OFFER_HOD:
            if self.can_travel(node.sefirah, "hod"):
                return get_node("hod").pond
            return None
        if directive.kind == DirectiveKind.REQUIRE_MALKHUT:
            if self.can_travel(node.sefirah, "malkhut"):
                return get_node("malkhut").pond
            return None
        return None


def _normalize_profile(profile: ProfileMap) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for key, value in (profile or {}).items():
        name = getattr(key, "value", key)
        try:
            out[str(name).lower()] = float(value)
        except (TypeError, ValueError):
            continue
    return out


def _coerce_node(current: str) -> SefirahNode:
    raw = current.strip()
    lowered = raw.lower()
    if lowered in NODES:
        return get_node(lowered)
    by_pond = get_node_by_pond(raw)
    if by_pond:
        return by_pond
    raise LatticeError(f"Unknown place on the tree: {current}")
