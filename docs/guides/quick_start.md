# VORTEX Quick Start Guide

This guide will help you quickly set up and begin your journey through the Vortex of Enlightenment.

## Installation

### 1. Basic Setup

1. **Install Python 3.8+** if you don't already have it
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Clone or download the VORTEX repository**
   ```bash
   git clone https://github.com/username/vortex.git
   cd vortex
   ```

3. **Create a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game**
   ```bash
   python run_game.py
   ```

### 2. Configuration (Optional)

For a personalized experience, you can configure VORTEX through environment variables:

```bash
# Enable debug mode
export VORTEX_APP__DEBUG=true

# Change text speed (lower is faster)
export VORTEX_UI__TEXT_SPEED=0.005

# Set default guide
export VORTEX_GAME__DEFAULT_GUIDE=isis
```

## Your First Journey

### Understanding the Interface

When you start VORTEX, you'll see a welcome message and be prompted to begin your journey. The interface is text-based and intuitive:

```
╔══════════════════════════════════════════════╗
║        The Vortex of Enlightenment           ║
╚══════════════════════════════════════════════╝

Welcome, seeker of wisdom. You stand at the threshold 
of a journey through mystical waters and ancient knowledge.

> (Your input goes here)
```

### Initial Steps

1. **Create Your Profile**
   - Enter your name when prompted
   - Complete the VoightKampff questionnaire honestly
   - Your responses will determine your starting guide and experience

2. **Meet Your Guide**
   - Based on your profile, you'll be assigned a mythological guide
   - Each guide has unique characteristics and wisdom to share
   - Your guide will help navigate your journey

3. **Explore the Central Hub**
   - Your journey begins in the Central Hub
   - Explore available locations by typing "look" or "explore"
   - Move to different locations using "go [location name]"

### Basic Commands

Here are some essential commands to navigate the VORTEX:

- `look` or `examine` - Observe your current surroundings
- `go [location]` - Travel to a connected location
- `talk` or `speak` - Engage with your guide
- `help` - Display available commands
- `inventory` or `tokens` - View your collected tokens
- `achievements` - View your achievements
- `save` - Save your progress
- `exit` or `quit` - Exit the game (automatically saves)

### Conversation with Guides

When interacting with your guide, you can:

- Ask questions about mythology and symbolism
- Seek guidance on your journey
- Discuss philosophical concepts
- Request explanations about locations or tokens

Example conversation:
```
> talk
What would you like to discuss with Thoth?

> What is the significance of the Wisdom Pond?

Thoth: The Wisdom Pond represents the collective knowledge of all 
who have journeyed before you. Its waters reflect not just what is seen, 
but what lies beneath perception. By immersing yourself in its depths, 
you gain insights that transcend ordinary understanding.
```

## Understanding Tokens and Achievements

### Tokens

As you explore and complete challenges, you'll collect tokens that represent spiritual insights and progress:

- **Wisdom Tokens** - Gained through solving puzzles and answering questions
- **Harmony Tokens** - Earned by balancing opposing forces
- **Insight Tokens** - Discovered through deep reflection and observation
- **Transcendence Tokens** - Rare tokens from completing significant milestones

Tokens can be used to unlock new areas, gain special abilities, or enhance your connection with guides.

### Achievements

VORTEX tracks your progress through achievements, including:

- **First Steps** - Begin your journey
- **Explorer** - Visit multiple locations
- **Philosopher** - Engage in deep conversations with guides
- **Enlightened** - Reach significant milestones in understanding

View your achievements at any time with the `achievements` command.

## Progressing Through the Vortex

### The Pond System

The VORTEX is structured around mystical ponds, each with unique properties:

- **Wisdom Pond** - Centers on knowledge and intellectual growth
- **Reflection Pool** - Focuses on self-discovery and introspection
- **Sacred Grove** - Emphasizes connection with nature and life forces

### Advancing Your Journey

To progress through VORTEX:

1. Explore all available locations
2. Complete challenges appropriate to your profile
3. Collect tokens to unlock new areas
4. Engage with your guide to gain deeper insights
5. Reflect on your experiences to unlock hidden meanings

## Tips for New Travelers

- Take your time and absorb the experience
- There are no wrong answers in the VORTEX, only different paths
- Your guide is your most valuable resource—engage with them often
- Return to previously visited locations as you gain new insights
- Save your progress regularly
- The journey itself is more important than the destination

## Troubleshooting

If you encounter issues:

- **Game won't start**: Ensure Python 3.8+ is installed and all requirements are installed
- **Text appears too quickly/slowly**: Adjust the text speed in configuration
- **Guide doesn't respond**: Try rephrasing your question or use simpler language
- **Can't navigate to a location**: Check that you've spelled the location correctly and it's connected to your current location

For more detailed help, refer to the [full documentation](../reference/troubleshooting.md) or reach out to the community.

Welcome, traveler. Your journey awaits. 