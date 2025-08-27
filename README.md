# VORTEX

VORTEX is a mystical journey through interconnected spiritual realms, combining ancient wisdom with modern gameplay mechanics. Players explore sacred spaces, solve challenges, and progress through symbolic pathways while collecting tokens and achievements.

## Core Features

- **Mystical Framework**:
  - Pond system with unique elemental alignments
  - Sacred streams connecting different realms
  - Integration of multiple spiritual traditions
  - Symbolic progression pathways

- **Gameplay Systems**:
  - Profile-based challenge adaptation
  - Token-based advancement
  - Achievement tracking
  - Dynamic difficulty scaling

- **Spiritual Integration**:
  - Sefirot path navigation
  - Multiple cultural traditions (Egyptian, Dogon, Mayan)
  - Sacred geometry patterns
  - Symbolic interpretation challenges

- **LLM-Powered Dialogue**:
  - Deepseek R1 integration for dynamic guide interactions
  - Personalized responses based on player profile
  - Contextually aware conversations
  - Cultural and mythological consistency

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Redis (optional, for advanced caching)
- SQLite (default database) or PostgreSQL (for production)

### Basic Installation

1. Clone the repository
```bash
git clone https://github.com/username/vortex.git
cd vortex
```

2. Create and activate a virtual environment
```bash
# On Linux/macOS
python -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the game
```bash
python run_game.py
```

### Development Installation

For development work, install additional development dependencies:

```bash
pip install -r requirements-dev.txt
pip install -e .  # Install in editable mode
```

Set up pre-commit hooks:
```bash
pre-commit install
```

### Environment Configuration

VORTEX can be configured using environment variables:

```bash
# Core app configuration
export VORTEX_APP__DEBUG=true
export VORTEX_APP__LOG_LEVEL=DEBUG

# Database configuration
export VORTEX_DATABASE__URL="sqlite:///vortex_dev.db"

# LLM configuration
export VORTEX_LLM__API_KEY="your-api-key"
```

Alternatively, create a `.env` file in the project root:

```
VORTEX_APP__DEBUG=true
VORTEX_APP__LOG_LEVEL=DEBUG
VORTEX_DATABASE__URL=sqlite:///vortex_dev.db
```

## Project Structure

```
vortex/
├── src/                  # Main source code
│   ├── core/             # Core game functionality
│   ├── guides/           # Mythological guide system
│   ├── zones/            # Location and pond system
│   ├── mythology/        # Mythological systems integration
│   └── db/               # Database models and connections
├── docs/                 # Documentation
│   ├── architecture.md   # System architecture
│   ├── api/              # API documentation
│   ├── guides/           # User guides
│   └── reference/        # Reference materials
├── tests/                # Test suite
├── examples/             # Example scripts and usage
└── scripts/              # Utility scripts
```

## Documentation

Comprehensive documentation is available in the `docs` directory:

- [Architecture Overview](docs/architecture.md) - System design and component interactions
- [Developer Guide](docs/guides/developer_guide.md) - Guide for developers
- [User Guide](docs/guides/user_guide.md) - Guide for players
- [Configuration Reference](docs/reference/configuration.md) - Configuration options

## Development

### Running Tests

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=vortex --cov-report=term-missing

# Run specific test
pytest vortex/tests/core/test_game.py
```

### Code Quality

Run linting checks:

```bash
flake8 vortex
pylint vortex
mypy vortex
```

Generate documentation:

```bash
cd docs
make html
```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Egyptian, Dogon, and Mayan mythological systems
- The Sefirot and Tree of Life concepts
- Sacred geometry principles
- Deepseek AI for LLM capabilities