# VORTEX Architecture

## System Overview

VORTEX is a text-based adventure game with a focus on spiritual and mythological themes. The system combines adaptive gameplay, profile-based user interactions, and a rich mythological framework to create a personalized journey for each player.

```
┌─────────────────────────┐
│       Game Engine       │
├─────────────────────────┤
│    Event Bus System     │
├─────┬───────────┬───────┤
│User │  Guide    │Location│
│Prof.│  System   │ System │
├─────┼───────────┼───────┤
│Token│Achievement│Challenge│
│Sys. │  System   │ System  │
└─────┴───────────┴────────┘
```

## Core Components

### Game Engine

The Game Engine is the central coordinator of the VORTEX experience, orchestrating all other components and managing the overall game state.

**Key Responsibilities:**
- Game initialization and shutdown
- Player creation and management
- Turn management and game flow
- Component coordination via the Event Bus
- Save/load functionality

**Key Files:**
- `vortex/src/core/game.py` - Main game coordination class
- `vortex/src/core/engine.py` - Core engine functionality
- `vortex/src/core/config.py` - Configuration management

### Event Bus System

The Event Bus facilitates decoupled communication between components through a publish-subscribe pattern.

**Key Responsibilities:**
- Event registration and unregistration
- Event dispatch to subscribers
- Asynchronous communication

**Key Files:**
- `vortex/src/core/communication/event_bus.py` - Event bus implementation

### User Profiling System

The User Profiling System analyzes player responses and behavior to build a psychological profile that influences gameplay.

**Key Responsibilities:**
- Initial questionnaire administration
- Profile creation and updates
- Profile storage and retrieval
- Profile dimension analysis

**Key Files:**
- `vortex/src/core/user_profiling/questionnaire.py` - VoightKampff questionnaire
- `vortex/src/core/user_profiling/profile_matrix.py` - Profile storage and analysis

### Guide System

The Guide System provides mythological guides that interact with the player based on their profile, offering guidance and narratives tailored to their preferences.

**Key Responsibilities:**
- Guide selection based on user profile
- Dialogue generation and management
- LLM-powered conversations
- Cultural and mythological consistency

**Key Files:**
- `vortex/src/guides/guide_factory.py` - Guide creation and selection
- `vortex/src/guides/base_guide.py` - Guide base functionality
- `vortex/src/guides/llm_dialogue.py` - LLM-powered dialogue system

### Location System

The Location System manages the game's spatial structure, including ponds, pathways, and connectivity between realms.

**Key Responsibilities:**
- Location management and descriptions
- Navigation between locations
- Location-specific interactions
- Discovery tracking

**Key Files:**
- `vortex/src/zones/location_manager.py` - Location management
- `vortex/src/zones/pond_system.py` - Pond implementation

### Token System

The Token System manages the in-game currency and progression mechanics.

**Key Responsibilities:**
- Token collection and spending
- Token-based unlocks
- Token analytics
- Progression tracking

**Key Files:**
- `vortex/src/core/finance/token_system.py` - Token implementation
- `vortex/src/core/crypto/bitcoin_integration.py` - Bitcoin token integration

### Achievement System

The Achievement System tracks player accomplishments and provides rewards for specific milestones.

**Key Responsibilities:**
- Achievement tracking and unlocking
- Notification of achievements
- Achievement persistence
- Achievement-based rewards

**Key Files:**
- `vortex/src/core/achievements.py` - Achievement functionality

### Challenge System

The Challenge System provides puzzles, questions, and tasks adaptive to the player's profile.

**Key Responsibilities:**
- Challenge generation and presentation
- Challenge difficulty adaptation
- Response validation
- Reward allocation

**Key Files:**
- `vortex/src/core/adaptive_game.py` - Adaptive gameplay mechanics

## Data Flow

### Player Interaction Flow

