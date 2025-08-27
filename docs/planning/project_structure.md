# Project Structure and Implementation Guide

A comprehensive overview of the Vortex of Enlightenment codebase organization and current implementation status.

## Directory Structure

```
vortex/
├── src/
│   ├── core/                # Core game systems
│   │   ├── __init__.py
│   │   ├── engine.py       # Main game engine
│   │   ├── adaptive_game.py # Adaptive gameplay system
│   │   ├── constants.py    # System constants
│   │   ├── progression.py  # Virtue/Vice mechanics
│   │   ├── llm/              # LLM integration
│   │   │   ├── __init__.py
│   │   │   ├── deepseek_client.py  # Deepseek-R1 70B client
│   │   │   └── config.py     # LLM configuration
│   │   └── user_profiling/ # User profiling systems
│   │       ├── __init__.py
│   │       ├── behavioral_analysis.py  # Behavioral tracking
│   │       └── questionnaire.py       # Initial profiling
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
│   ├── guides/           # Guide system
│   │   ├── __init__.py
│   │   ├── base_guide.py  # Guide framework
│   │   ├── llm_dialogue.py   # LLM dialogue system
│   │   ├── personality.py # Personality engine
│   │   ├── maat.py       # Egyptian wisdom guide
│   │   ├── isis.py       # Egyptian nurture guide
│   │   ├── horus.py      # Egyptian protection guide
│   │   └── odin.py       # Norse wisdom guide
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
│   │
│   └── content/         # Game content
│       ├── challenges/
│       ├── dialogs/
│       └── scenarios/
│
├── tests/              # Test suite
│   ├── core/           # Core system tests
│   │   ├── test_engine.py
│   │   ├── test_adaptive_game.py
│   │   ├── test_progression.py
│   │   └── user_profiling/
│   │       ├── test_behavioral_analysis.py
│   │       └── test_questionnaire.py
│   ├── guides/         # Guide system tests
│   │   ├── test_base_guide.py
│   │   ├── test_maat.py
│   │   ├── test_isis.py
│   │   ├── test_horus.py
│   │   └── test_odin.py
│   ├── zones/          # Zone implementation tests
│   │   ├── test_base_zone.py
│   │   ├── test_stream_manager.py
│   │   └── test_ponds.py
│   └── integration/    # Cross-system integration tests
│       ├── test_behavioral_integration.py
│       ├── test_guide_profiling.py
│       └── test_zone_progression.py
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
- Adaptive gameplay system with real-time adjustments
- Player state management with profile integration
- Virtue/Vice progression system
- Cross-cultural achievement tracking
- Behavioral analysis integration

### User Profiling (`src/core/user_profiling/`)
- Behavioral analysis system
  - Real-time interaction tracking
  - Pattern recognition
  - Temporal analysis
- Initial questionnaire framework
- Multi-dimensional behavioral tracking
- Guide interaction optimization
- Adaptive difficulty scaling

### Zone System (`src/zones/`)
- All pond implementations complete
- Stream management system operational
- Dynamic content adaptation based on profiles
- Cross-cultural challenge integration

### LLM Integration (`src/core/llm/`)
- Deepseek-R1 70B model integration
- Error handling and retries
- Memory-efficient processing
- Response validation
- Conversation management

### Guide System (`src/guides/`)
- LLM-powered dialogue system
- Profile-based adaptation
- Cultural context integration
- Conversation memory
- Response validation
- Error recovery

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
- Unit tests for all components
- Mock LLM integration
- Integration testing
- Performance benchmarks
- Cultural validation

### Cultural Accuracy
- Keep mythology references updated
- Document cross-cultural connections
- Maintain technical specifications
- Update integration guides

### Testing Framework
1. **Core Testing** (`tests/core/`)
   - Unit tests for engine components
   - Behavioral analysis validation
   - Profile management tests
   - LLM integration tests
   - Performance benchmarks

2. **Guide Testing** (`tests/guides/`)
   - Base guide functionality
   - LLM dialogue system
   - Personality adaptation
   - Cultural integration
   - Error handling
   - Memory management

3. **Integration Testing** (`tests/integration/`)
   - Guide-Zone interactions
   - Profile adaptation flows
   - Cultural context handling
   - Memory persistence
   - Error recovery systems
   - System stability
   - Cross-cultural wisdom
   - Virtue progression
   - Emotional state handling
   - Challenge completion
   - Multi-component scenarios

4. **Test Coverage**
   - Core systems: 90%
   - Guide system: 85%
   - Integration tests: 75%
   - Cultural validation: 70%

### Development Guidelines

#### Testing Standards
- All new features require tests
- Integration tests for component interactions
- Cultural sensitivity validation
- Performance benchmarking
- Error recovery verification 