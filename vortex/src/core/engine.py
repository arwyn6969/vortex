"""Core game engine that manages the main game components and lifecycle."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class GameState:
    """Represents the current state of the game."""
    current_location: str = "Central Hub"
    is_running: bool = True

class EventBus:
    """Handles event dispatching and subscription."""
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def dispatch(self, event_type: str, data: Optional[dict] = None):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

class CoreEngine:
    """Main game engine that coordinates all game systems."""
    
    def __init__(self):
        """Initialize the core game components."""
        self.state = GameState()
        self.event_bus = EventBus()
        
    def start(self):
        """Start the game engine."""
        self.state.is_running = True
        self._initialize_systems()
        self._main_loop()
    
    def stop(self):
        """Stop the game engine."""
        self.state.is_running = False
    
    def _initialize_systems(self):
        """Initialize all required game systems."""
        # TODO: Initialize other systems like profile tracker, state manager, etc.
        self.event_bus.dispatch("game_init")
    
    def _main_loop(self):
        """Main game loop."""
        self.event_bus.dispatch("game_start")
        
        while self.state.is_running:
            # TODO: Handle input and update game state
            pass
        
        self.event_bus.dispatch("game_end")
    
    def get_current_location(self) -> str:
        """Get the player's current location."""
        return self.state.current_location
    
    def set_current_location(self, location: str):
        """Set the player's current location."""
        self.state.current_location = location
        self.event_bus.dispatch("location_changed", {"location": location}) 