"""
Dialogue management functionality for the VORTEX system.

This module handles dialogue generation, context tracking, and response processing.
It extracts dialogue-specific functionality to improve separation of concerns
and maintainability.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ..core.ui.terminal import TerminalUI
from ..guides.guide_factory import GuideFactory
from ..core.user_profiling.profile_matrix import ProfileMatrix

@dataclass
class DialogueContext:
    """Represents the context of a dialogue interaction."""
    guide_name: str
    player_name: str
    current_location: str
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    last_interaction: Optional[datetime] = None
    topic_focus: Optional[str] = None

class DialogueManager:
    """
    Manages dialogue-related functionality including generation and processing.
    
    This class consolidates dialogue management logic to improve modularity
    and provide better conversation state tracking.
    """
    
    def __init__(self, ui: TerminalUI, guide_factory: GuideFactory, profile_matrix: ProfileMatrix):
        """
        Initialize the dialogue manager.
        
        Args:
            ui: User interface for dialogue display
            guide_factory: Factory for creating and managing guides
            profile_matrix: Profile matrix for personality-based responses
        """
        self.ui = ui
        self.guide_factory = guide_factory
        self.profile_matrix = profile_matrix
        self.current_context: Optional[DialogueContext] = None
        
        # Maximum conversation history to maintain
        self.max_history_length = 10
        
    def initialize_dialogue(self, guide_name: str, player_name: str, location: str):
        """
        Initialize a new dialogue context.
        
        Args:
            guide_name: Name of the active guide
            player_name: Name of the player
            location: Current location name
        """
        self.current_context = DialogueContext(
            guide_name=guide_name,
            player_name=player_name,
            current_location=location,
            last_interaction=datetime.now()
        )
        
    def update_location(self, new_location: str):
        """
        Update the current location in dialogue context.
        
        Args:
            new_location: Name of the new location
        """
        if self.current_context:
            self.current_context.current_location = new_location
            
    def add_to_history(self, speaker: str, message: str):
        """
        Add a message to the conversation history.
        
        Args:
            speaker: Who said the message (player or guide name)
            message: The content of the message
        """
        if not self.current_context:
            return
            
        self.current_context.conversation_history.append({
            "speaker": speaker,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Maintain history length
        if len(self.current_context.conversation_history) > self.max_history_length:
            self.current_context.conversation_history.pop(0)
            
    def get_guide_response(self, player_input: str) -> Optional[str]:
        """
        Generate a guide's response to player input.
        
        Args:
            player_input: The player's message or command
            
        Returns:
            The guide's response or None if no response is appropriate
        """
        if not self.current_context:
            return None
            
        # Add player input to history
        self.add_to_history(self.current_context.player_name, player_input)
        
        # Get the appropriate guide
        guide = self.guide_factory.create_guide(self.current_context.guide_name)
        if not guide:
            return None
            
        # Get player profile for personalized responses
        profile = self.profile_matrix.get_profile(self.current_context.player_name)
        
        # Generate response based on context
        response = guide.generate_response(
            player_input,
            profile.dimensions if profile else {},
            {
                "conversation_history": self.current_context.conversation_history,
                "current_location": self.current_context.current_location
            }
        )
        
        if response:
            # Add guide's response to history
            self.add_to_history(self.current_context.guide_name, response)
            self.current_context.last_interaction = datetime.now()
            
        return response
        
    def get_conversation_summary(self) -> List[Dict[str, str]]:
        """
        Get a summary of the current conversation.
        
        Returns:
            List of conversation entries
        """
        return self.current_context.conversation_history if self.current_context else []
        
    def clear_context(self):
        """Clear the current dialogue context."""
        self.current_context = None
        
    def set_topic_focus(self, topic: Optional[str]):
        """
        Set the current topic focus for the conversation.
        
        Args:
            topic: The topic to focus on, or None to clear focus
        """
        if self.current_context:
            self.current_context.topic_focus = topic
            
    def get_topic_focus(self) -> Optional[str]:
        """
        Get the current topic focus.
        
        Returns:
            The current topic focus or None if not set
        """
        return self.current_context.topic_focus if self.current_context else None 