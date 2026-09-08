"""
Silent director vocabulary.

The Watcher never speaks to the player. It emits directives that the
face-guide and the lattice must obey. Keep this module free of LLM calls.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DirectiveKind(str, Enum):
    HOLD = "hold"  # stay on this sefirah
    OPEN_PATH = "open_path"  # allow a specific stream
    SWITCH_PILLAR = "switch_pillar"  # nudge toward mercy / severity / balance
    SLOW = "slow"  # fewer challenges, more silence
    INTENSIFY = "intensify"  # raise difficulty on this office
    CHANGE_DIALECT = "change_dialect"  # classical <-> folk
    OFFER_HOD = "offer_hod"  # invite language / meme / stamp work
    REQUIRE_MALKHUT = "require_malkhut"  # only valid if player is ready to bind
    SOFTEN = "soften"  # Gevurah running hot
    AUTHENTICITY_CHECK = "authenticity_check"  # Watcher wants another probe


@dataclass(frozen=True)
class WatcherDirective:
    kind: DirectiveKind
    sefirah: Optional[str] = None
    pillar: Optional[str] = None
    dialect: Optional[str] = None  # "classical" | "folk"
    reason: str = ""

    def as_prompt_constraint(self) -> str:
        """One line the face-guide system prompt can include."""
        bits = [f"WATCHER DIRECTIVE: {self.kind.value}"]
        if self.sefirah:
            bits.append(f"sefirah={self.sefirah}")
        if self.pillar:
            bits.append(f"pillar={self.pillar}")
        if self.dialect:
            bits.append(f"dialect={self.dialect}")
        if self.reason:
            bits.append(self.reason)
        return " | ".join(bits)
