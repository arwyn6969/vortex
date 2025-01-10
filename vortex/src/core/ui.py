"""Terminal-based user interface for the game."""

import sys
from typing import Optional, Callable

class Command:
    """Represents a game command with its handler and help text."""
    def __init__(self, handler: Callable, help_text: str):
        self.handler = handler
        self.help_text = help_text

class TerminalUI:
    """Handles terminal-based user interaction."""
    
    def __init__(self):
        """Initialize the terminal UI."""
        self.commands = {}
        self._register_commands()
    
    def _register_commands(self):
        """Register all available commands."""
        self.commands = {
            "help": Command(self._handle_help, "Show available commands"),
            "quit": Command(self._handle_quit, "Exit the game"),
            "map": Command(self._handle_map, "Show current location and available paths"),
            "enter": Command(self._handle_enter, "Enter a specific pond (usage: enter <pond_name>)"),
        }
    
    def _handle_help(self, args: Optional[list] = None) -> str:
        """Handle the help command."""
        help_text = "\nAvailable Commands:\n"
        for cmd_name, cmd in self.commands.items():
            help_text += f"  {cmd_name:10} - {cmd.help_text}\n"
        return help_text
    
    def _handle_quit(self, args: Optional[list] = None) -> str:
        """Handle the quit command."""
        sys.exit(0)
    
    def _handle_map(self, args: Optional[list] = None) -> str:
        """Handle the map command."""
        # TODO: Implement actual map display
        return "You are in the Central Hub\nAvailable paths:\n- Wisdom Pond (North)\n- Kindness Pond (East)"
    
    def _handle_enter(self, args: Optional[list]) -> str:
        """Handle the enter command."""
        if not args:
            return "Please specify a pond to enter (usage: enter <pond_name>)"
        pond_name = args[0].lower()
        # TODO: Implement actual pond entry logic
        return f"Entering {pond_name.title()} Pond..."
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return the result."""
        if not user_input.strip():
            return ""
        
        parts = user_input.lower().split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else None
        
        if command not in self.commands:
            return f"Unknown command: {command}. Type 'help' for available commands."
        
        try:
            return self.commands[command].handler(args)
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def display(self, message: str):
        """Display a message to the user."""
        print(message)
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get input from the user."""
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            return "quit" 