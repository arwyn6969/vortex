#!/usr/bin/env python3
"""
simulate_game.py

Script to automatically play the Vortex of Enlightenment game with a bot UI.
"""
import time
# CUSTOM DEBUG: disable all sleep calls for faster simulation
time.sleep = lambda _: None
import vortex.src.core.ui.terminal as terminal_module
import vortex.src.core.game as game_module
from vortex.src.core.ui.terminal import TerminalUI

# Define a Bot UI to automatically respond to prompts
class BotUI(TerminalUI):
    """A bot-based UI that provides automated responses."""
    def __init__(self):
        super().__init__()
        self.question_counter = 0
        # Simple test sequence
        self.command_sequence = [
            'look',
            'Hello Thoth, I seek wisdom about the universe',  # This should trigger LLM response
            'quit'
        ]
        self.command_counter = 0  # Track current command index

    def display_text(self, text: str):
        # Print game text and pause for readability
        print(text)
        time.sleep(0.3)

    def get_input(self, prompt: str) -> str:
        # Automatically decide on responses based on prompt content
        print(prompt, end='')
        # CUSTOM DEBUG: Log incoming prompt for analysis
        print(f"[LOG] Received prompt: '{prompt.strip()}'", flush=True)
        prompt_lower = prompt.lower()
        if 'are you ready' in prompt_lower:
            reply = 'y'
        elif 'enter your name' in prompt_lower:
            reply = 'BotUser'
        elif 'your response' in prompt_lower or 'your approach' in prompt_lower:
            # CUSTOM: Cycle through options for more varied profiling responses
            self.question_counter += 1
            # Assume up to 4 options per question; cycle through 1-4
            choice = (self.question_counter % 4) + 1
            reply = str(choice)
        elif prompt.strip().startswith('>'):
            # CUSTOM: Use predefined command sequence instead of quitting
            if self.command_counter < len(self.command_sequence):
                reply = self.command_sequence[self.command_counter]
                self.command_counter += 1
            else:
                # After exhausting commands, quit the game
                reply = 'quit'
        else:
            # Default fallback
            reply = '1'
        # CUSTOM DEBUG: Log chosen reply for traceability
        print(f"[LOG] BotUI reply: '{reply}'", flush=True)
        print(reply)
        time.sleep(0.3)
        return reply

# Override the TerminalUI used by Game to use our BotUI
terminal_module.TerminalUI = BotUI
# Also override in game module (in case it references its own import)
game_module.TerminalUI = BotUI
# CUSTOM DEBUG: override CoreEngine.start to prevent it from blocking
game_module.CoreEngine.start = lambda self: None

def main():
    # Start the game with bot-driven UI
    game = game_module.Game()
    game.start()

if __name__ == '__main__':
    main() 