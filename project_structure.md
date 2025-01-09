# Project Structure and Implementation Guide

A comprehensive overview of the Vortex of Enlightenment codebase organization and development timeline.

## Directory Structure

```
vortex/
├── src/
│   ├── core/              # Core game systems
│   │   ├── __init__.py
│   │   ├── game.py        # Main game loop
│   │   ├── player.py      # Player state management
│   │   └── constants.py   # Game constants
│   │
│   ├── zones/            # Zone implementations
│   │   ├── __init__.py
│   │   ├── base_zone.py  # Abstract base class for zones
│   │   └── ponds/        # Individual pond implementations
│   │       ├── kindness.py
│   │       ├── wisdom.py
│   │       └── ...
│   │
│   ├── questionnaire/    # Player profiling system
│   │   ├── __init__.py
│   │   ├── questions.py  # Question bank
│   │   └── analyzer.py   # Response analysis
│   │
│   ├── guides/          # AI guide system
│   │   ├── __init__.py
│   │   ├── base_guide.py
│   │   └── personalities/
│   │
│   ├── mythology/       # Mythological framework
│   │   ├── __init__.py
│   │   ├── ogdoad.py    # Ogdoad implementation
│   │   └── sefirot.py   # Sefirot mappings
│   │
│   └── ui/             # User interface
│       ├── __init__.py
│       ├── ascii_art.py # ASCII art resources
│       └── terminal.py  # Terminal utilities
│
├── data/               # Game assets and data
│   ├── archetypal_db.json
│   ├── questions.json
│   └── ascii_art/
│
├── tests/             # Test suite
│   ├── test_questionnaire.py
│   ├── test_zones.py
│   └── ...
│
├── docs/              # Documentation
│   ├── style_guide.md
│   ├── api_reference.md
│   └── tutorials/
│
├── main.py           # Entry point
├── requirements.txt  # Dependencies
└── README.md        # Project overview
```

## Core Components

### Game Engine (`src/core/`)
- `game.py`: Main game loop and state management
- `player.py`: Player data and progression tracking
- `constants.py`: Game-wide configuration

### Zone System (`src/zones/`)
- `base_zone.py`: Abstract zone interface
- `ponds/`: Individual pond implementations
  - Each pond represents a Sefirot sphere
  - Contains unique challenges and narratives

### Guide System (`src/guides/`)
- `base_guide.py`: Guide behavior framework
- `personalities/`: Unique guide personalities
  - Adaptive dialogue systems
  - Challenge management

## Development Timeline

### Phase 1: Foundation (Week 1)
1. Project Setup
   - Repository initialization
   - Development environment configuration
   - Core dependencies installation

2. Core Systems
   - Game loop implementation
   - Player state management
   - Basic terminal interface

### Phase 2: Zone Development (Weeks 2-4)
1. Base Systems
   - Zone framework implementation
   - Guide system development
   - Token collection mechanics

2. Content Creation
   - Individual pond development
   - Challenge implementation
   - Narrative integration

### Phase 3: Polish (Week 5)
1. Testing
   - Comprehensive test suite
   - Performance optimization
   - Bug fixes

2. Documentation
   - API documentation
   - User guides
   - Development documentation

## Key Implementation Examples

### Game Loop (`src/core/game.py`)
```python
class Game:
    def __init__(self):
        self.player = None
        self.current_zone = None
        self.questionnaire = None
        
    def start(self):
        """Initialize and start the game."""
        self.show_intro()
        if self.get_player_consent():
            self.run_questionnaire()
            self.main_loop()
```

### Zone Implementation (`src/zones/base_zone.py`)
```python
from abc import ABC, abstractmethod

class Zone(ABC):
    """Abstract base class for all zones."""
    
    def __init__(self, name: str, guide: Guide):
        self.name = name
        self.guide = guide
        self.connected_zones = []
    
    @abstractmethod
    def enter(self, player: Player) -> None:
        """Handle player entry into zone."""
        pass
```

## Development Guidelines

1. Code Style
   - Follow PEP 8
   - Use type hints
   - Document all public interfaces

2. Testing
   - Write unit tests for new features
   - Maintain test coverage
   - Include integration tests

3. Documentation
   - Update docs with new features
   - Follow style guide
   - Include usage examples 