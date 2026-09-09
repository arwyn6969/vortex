"""Session veils over the 22-letter graph.

Topology (which streams exist) lives in paths.py.
These gates are how the lattice does work in a living session.

- Crown (any stream *to* keter) is veiled until Tiferet harmony:
  Mercy and Severity both stand (each >= 0.25) while the seeker is in the heart.
- Qoph (netzach–malkhut) is veiled until the seeker Looks at Netzach.
  It is the back of the head, not a shortcut you invent.
- Sit reopens Watcher-darkened streams. Veils are unread, not closed.

The CLI Lattice.can_travel stays topological. The playable session must apply veils.
"""
from __future__ import annotations

from .paths import path_between


def crown_open(harmony: bool) -> bool:
    return bool(harmony)


def qoph_open(looked_at_netzach: bool) -> bool:
    return bool(looked_at_netzach)


def pillars_meet(mercy: float, severity: float, threshold: float = 0.25) -> bool:
    return mercy >= threshold and severity >= threshold


def stream_open(
    src: str,
    dst: str,
    *,
    harmony: bool,
    looked_at_netzach: bool,
) -> bool:
    src, dst = src.lower(), dst.lower()
    if src == dst:
        return True
    if path_between(src, dst) is None:
        return False
    if dst == "keter" and not crown_open(harmony):
        return False
    if {src, dst} == {"netzach", "malkhut"} and not qoph_open(looked_at_netzach):
        return False
    return True
