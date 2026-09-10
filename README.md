# VORTEX

VORTEX is a mystical journey through interconnected spiritual realms, combining ancient wisdom with modern gameplay mechanics. Players explore sacred spaces, solve challenges, and progress through symbolic pathways while collecting tokens and achievements.

The engine is the Tree of Life. Ponds are sefirot. Streams are the 22 paths (Aleph through Tav). Guides are dialects of the same office (classical and folk). The Watcher is the unspoken director. Bitcoin is Malkhut — a public record, never a key dump.

Doctrine: [docs/doctrine/THE_LATTICE.md](docs/doctrine/THE_LATTICE.md)

Playable layer: [docs/doctrine/PLAY.md](docs/doctrine/PLAY.md)

Next (suggestions): [docs/doctrine/NEXT.md](docs/doctrine/NEXT.md)

## Core Features

- **Mystical Framework**: pond system, sacred streams, multiple traditions, symbolic pathways
- **Gameplay Systems**: profile adaptation, tokens, achievements, dynamic difficulty
- **Spiritual Integration**: Sefirot navigation, Egyptian / Dogon / Mayan correspondences
- **LLM-Powered Dialogue**: guide conversations shaped by profile and Watcher directives
- **The Lattice**: ten sefirot ↔ ten ponds ↔ classical + folk guides; travel only along defined paths; ledger effects only at Kingdom Pond; bind by signed message, never by pasted WIF
- **The 22 streams**: named letters in `vortex/src/mythology/paths.py`. A second walk names the meaning.
- **Veils**: Crown stays unnamed until Mercy and Severity meet in Tiferet. Qoph (the back of the head) lights when you Look at Netzach. The Watcher may darken a stream; Sit reopens it.

## Installation

Prerequisites: Python 3.8+, pip. Redis optional. SQLite default.

```bash
git clone https://github.com/arwyn6969/vortex.git
cd vortex
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_game.py
```

Development:

```bash
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
pytest vortex/tests/test_lattice.py vortex/tests/test_paths.py vortex/tests/test_veils.py
```

## Documentation

- [The Lattice](docs/doctrine/THE_LATTICE.md)
- [Playable layer](docs/doctrine/PLAY.md)
- [Staircase](docs/doctrine/STAIRCASE.md)
- [Next](docs/doctrine/NEXT.md)
- [Architecture](docs/architecture.md)
- [Security](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT — see [LICENSE](LICENSE).
