"""Main entry point for the Vortex of Enlightenment game."""

from vortex.src.core.game import Game

def main():
    """Main entry point for the game."""
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\nThank you for playing Vortex of Enlightenment!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("The game has been terminated.")

if __name__ == "__main__":
    main() 