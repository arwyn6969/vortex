#!/usr/bin/env python3
"""
Run script for the Vortex of Enlightenment game.
"""
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from vortex.src.core.game import Game
except ImportError as e:
    print(f"Error importing game module: {e}")
    print("Make sure you have installed all required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main entry point."""
    try:
        # Create and start the game
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\nThank you for exploring the Vortex of Enlightenment!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The game has been terminated.")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 