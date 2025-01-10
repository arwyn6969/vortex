"""
UI interface module that provides a unified interface for both terminal and GUI modes.
"""
from typing import Optional, List, Dict, Union
from enum import Enum
from .terminal import TerminalUI
from .gui import VortexGUI
from .response_generator import ResponseGenerator
from ..user_profiling.profile_matrix import ProfileMatrix

class UIMode(Enum):
    """Enum for UI modes."""
    TERMINAL = "terminal"
    GUI = "gui"

class VortexInterface:
    """Unified interface for Vortex UI implementations."""
    
    def __init__(
        self,
        mode: Union[UIMode, str] = UIMode.GUI,
        profile_matrix: Optional[ProfileMatrix] = None
    ):
        """Initialize the UI interface with specified mode."""
        if isinstance(mode, str):
            mode = UIMode(mode.lower())
        
        self.mode = mode
        self.profile_matrix = profile_matrix or ProfileMatrix()
        self.response_generator = ResponseGenerator(self.profile_matrix)
        self._ui = self._create_ui()
        
        # Track interaction history for context detection
        self.recent_interactions: List[str] = []
        self.max_interaction_history = 20
        self.current_location: Optional[str] = None
        
        if self.mode == UIMode.GUI:
            self._setup_gui_callbacks()
    
    def _create_ui(self) -> Union[TerminalUI, VortexGUI]:
        """Create the appropriate UI implementation."""
        if self.mode == UIMode.TERMINAL:
            return TerminalUI()
        return VortexGUI()
    
    def _setup_gui_callbacks(self):
        """Set up callbacks for GUI mode."""
        if isinstance(self._ui, VortexGUI):
            self._ui.set_message_callback(self._handle_gui_message)
            self._ui.set_button_callback(self._handle_gui_button)
    
    def _handle_gui_message(self, message: str):
        """Handle messages from GUI."""
        # Add to interaction history
        self.recent_interactions.append(message)
        if len(self.recent_interactions) > self.max_interaction_history:
            self.recent_interactions.pop(0)
        
        # Process the message
        response = self._ui.process_input(message)
        if response:
            self.display_message(response)
        
        # Update quick responses based on new context
        self._update_quick_responses()
    
    def _handle_gui_button(self, button_text: str):
        """Handle quick response button clicks."""
        # Add to interaction history
        self.recent_interactions.append(button_text)
        if len(self.recent_interactions) > self.max_interaction_history:
            self.recent_interactions.pop(0)
        
        # Process the button click
        response = self._ui.process_input(button_text)
        if response:
            self.display_message(response)
        
        # Update quick responses based on new context
        self._update_quick_responses()
    
    def _update_quick_responses(self):
        """Update quick response buttons based on current context."""
        if self.mode != UIMode.GUI:
            return
            
        # Determine current context
        context = self.response_generator.get_response_context(
            self.recent_interactions,
            self.current_location
        )
        
        # Generate new responses
        responses = self.response_generator.generate_responses(
            "current_user",  # TODO: Add proper user ID handling
            context
        )
        
        # Update the UI
        self.update_quick_responses(responses)
    
    def start(self):
        """Start the UI."""
        if self.mode == UIMode.GUI:
            self._ui.start()
    
    def stop(self):
        """Stop the UI."""
        if self.mode == UIMode.GUI:
            self._ui.stop()
    
    def display_message(self, message: str, message_type: str = "system"):
        """Display a message to the user."""
        if self.mode == UIMode.TERMINAL:
            self._ui.display_text(message)
        else:
            self._ui.display_message(message, message_type)
    
    def update_quick_responses(self, responses: List[str]):
        """Update quick response options."""
        if self.mode == UIMode.GUI:
            self._ui.update_quick_responses(responses)
    
    def update_stats(self, stats: Dict[str, str]):
        """Update displayed statistics."""
        if self.mode == UIMode.GUI:
            self._ui._update_stats(stats)
    
    def clear_screen(self):
        """Clear the display area."""
        if self.mode == UIMode.TERMINAL:
            self._ui.clear_screen()
    
    def show_intro(self):
        """Display the introduction screen."""
        if self.mode == UIMode.TERMINAL:
            self._ui.show_intro()
        else:
            intro_text = """
            Welcome to the Vortex of Enlightenment
            
            A journey through mystical ponds of wisdom, where ancient knowledge
            flows through sacred streams, and truth reveals itself to those
            who seek it.
            
            Your responses will determine your path through the Vortex.
            Answer truthfully, for the waters of wisdom reflect the essence
            of your being.
            """
            self.display_message(intro_text)
            
            # Initialize quick responses for the introduction
            self._update_quick_responses()
    
    def get_input(self, prompt: str = "> ") -> str:
        """Get input from the user."""
        if self.mode == UIMode.TERMINAL:
            return self._ui.get_input(prompt)
        return ""  # GUI handles input through callbacks
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return the result."""
        return self._ui.process_input(user_input)
    
    def set_location(self, location: str):
        """Set the current location to influence response context."""
        self.current_location = location
        self._update_quick_responses() 