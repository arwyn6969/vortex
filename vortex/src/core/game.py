"""
Main game loop and state management.
"""
from typing import Optional
from .player import Player
from ..ui.terminal import TerminalUI

class Game:
    def __init__(self):
        self.player: Optional[Player] = None
        self.current_zone = None
        self.questionnaire = None
        self.ui = TerminalUI()
        
    def start(self):
        """Initialize and start the game."""
        self.ui.show_intro()
        if self.get_player_consent():
            self.create_player()
            self.run_questionnaire()
            self.main_loop()
            
    def get_player_consent(self) -> bool:
        """Get player's consent to start the game."""
        response = self.ui.prompt("Do you want to play a game? (Y/N)")
        return response.lower() in ['y', 'yes']
    
    def create_player(self):
        """Create a new player instance."""
        name = self.ui.prompt("Enter your name, traveler:")
        self.player = Player(name)
    
    def run_questionnaire(self):
        """Run the initial questionnaire."""
        # TODO: Implement questionnaire logic
        pass
    
    def main_loop(self):
        """Main game loop."""
        while True:
            self.process_input()
            self.update_state()
            self.render()
            
    def process_input(self):
        """Process player input."""
        command = self.ui.get_command()
        if command == "quit":
            self.quit_game()
        self.current_zone.process_action(command)
    
    def update_state(self):
        """Update game state."""
        pass
    
    def render(self):
        """Render current game state."""
        self.ui.clear_screen()
        self.current_zone.render(self.ui)
    
    def quit_game(self):
        """Clean up and exit the game."""
        self.ui.show_exit_message()
        exit(0) 