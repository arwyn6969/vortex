# Project Structure and Implementation Guide

A comprehensive overview of the Vortex of Enlightenment codebase organization and current implementation status.

## Directory Structure

```
vortex/
├── src/
│   ├── core/                # Core game systems
│   │   ├── __init__.py
│   │   ├── engine.py       # Main game engine
│   │   ├── player.py       # Player state & profile
│   │   ├── constants.py    # System constants
│   │   └── progression.py  # Virtue/Vice mechanics
│   │
│   ├── zones/             # Zone implementations
│   │   ├── __init__.py
│   │   ├── base_zone.py   # Abstract zone interface
│   │   ├── stream_manager.py  # Stream connections
│   │   ├── wisdom_pond.py    # Chokhmah implementation
│   │   ├── kindness_pond.py  # Chesed implementation
│   │   ├── expression_pond.py # Tiferet implementation
│   │   ├── severity_pond.py  # Gevurah implementation
│   │   ├── understanding_pond.py # Binah implementation
│   │   └── harmony_pond.py   # Yesod implementation
│   │
│   ├── profiling/         # Behavioral profiling
│   │   ├── __init__.py
│   │   ├── questionnaire.py  # Voight-Kampff system
│   │   ├── analyzer.py      # Response analysis
│   │   └── dimensions.py    # Behavioral dimensions
│   │
│   ├── guides/           # Guide system
│   │   ├── __init__.py
│   │   ├── base_guide.py  # Guide framework
│   │   ├── personality.py # Personality engine
│   │   └── archetypes/    # Cultural variants
│   │       ├── egyptian/
│   │       ├── mayan/
│   │       └── dogon/
│   │
│   ├── mythology/        # Mythological framework
│   │   ├── __init__.py
│   │   ├── sefirot.py    # Kabbalistic system
│   │   ├── ogdoad.py     # Egyptian system
│   │   ├── dogon.py      # Dogon cosmology
│   │   ├── mayan.py      # Mayan calendar
│   │   └── integration.py # Cross-cultural mapping
│   │
│   └── ui/              # User interface
│       ├── __init__.py
│       ├── terminal.py   # Terminal interface
│       ├── display.py    # Visual components
│       └── themes.py     # Visual themes
│
├── data/                # Game content
│   ├── profiles/        # Profile templates
│   ├── mythology/       # Mythological data
│   │   ├── sefirot/
│   │   ├── ogdoad/
│   │   ├── dogon/
│   │   └── mayan/
│   └── content/         # Game content
│       ├── challenges/
│       ├── dialogs/
│       └── scenarios/
│
├── tests/              # Test suite
│   ├── unit/
│   │   ├── test_profiling.py
│   │   ├── test_zones.py
│   │   └── test_mythology.py
│   └── integration/
│       ├── test_progression.py
│       └── test_cross_cultural.py
│
├── docs/               # Documentation
│   ├── integration.md  # System integration
│   ├── mechanics.md    # Game mechanics
│   └── mythology/      # Cultural references
│       ├── sefirot.md
│       ├── ogdoad.md
│       ├── dogon.md
│       └── mayan.md
│
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md         # Project overview
```

## Core Components

### Game Engine (`src/core/`)
- Complete implementation of core game loop
- Player state management with profile integration
- Virtue/Vice progression system
- Cross-cultural achievement tracking

### Zone System (`src/zones/`)
- All pond implementations complete
- Stream management system operational
- Dynamic content adaptation based on profiles
- Cross-cultural challenge integration

### Profiling System (`src/profiling/`)
- Enhanced Voight-Kampff questionnaire
- Multi-dimensional behavioral analysis
- Real-time profile adaptation
- Content personalization engine

### Guide System (`src/guides/`)
- Adaptive personality framework
- Cultural archetype integration
- Dynamic teaching methods
- Personalized interaction patterns

### Mythology Framework (`src/mythology/`)
- Complete Sefirot-Ogdoad mapping
- Dogon cosmological integration
- Mayan calendar mechanics
- Cross-cultural correspondence system

## Implementation Status

### Completed Features
- Core game engine
- All pond implementations
- Behavioral profiling system
- Guide personality framework
- Basic mythological integration
- Terminal UI system

### In Progress
- Advanced content adaptation
- Cross-cultural achievement system
- Integration testing
- Documentation updates

### Planned Features
- Enhanced guide interactions
- Advanced symbolic mechanics
- Extended mythological content
- Additional cultural integrations

## Development Guidelines

### Code Standards
- Type hints required
- Docstring documentation
- PEP 8 compliance
- Unit test coverage

### Documentation
- Keep mythology references updated
- Document cross-cultural connections
- Maintain technical specifications
- Update integration guides

### Testing
- Unit tests for new features
- Integration tests for systems
- Cultural accuracy validation
- Performance benchmarking 