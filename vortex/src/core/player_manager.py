"""
Player management functionality for the VORTEX system.

This module handles player creation, profile management, and persistence.
It extracts player-specific functionality from the Game class to improve
separation of concerns and maintainability.
"""
from typing import Optional, Dict, List, Any
from pathlib import Path
import json
import logging
from datetime import datetime

from ..core.player import Player
from ..core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from ..core.user_profiling.questionnaire import VoightKampffQuestionnaire
from ..core.ui.terminal import TerminalUI
from ..core.config import config

logger = logging.getLogger(__name__)

class PlayerManager:
    """
    Manages player-related functionality including creation, profiles, and persistence.
    
    This class consolidates player management logic that was previously spread
    across the Game class, improving modularity and separation of concerns.
    """
    
    def __init__(self, ui: TerminalUI, profile_matrix: ProfileMatrix):
        """
        Initialize the player manager.
        
        Args:
            ui: User interface for player interaction
            profile_matrix: Profile matrix for managing player profiles
        """
        self.ui = ui
        self.profile_matrix = profile_matrix
        self.questionnaire = VoightKampffQuestionnaire()
        self.player: Optional[Player] = None
        self.last_save_time = datetime.now()
        
    def create_player(self, name: Optional[str] = None) -> Optional[Player]:
        """
        Create a new player instance.
        
        Args:
            name: Optional player name. If None, will prompt for name.
            
        Returns:
            The created Player instance or None if creation failed
            
        Raises:
            ValueError: If the name validation fails
        """
        try:
            if not name:
                name = self.ui.get_input("\nEnter your name, seeker of wisdom: ")
                
            if not name.strip():
                self.ui.display_text("Please enter a valid name.")
                return None
                
            self.player = Player(name)
            self.player.current_pond = config.get("game.starting_location", "Central Hub")
            self.profile_matrix.create_profile(name)
            logger.info(f"Created new player: {name}")
            return self.player
            
        except ValueError as e:
            self.ui.display_text(f"\nError: {e}")
            self.ui.display_text("Please try again.")
            logger.error(f"Player creation failed: {str(e)}")
            return None
            
    def run_questionnaire(self) -> Optional[Dict[ProfileDimension, float]]:
        """
        Run the initial questionnaire and return the profile updates.
        
        Returns:
            Dictionary mapping profile dimensions to values, or None if failed
        """
        if not self.player:
            logger.error("Cannot run questionnaire without a player")
            return None
            
        try:
            self.ui.display_text(
                "\nI will now present you with a series of scenarios. "
                "Your responses will help determine your starting point in the Vortex. "
                "Please answer thoughtfully and honestly - there are no right or wrong answers."
            )
            
            total_questions = len(self.questionnaire.questions)
            if total_questions == 0:
                self.ui.display_text("Error: No questions available in the questionnaire.")
                logger.error("Questionnaire contains no questions")
                return None
                
            profile_updates = {}
            
            for i in range(total_questions):
                if not self._process_question(i, profile_updates, total_questions):
                    continue
            
            # Normalize values to ensure they're within bounds
            for dimension in profile_updates:
                profile_updates[dimension] = max(0.0, min(1.0, profile_updates[dimension]))
            
            logger.info(f"Completed questionnaire for player: {self.player.name}")
            return profile_updates
            
        except Exception as e:
            self.ui.display_text(f"Critical error in questionnaire: {str(e)}")
            logger.exception(f"Questionnaire error: {str(e)}")
            return None
            
    def _process_question(self, 
                          question_index: int, 
                          profile_updates: Dict[ProfileDimension, float], 
                          total_questions: int) -> bool:
        """
        Process a single questionnaire question.
        
        Args:
            question_index: Index of the question to process
            profile_updates: Dictionary to update with profile changes
            total_questions: Total number of questions for normalization
            
        Returns:
            True if question was processed successfully, False otherwise
        """
        import time
        
        question = self.questionnaire.get_question(question_index)
        if not question:
            self.ui.display_text(f"Error: Failed to retrieve question {question_index+1}.")
            return False
            
        # Display question with context
        try:
            if question.context:
                self.ui.display_text(f"\n{question.context}")
            self.ui.display_text(f"\n{question.text}")
        except Exception as e:
            self.ui.display_text(f"Error displaying question {question_index+1}: {str(e)}")
            return False
            
        # Get response
        try:
            response = self.ui.get_input("\nYour response: ")
            if not response.strip():
                self.ui.display_text("Please provide a response.")
                response = self.ui.get_input("\nYour response: ")
        except Exception as e:
            self.ui.display_text(f"Error processing response: {str(e)}")
            return False
        
        # Process response
        try:
            impacts = self.questionnaire.analyze_response(question, response)
            for dimension, value in impacts.items():
                if dimension not in profile_updates:
                    profile_updates[dimension] = 0.0
                profile_updates[dimension] += value / total_questions
        except Exception as e:
            self.ui.display_text(f"Error analyzing response: {str(e)}")
            return False
        
        # Add a thoughtful pause between questions
        self.ui.display_text("\n...")
        time.sleep(config.get("ui.question_pause_seconds", 1.0))
        return True
        
    def save_player(self) -> bool:
        """
        Save the current player state to disk.
        
        Returns:
            True if save was successful, False otherwise
        """
        if not self.player:
            logger.warning("Attempted to save non-existent player")
            return False
            
        try:
            # Create save directory if it doesn't exist
            save_dir = Path(config.get("paths.saves", "saves"))
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare player data
            player_data = {
                "name": self.player.name,
                "current_pond": self.player.current_pond,
                "inventory": self.player.inventory,
                "tokens": {k: v for k, v in self.player.tokens.items()},
                "visited_locations": list(self.player.visited_locations) if hasattr(self.player, 'visited_locations') else [],
                "stats": {k: v for k, v in self.player.stats.items()},
                "saved_at": datetime.now().isoformat()
            }
            
            # Save to file
            save_path = save_dir / f"{self.player.name.lower().replace(' ', '_')}.json"
            with open(save_path, 'w') as f:
                json.dump(player_data, f, indent=2)
                
            self.last_save_time = datetime.now()
            logger.info(f"Saved player data for {self.player.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save player data: {str(e)}")
            return False
            
    def load_player(self, name: str) -> Optional[Player]:
        """
        Load a player from saved data.
        
        Args:
            name: Name of the player to load
            
        Returns:
            Loaded Player instance or None if loading failed
        """
        try:
            save_dir = Path(config.get("paths.saves", "saves"))
            save_path = save_dir / f"{name.lower().replace(' ', '_')}.json"
            
            if not save_path.exists():
                self.ui.display_text(f"No saved data found for {name}.")
                logger.warning(f"No save file found for player: {name}")
                return None
                
            # Load player data
            with open(save_path, 'r') as f:
                player_data = json.load(f)
                
            # Create player and restore data
            self.player = Player(player_data["name"])
            self.player.current_pond = player_data["current_pond"]
            self.player.inventory = player_data["inventory"]
            self.player.tokens = player_data["tokens"]
            
            if "visited_locations" in player_data:
                self.player.visited_locations = player_data["visited_locations"]
                
            if "stats" in player_data:
                self.player.stats = player_data["stats"]
                
            # Ensure profile exists
            if not self.profile_matrix.has_profile(self.player.name):
                self.profile_matrix.create_profile(self.player.name)
                
            logger.info(f"Loaded player data for {self.player.name}")
            return self.player
            
        except Exception as e:
            self.ui.display_text(f"\nError loading player data: {e}")
            logger.error(f"Failed to load player data: {str(e)}")
            return None
            
    def list_saved_players(self) -> List[str]:
        """
        List all saved player names.
        
        Returns:
            List of saved player names
        """
        try:
            save_dir = Path(config.get("paths.saves", "saves"))
            if not save_dir.exists():
                return []
                
            player_files = list(save_dir.glob("*.json"))
            return [p.stem.replace('_', ' ') for p in player_files]
            
        except Exception as e:
            logger.error(f"Error listing saved players: {str(e)}")
            return []
            
    def get_player(self) -> Optional[Player]:
        """
        Get the current player instance.
        
        Returns:
            Current player or None if no player exists
        """
        return self.player
        
    def update_player_location(self, location: str) -> None:
        """
        Update the player's current location and visited locations list.
        
        Args:
            location: The new location name
        """
        if not self.player:
            return
            
        self.player.current_pond = location
        
        # Track unique locations visited
        visited_locations = set(self.player.visited_locations) if hasattr(self.player, 'visited_locations') else set()
        visited_locations.add(location)
        self.player.visited_locations = list(visited_locations)
        
    def should_autosave(self) -> bool:
        """
        Check if enough time has passed for autosave.
        
        Returns:
            True if autosave should be performed, False otherwise
        """
        if not self.player:
            return False
            
        save_interval = config.get("game.save_interval_minutes", 10)
        time_diff = (datetime.now() - self.last_save_time).total_seconds() / 60
        return time_diff >= save_interval 