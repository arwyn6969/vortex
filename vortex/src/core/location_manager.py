"""
Location management functionality for the VORTEX system.

This module handles location state, navigation, and environment descriptions.
It extracts location-specific functionality from the Game class to improve
separation of concerns and maintainability.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from ..core.ui.terminal import TerminalUI
from ..core.engine import CoreEngine

@dataclass
class Location:
    """Represents a location in the game world."""
    name: str
    description: str
    connections: List[str]

class LocationManager:
    """
    Manages location-related functionality including navigation and environment descriptions.
    
    This class consolidates location management logic that was previously spread
    across the Game class, improving modularity and separation of concerns.
    """
    
    def __init__(self, ui: TerminalUI, engine: CoreEngine):
        """
        Initialize the location manager.
        
        Args:
            ui: User interface for location descriptions
            engine: Core game engine for state management
        """
        self.ui = ui
        self.engine = engine
        
        # Initialize default locations
        self.locations: Dict[str, Location] = {
            "Central Hub": Location(
                name="Central Hub",
                description="A serene circular chamber with flowing water channels and ancient symbols.",
                connections=["Wisdom Pond", "Reflection Pool", "Sacred Grove"]
            ),
            "Wisdom Pond": Location(
                name="Wisdom Pond",
                description="A deep pool of crystal-clear water, surrounded by ancient scrolls and mystical artifacts.",
                connections=["Central Hub", "Library of Ages"]
            ),
            "Reflection Pool": Location(
                name="Reflection Pool",
                description="A still pool that mirrors not just your image, but glimpses of your inner self.",
                connections=["Central Hub", "Chamber of Echoes"]
            ),
            "Sacred Grove": Location(
                name="Sacred Grove",
                description="An ethereal garden where ancient trees whisper wisdom of the ages.",
                connections=["Central Hub", "Meditation Glade"]
            )
        }
        
        # CUSTOM DEBUG: Add missing locations for full navigation coverage
        self.add_location(
            "Library of Ages",
            "An ancient repository of knowledge, with towering shelves and scrolls.",
            ["Wisdom Pond"]
        )
        self.add_location(
            "Chamber of Echoes",
            "A chamber where every sound reverberates with deeper meaning.",
            ["Reflection Pool"]
        )
        self.add_location(
            "Meditation Glade",
            "A tranquil glade bathed in soft light and whispers of the wind.",
            ["Sacred Grove"]
        )
        
        # Subscribe to relevant engine events
        self.engine.event_bus.subscribe("location_changed", self._on_location_changed)
        
    def get_current_location(self) -> Optional[Location]:
        """
        Get the current location object.
        
        Returns:
            The current Location object or None if not found
        """
        current = self.engine.get_current_location()
        return self.locations.get(current)
        
    def get_available_connections(self) -> List[str]:
        """
        Get list of available connections from current location.
        
        Returns:
            List of location names that can be reached from current location
        """
        location = self.get_current_location()
        return location.connections if location else []
        
    def can_move_to(self, destination: str) -> bool:
        """
        Check if movement to destination is possible from current location.
        
        Args:
            destination: Name of the destination location
            
        Returns:
            True if movement is possible, False otherwise
        """
        connections = self.get_available_connections()
        return any(destination.lower() in conn.lower() for conn in connections)
        
    def move_to(self, destination: str) -> bool:
        """
        Attempt to move to the specified destination.
        
        Args:
            destination: Name of the destination location
            
        Returns:
            True if movement was successful, False otherwise
        """
        if not self.can_move_to(destination):
            self.ui.display_text(f"You cannot go to {destination} from here.")
            return False
            
        # Find the exact destination name (case-sensitive)
        connections = self.get_available_connections()
        for conn in connections:
            if destination.lower() in conn.lower():
                self.engine.set_current_location(conn)
                # Location description will be shown by the event handler
                return True
                
        return False
        
    def show_location_description(self):
        """Display description of the current location."""
        location = self.get_current_location()
        if not location:
            return
            
        self.ui.display_text(f"\nYou are in the {location.name}")
        self.ui.display_text(f"\n{location.description}")
        
        if location.connections:
            self.ui.display_text("\nPaths lead to:")
            for conn in location.connections:
                self.ui.display_text(f"  • {conn}")
                
    def _on_location_changed(self, data: dict):
        """
        Handle location change events.
        
        Args:
            data: Event data containing the new location
        """
        if data and "location" in data:
            self.show_location_description()
            
    def add_location(self, name: str, description: str, connections: List[str]):
        """
        Add a new location to the game world.
        
        Args:
            name: Name of the new location
            description: Description of the new location
            connections: List of connected location names
        """
        self.locations[name] = Location(
            name=name,
            description=description,
            connections=connections
        )
        
        # Update connections in connected locations
        for conn in connections:
            if conn in self.locations:
                if name not in self.locations[conn].connections:
                    self.locations[conn].connections.append(name)
                    
    def remove_location(self, name: str):
        """
        Remove a location from the game world.
        
        Args:
            name: Name of the location to remove
        """
        if name in self.locations:
            # Remove connections from other locations
            location = self.locations[name]
            for conn in location.connections:
                if conn in self.locations:
                    self.locations[conn].connections.remove(name)
                    
            # Remove the location itself
            del self.locations[name] 