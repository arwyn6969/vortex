"""
Player state management.
"""
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional, Union

from dataclasses import dataclass, asdict

@dataclass
class PlayerState:
    """Represents the complete state of a player that can be saved/loaded."""
    name: str
    current_pond: Optional[str]
    inventory: List[str]
    completed_challenges: Set[str]
    unlocked_streams: Set[str]
    last_save: datetime
    version: str = "1.0.0"

class Player:
    CURRENT_VERSION = "1.0.0"
    VALID_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,32}$')
    
    def __init__(self, name: str):
        if not self._validate_name(name):
            raise ValueError(
                "Invalid player name. Must be 3-32 characters long and contain "
                "only letters, numbers, underscores, and hyphens."
            )
        self.name = name
        self.current_pond = None
        self.inventory: List[str] = []
        self.completed_challenges: Set[str] = set()
        self.unlocked_streams: Set[str] = set()
        
    @classmethod
    def _validate_name(cls, name: str) -> bool:
        """Validate player name format."""
        return bool(cls.VALID_NAME_PATTERN.match(name))
        
    def add_to_inventory(self, item: str) -> None:
        """Add an item to player's inventory."""
        if not item or not isinstance(item, str):
            raise ValueError("Invalid item")
        self.inventory.append(item)
        
    def remove_from_inventory(self, item: str) -> bool:
        """Remove an item from player's inventory."""
        if not item or not isinstance(item, str):
            raise ValueError("Invalid item")
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def has_item(self, item: str) -> bool:
        """Check if player has an item."""
        if not item or not isinstance(item, str):
            raise ValueError("Invalid item")
        return item in self.inventory
    
    def complete_challenge(self, challenge_id: str) -> None:
        """Mark a challenge as completed."""
        if not challenge_id or not isinstance(challenge_id, str):
            raise ValueError("Invalid challenge ID")
        self.completed_challenges.add(challenge_id)
        
    def unlock_stream(self, stream_id: str) -> None:
        """Unlock a stream connection."""
        if not stream_id or not isinstance(stream_id, str):
            raise ValueError("Invalid stream ID")
        self.unlocked_streams.add(stream_id)
        
    def can_access_stream(self, stream_id: str) -> bool:
        """Check if player can access a stream."""
        if not stream_id or not isinstance(stream_id, str):
            raise ValueError("Invalid stream ID")
        return stream_id in self.unlocked_streams

    def to_state(self) -> PlayerState:
        """Convert current player instance to a serializable state."""
        return PlayerState(
            name=self.name,
            current_pond=self.current_pond,
            inventory=self.inventory.copy(),
            completed_challenges=self.completed_challenges.copy(),
            unlocked_streams=self.unlocked_streams.copy(),
            last_save=datetime.now(),
            version=self.CURRENT_VERSION
        )

    @classmethod
    def from_state(cls, state: PlayerState) -> 'Player':
        """Create a new Player instance from a saved state."""
        # Version compatibility check
        if state.version != cls.CURRENT_VERSION:
            raise ValueError(
                f"Save version mismatch. Expected {cls.CURRENT_VERSION}, got {state.version}"
            )
            
        player = cls(state.name)
        player.current_pond = state.current_pond
        player.inventory = state.inventory.copy()
        player.completed_challenges = state.completed_challenges.copy()
        player.unlocked_streams = state.unlocked_streams.copy()
        return player

    def _backup_save_file(self, file_path: Path) -> None:
        """Create a backup of the save file if it exists."""
        if file_path.exists():
            backup_path = file_path.with_suffix('.json.bak')
            shutil.copy2(file_path, backup_path)

    def save(self, save_dir: str = "saves") -> bool:
        """Save player state to disk.
        
        Args:
            save_dir: Directory to save player data in
            
        Returns:
            bool: True if save was successful, False otherwise
            
        Raises:
            ValueError: If save_dir is invalid
        """
        if not save_dir or not isinstance(save_dir, str):
            raise ValueError("Invalid save directory")
            
        try:
            # Ensure save directory exists
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)
            
            # Create state and serialize
            state = self.to_state()
            state_dict = asdict(state)
            
            # Convert sets to lists for JSON serialization
            state_dict['completed_challenges'] = list(state_dict['completed_challenges'])
            state_dict['unlocked_streams'] = list(state_dict['unlocked_streams'])
            state_dict['last_save'] = state_dict['last_save'].isoformat()
            
            # Save to file with backup
            file_path = save_path / f"{self.name.lower()}_save.json"
            self._backup_save_file(file_path)
            
            with open(file_path, 'w') as f:
                json.dump(state_dict, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving player state: {e}")
            return False

    @classmethod
    def load(cls, name: str, save_dir: str = "saves") -> Optional['Player']:
        """Load player state from disk.
        
        Args:
            name: Name of the player to load
            save_dir: Directory containing save files
            
        Returns:
            Optional[Player]: Loaded player instance or None if load failed
            
        Raises:
            ValueError: If name or save_dir is invalid
        """
        if not cls._validate_name(name):
            raise ValueError("Invalid player name")
        if not save_dir or not isinstance(save_dir, str):
            raise ValueError("Invalid save directory")
            
        try:
            # Construct save file path
            save_path = Path(save_dir) / f"{name.lower()}_save.json"
            if not save_path.exists():
                # Try backup file
                backup_path = save_path.with_suffix('.json.bak')
                if backup_path.exists():
                    save_path = backup_path
                else:
                    return None
                
            # Load and parse save file
            with open(save_path, 'r') as f:
                state_dict = json.load(f)
                
            # Version compatibility check
            if state_dict.get('version', '0.0.0') != cls.CURRENT_VERSION:
                raise ValueError(
                    f"Save version mismatch. Expected {cls.CURRENT_VERSION}, "
                    f"got {state_dict.get('version', '0.0.0')}"
                )
                
            # Convert lists back to sets
            state_dict['completed_challenges'] = set(state_dict['completed_challenges'])
            state_dict['unlocked_streams'] = set(state_dict['unlocked_streams'])
            state_dict['last_save'] = datetime.fromisoformat(state_dict['last_save'])
            
            # Create state and player
            state = PlayerState(**state_dict)
            return cls.from_state(state)
            
        except Exception as e:
            print(f"Error loading player state: {e}")
            return None 