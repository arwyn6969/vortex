"""
Terminal-based user interface for the game.
"""
import os
import sys
from typing import Optional, Callable, List
from datetime import datetime

class TerminalUI:
    """Handles terminal-based user interaction."""
    
    def __init__(self):
        self.last_command: Optional[str] = None
        self.keystroke_callback: Optional[Callable[[int], None]] = None
        self._keystroke_buffer = 0
        self._last_keystroke_time = datetime.now()
        self._keystroke_batch_size = 10  # Send keystrokes in batches
    
    def set_keystroke_callback(self, callback: Callable[[int], None]):
        """Set callback for keystroke tracking."""
        self.keystroke_callback = callback
    
    def _handle_keystrokes(self, text: str):
        """Handle keystroke tracking."""
        if not self.keystroke_callback:
            return
            
        # Count keystrokes (excluding backspaces)
        keystroke_count = len(text)
        self._keystroke_buffer += keystroke_count
        
        # If we've reached the batch size, send the keystrokes
        if self._keystroke_buffer >= self._keystroke_batch_size:
            self.keystroke_callback(self._keystroke_buffer)
            self._keystroke_buffer = 0
            self._last_keystroke_time = datetime.now()
    
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
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get input from the user with the specified prompt."""
        try:
            response = input(prompt)
            self._handle_keystrokes(response)
            return response.strip()
        except (KeyboardInterrupt, EOFError):
            return "quit"
    
    def process_input(self, user_input: str) -> Optional[str]:
        """Process user input and return any response."""
        if not user_input:
            return None
            
        # Store last command
        self.last_command = user_input.lower()
        
        # Return None to indicate no specific response needed
        return None
    
    def display_error(self, message: str):
        """Display an error message."""
        print(f"\nError: {message}", file=sys.stderr)
    
    def display_success(self, message: str):
        """Display a success message."""
        print(f"\nSuccess: {message}")
    
    def display_separator(self):
        """Display a visual separator."""
        print("\n" + "─" * 60 + "\n")
    
    def display_options(self, options: List[str], prompt_text: str = "Choose an option:"):
        """Display a list of options and get user selection."""
        print(f"\n{prompt_text}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                choice = int(self.get_input("\nEnter your choice (number): "))
                if 1 <= choice <= len(options):
                    return choice - 1
                print("Please enter a valid option number.")
            except ValueError:
                print("Please enter a number.")
                
    def update_display(self, text: str):
        """Update the display with new text."""
        self.display_text(text)
        
    def show_status(self, status: dict):
        """Display current game status."""
        self.display_separator()
        for key, value in status.items():
            print(f"{key}: {value}")
        self.display_separator() 