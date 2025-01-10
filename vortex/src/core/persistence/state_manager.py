import json
import os
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

class StateManager:
    """Manages persistent storage of zone states."""
    
    def __init__(self):
        self.data_dir = Path("data/zone_states")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def load_zone_state(self, zone_name: str) -> Optional[Dict]:
        """Load the persistent state for a zone."""
        file_path = self.data_dir / f"{zone_name.lower()}_state.json"
        
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    state = json.load(f)
                    
                # Validate and sanitize loaded state
                if self._validate_state(state):
                    return state
                    
        except Exception as e:
            print(f"Error loading state for {zone_name}: {str(e)}")
            
        return None
        
    def save_zone_state(self, zone_name: str, state: Dict) -> bool:
        """Save the current state for a zone."""
        try:
            # Validate state before saving
            if not self._validate_state(state):
                return False
                
            # Add metadata
            state["last_updated"] = datetime.now().isoformat()
            
            # Save to file
            file_path = self.data_dir / f"{zone_name.lower()}_state.json"
            with open(file_path, 'w') as f:
                json.dump(state, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error saving state for {zone_name}: {str(e)}")
            return False
            
    def _validate_state(self, state: Dict) -> bool:
        """Validate the structure of a zone state."""
        required_keys = ["mood", "personality_traits", "environmental_state"]
        
        # Check required keys exist
        if not all(key in state for key in required_keys):
            return False
            
        # Validate mood structure
        mood = state.get("mood", {})
        if not all(key in mood for key in ["harmony", "energy", "resonance"]):
            return False
            
        # Validate personality traits
        traits = state.get("personality_traits", {})
        if not all(key in traits for key in ["openness", "responsiveness", "intensity"]):
            return False
            
        # Validate environmental state
        env_state = state.get("environmental_state", {})
        if not all(key in env_state for key in ["base_description", "current_modifications", "ambient_effects", "collective_imprint"]):
            return False
            
        return True
        
    def get_zone_history(self, zone_name: str) -> Dict:
        """Get historical data about zone evolution."""
        state = self.load_zone_state(zone_name)
        if not state:
            return {}
            
        return {
            "last_updated": state.get("last_updated"),
            "collective_imprint": state.get("environmental_state", {}).get("collective_imprint", {}),
            "ambient_effects": state.get("environmental_state", {}).get("ambient_effects", [])
        }
        
    def reset_zone_state(self, zone_name: str) -> bool:
        """Reset a zone's state to default values."""
        file_path = self.data_dir / f"{zone_name.lower()}_state.json"
        
        try:
            if file_path.exists():
                os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error resetting state for {zone_name}: {str(e)}")
            return False 