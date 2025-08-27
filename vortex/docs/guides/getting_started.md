# Getting Started with Vortex

Welcome to the Vortex of Enlightenment project! This guide will help you set up and start using the system.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- A Unix-like environment (Linux/MacOS) or Windows with WSL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vortex.git
   cd vortex
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install development dependencies (if contributing):
   ```bash
   pip install -r requirements-dev.txt
   ```

## Initial Setup

1. Configure your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

2. Initialize the database:
   ```bash
   python -m vortex.db.init
   ```

3. Run the initial setup:
   ```bash
   python setup.py develop
   ```

## Running the System

1. Start the main application:
   ```bash
   python run_game.py
   ```

2. Run tests (optional):
   ```bash
   ./run_tests.sh
   ```

## Core Concepts

### The Pond System
- Interactive meditation spaces
- Energy flow and balance
- Guide interactions
- Token earning opportunities

### Profile System
- Personal progress tracking
- Behavioral analysis
- Achievement system
- Customized challenges

### Token System
- Different token types
- Earning mechanisms
- Usage and benefits
- Multiplier system

## First Steps

1. Complete the initial questionnaire
2. Explore the basic pond system
3. Connect with your first guide
4. Begin basic challenges
5. Track your progress

## Advanced Features

### Guide Interaction
- Learn about different guides
- Understand their domains
- Complete guide-specific challenges
- Earn special tokens

### Challenge System
- Progressive difficulty
- Multi-guide challenges
- Special events
- Seasonal activities

### Token Management
- Token types overview
- Earning strategies
- Using tokens effectively
- Multiplier optimization

## Troubleshooting

### Common Issues
1. Database connection problems
   - Check your .env configuration
   - Ensure database service is running

2. Token system issues
   - Verify wallet connection
   - Check token balance
   - Review transaction history

3. Guide interaction problems
   - Confirm guide availability
   - Check challenge prerequisites
   - Review energy levels

### Getting Help
- Check the FAQ section
- Review error messages
- Join the community
- Contact support

## Next Steps

1. Read the [Mythology Guide](./mythology.md)
2. Review the [Architecture Documentation](../technical/architecture.md)
3. Join the community
4. Start your journey

## Resources

- [Full Documentation](../index.md)
- [API Reference](../api/index.md)
- [Community Guidelines](../community/guidelines.md)
- [Contributing Guide](../CONTRIBUTING.md) 