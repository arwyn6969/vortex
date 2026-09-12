"""Compatibility imports for the legacy Python experiments."""
from pathlib import Path

for relative in ("vortex/src/core", "vortex-next/src/core"):
    candidate = Path(__file__).resolve().parent.parent / relative
    if candidate.is_dir():
        __path__.append(str(candidate))