```
┌──────────┐    ┌───────────┐    ┌──────────┐
│  Player  │───►│ Terminal  │───►│  Game    │
│  Input   │    │    UI     │    │  Engine  │
└──────────┘    └───────────┘    └────┬─────┘
                                      │
                                      ▼
┌──────────┐    ┌───────────┐    ┌──────────┐
│  Guide   │◄───│   Event   │◄───│ Command  │
│ Response │    │    Bus    │    │ Processor│
└──────────┘    └───────────┘    └──────────┘
```

1. Player enters text input through the Terminal UI
2. Input is passed to the Game Engine
3. Game Engine processes the command through Command Processor
4. Relevant events are published to the Event Bus
5. Appropriate guide responds based on player input and profile

### Profile Creation Flow

```
┌──────────┐    ┌───────────┐    ┌──────────┐
│ Initial  │───►│ Voight-   │───►│ Profile  │
│  Setup   │    │ Kampff    │    │  Matrix  │
└──────────┘    └───────────┘    └────┬─────┘
                                      │
                                      ▼
┌──────────┐    ┌───────────┐    ┌──────────┐
│  Guide   │◄───│   Guide   │◄───│ Profile  │
│Selection │    │  Factory  │    │ Analysis │
└──────────┘    └───────────┘    └──────────┘
```

1. Player begins initial setup
2. VoightKampff questionnaire assesses player attributes
3. Profile Matrix creates and stores player profile
4. Profile Analysis determines key player characteristics
5. Guide Factory selects appropriate guide based on profile
6. Guide is assigned to the player

### LLM Dialogue Generation Flow

```
┌──────────┐    ┌───────────┐    ┌──────────┐
│  Player  │───►│ Dialogue  │───►│  Prompt  │
│  Input   │    │  Context  │    │Generation │
└──────────┘    └───────────┘    └────┬─────┘
                                      │
                                      ▼
┌──────────┐    ┌───────────┐    ┌──────────┐
│ Response │◄───│ Response  │◄───│ Deepseek │
│ to Player│    │ Validation│    │   LLM    │
└──────────┘    └───────────┘    └──────────┘
```

1. Player input is combined with dialogue context
2. Prompt is generated based on guide personality and user profile
3. Prompt is sent to Deepseek-R1 LLM
4. Generated response is validated for quality and safety
5. Valid response is presented to the player

## Configuration System

The VORTEX configuration system provides a centralized way to manage application settings with the following features:

- Default configuration values for all components
- Environment variable overrides using VORTEX_CATEGORY__NAME format
- Configuration file support in JSON format
- Type conversion and validation
- Hierarchical configuration structure

Example usage:
```python
from vortex.src.core.config import config

# Get configuration values
db_url = config.get("database.url")
debug_mode = config.get("app.debug", default=False)

# Check if a configuration exists
if config.has("llm.api_key"):
    # Use the API key
    api_key = config.get("llm.api_key")
```

## Persistence Layer

VORTEX uses multiple persistence mechanisms:

1. **File-based Storage**
   - Save files for game state
   - Configuration files
   - Asset storage
   
2. **Database Storage (SQLAlchemy)**
   - User profiles
   - Achievement records
   - Historical data
   
3. **Redis Cache**
   - Session data
   - Temporary state
   - Performance-critical caching

## Testing Architecture

The VORTEX testing infrastructure includes:

1. **Unit Tests**
   - Component-level testing with pytest
   - Mocking for external dependencies
   
2. **Integration Tests**
   - Cross-component functionality testing
   - Event system validation
   
3. **System Tests**
   - End-to-end gameplay scenarios
   - Performance benchmarking

## Future Architecture Extensions

### Web Interface

A planned web interface will extend the system with:

- RESTful API for game interactions
- WebSocket for real-time updates
- Web-based UI for improved accessibility

### Enhanced LLM Integration

Future LLM improvements include:

- Fine-tuned models for specific cultural contexts
- Multimodal interactions with image generation
- Memory optimization for deeper conversation history

### Multiplayer Capabilities

A future multiplayer system will add:

- Shared mythological realms
- Guide-mediated player interactions
- Collaborative challenges and shared achievements 