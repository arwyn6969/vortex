"""
Terminal-based user interface for the game.
"""
import os
import sys
from typing import Optional

class TerminalUI:
    """Handles terminal-based user interaction."""
    
    def __init__(self):
        self.last_command: Optional[str] = None
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_intro(self):
        """Display the game introduction."""
        self.clear_screen()
        self.display_text("""
╔════════════════════════════════════════════════════════════════╗
║                   Vortex of Enlightenment                      ║
╚════════════════════════════════════════════════════════════════╝

A journey through mystical ponds of wisdom, where ancient knowledge
flows through sacred streams, and truth reveals itself to those
who seek it.

Your responses to the following questions will determine your 
path through the Vortex. Answer truthfully, for the waters of 
wisdom reflect the essence of your being.
""")
    
    def display_text(self, text: str):
        """Display text to the user."""
        print(text)
    
    def prompt(self, message: str) -> str:
        """Prompt the user for input."""
        try:
            return input(f"{message} ")
        except (KeyboardInterrupt, EOFError):
            self.display_text("\nFarewell, seeker...")
            sys.exit(0)
    
    def get_command(self) -> str:
        """Get a command from the user."""
        try:
            command = input("\nWhat would you like to do? ").strip().lower()
            self.last_command = command
            return command
        except (KeyboardInterrupt, EOFError):
            return "quit"
    
    def display_error(self, message: str):
        """Display an error message."""
        print(f"\nError: {message}", file=sys.stderr)
    
    def display_success(self, message: str):
        """Display a success message."""
        print(f"\nSuccess: {message}")
    
    def display_separator(self):
        """Display a visual separator."""
        print("\n" + "─" * 60 + "\n")
    
    def display_options(self, options: list, prompt_text: str = "Choose an option:"):
        """Display a list of options and get user selection."""
        print(f"\n{prompt_text}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                choice = int(self.prompt("\nEnter your choice (number):"))
                if 1 <= choice <= len(options):
                    return choice - 1
                print("Please enter a valid option number.")
            except ValueError:
                print("Please enter a number.") 