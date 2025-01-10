"""
Game core functionality.
"""
from typing import Optional, Dict
from pathlib import Path
from datetime import datetime, timedelta
from uuid import UUID

from .player import Player
from .ui.terminal import TerminalUI
from .user_profiling.questionnaire import VoightKampffQuestionnaire
from .user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from .user_profiling.behavioral_analysis import BehavioralAnalysis
from .achievements import AchievementManager
from .finance import TokenService
from .finance.bitcoin_tokens import BitcoinTokenType
from .finance.token_config import SPECIAL_SRC20_MULTIPLIERS, SPECIAL_STAMPS_MULTIPLIERS
from .db.session import get_db

class Game:
    # Auto-save interval in minutes
    AUTO_SAVE_INTERVAL = 15
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.current_zone = None
        self.ui = TerminalUI()
        self.profile_matrix = ProfileMatrix()
        self.behavioral_analysis = BehavioralAnalysis(self.profile_matrix)
        self.questionnaire = VoightKampffQuestionnaire()
        self.achievement_manager = AchievementManager(self.ui)
        self.token_service = TokenService(get_db(), self.achievement_manager)
        self.last_save_time = datetime.now()
        self.last_achievement_check = datetime.now()
        
        # Set up keystroke tracking
        self.ui.set_keystroke_callback(self._handle_keystrokes)
        
    def _handle_keystrokes(self, keystroke_count: int):
        """Handle keystroke tracking and token awards."""
        if self.player and hasattr(self.player, 'id'):
            self.token_service.record_keystrokes(
                UUID(self.player.id), 
                keystroke_count
            )
    
    def start(self):
        """Initialize and start the game."""
        try:
            self.ui.show_intro()
            if self.get_player_consent():
                self.create_player()
                initial_profile = self.run_questionnaire()
                if initial_profile:
                    self.initialize_game_state(initial_profile)
                    # Award first achievement
                    try:
                        self.achievement_manager.complete_achievement(
                            self.player.name,
                            "first_steps"
                        )
                    except ValueError as e:
                        print(f"Error awarding first achievement: {e}")
                    self.main_loop()
        except Exception as e:
            self.ui.display_text(f"\nCritical error starting game: {e}")
            self.emergency_save()
            raise
            
    def get_player_consent(self) -> bool:
        """Get player's consent to start the game."""
        self.ui.display_text(
            "\nWelcome to the Vortex of Enlightenment. "
            "Before we begin your journey, we need to understand your essence "
            "through a series of questions inspired by the Voight-Kampff test."
        )
        response = self.ui.prompt("\nAre you ready to begin? (Y/N)")
        return response.lower() in ['y', 'yes']
    
    def create_player(self):
        """Create a new player instance."""
        while True:
            try:
                name = self.ui.prompt("\nEnter your name, seeker of wisdom:")
                self.player = Player(name)
                self.profile_matrix.create_profile(name)
                break
            except ValueError as e:
                self.ui.display_text(f"\nError: {e}")
                self.ui.display_text("Please try again.")
        
        # Try to load existing save and achievement data
        save_dir = Path("saves")
        if save_dir.exists():
            try:
                loaded_player = Player.load(name)
                if loaded_player:
                    self.player = loaded_player
                    if self.achievement_manager.load_progress(name):
                        self.ui.display_text("\nWelcome back! Your previous journey continues...")
                    else:
                        self.ui.display_text("\nWelcome back! (Achievement data could not be loaded)")
            except ValueError as e:
                self.ui.display_text(f"\nError loading save data: {e}")
                self.ui.display_text("Starting fresh...")
            
    def check_auto_save(self) -> None:
        """Check if it's time for auto-save."""
        now = datetime.now()
        if now - self.last_save_time > timedelta(minutes=self.AUTO_SAVE_INTERVAL):
            self.save_game(auto_save=True)
            self.last_save_time = now
            
    def emergency_save(self) -> None:
        """Attempt emergency save in case of critical error."""
        if self.player:
            try:
                emergency_dir = Path("saves/emergency")
                emergency_dir.mkdir(parents=True, exist_ok=True)
                self.player.save(str(emergency_dir))
                self.achievement_manager.save_progress(
                    self.player.name,
                    str(emergency_dir)
                )
                self.ui.display_text("\nEmergency save completed.")
            except Exception as e:
                self.ui.display_text(f"\nFailed to create emergency save: {e}")
            
    def run_questionnaire(self) -> Optional[Dict[ProfileDimension, float]]:
        """Run the initial questionnaire and return the profile."""
        try:
            self.ui.display_text(
                "\nI will now present you with a series of scenarios. "
                "Your responses will help determine your starting point in the Vortex."
            )
            
            total_questions = len(self.questionnaire.questions)
            if total_questions == 0:
                self.ui.display_text("Error: No questions available in the questionnaire.")
                return None
                
            profile_updates = {}
            
            for i in range(total_questions):
                question = self.questionnaire.get_question(i)
                if not question:
                    self.ui.display_text(f"Error: Failed to retrieve question {i+1}.")
                    continue
                    
                # Display question and options
                try:
                    self.ui.display_text(f"\n{question.text}")
                    for j, option in enumerate(question.options):
                        self.ui.display_text(f"{j + 1}. {option}")
                except Exception as e:
                    self.ui.display_text(f"Error displaying question {i+1}: {str(e)}")
                    continue
                    
                # Get valid response with retry limit
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        response = self.ui.prompt("\nChoose your response (1-4):")
                        option_index = int(response) - 1
                        if 0 <= option_index < len(question.options):
                            break
                        self.ui.display_text(
                            f"Please enter a number between 1 and {len(question.options)}."
                        )
                    except ValueError:
                        self.ui.display_text("Please enter a valid number.")
                    except Exception as e:
                        self.ui.display_text(f"Error processing response: {str(e)}")
                    retry_count += 1
                    
                if retry_count >= max_retries:
                    self.ui.display_text(
                        "Maximum retry attempts reached. Skipping this question."
                    )
                    continue
                
                # Analyze response with error handling
                try:
                    impacts = self.questionnaire.analyze_response(question, option_index)
                    for dimension, value in impacts.items():
                        if dimension not in profile_updates:
                            profile_updates[dimension] = 0.0
                        profile_updates[dimension] += value / total_questions
                except Exception as e:
                    self.ui.display_text(
                        f"Error analyzing response for question {i+1}: {str(e)}"
                    )
                    continue
            
            # Validate final profile
            if not profile_updates:
                self.ui.display_text(
                    "Error: No valid responses were recorded. Please try again."
                )
                return None
                
            # Normalize values to ensure they're within bounds
            for dimension in profile_updates:
                profile_updates[dimension] = max(0.0, min(1.0, profile_updates[dimension]))
                
            return profile_updates
            
        except Exception as e:
            self.ui.display_text(f"Critical error in questionnaire: {str(e)}")
            return None
            
    def initialize_game_state(self, initial_profile: Dict[ProfileDimension, float]):
        """Initialize the game state based on the player's profile."""
        # TODO: Select starting zone based on profile
        pass
    
    def main_loop(self):
        """Main game loop."""
        try:
            while True:
                self.process_input()
                self.update_state()
                self.render()
                self.check_auto_save()
                self.achievement_manager.process_notifications()
        except Exception as e:
            self.ui.display_text(f"\nError in game loop: {e}")
            self.emergency_save()
            raise
            
    def process_input(self):
        """Process player input."""
        command = self.ui.get_command()
        if command == "quit":
            self.save_game()
            self.quit_game()
        elif command == "achievements":
            self.show_achievements()
        elif command == "tokens":
            self.show_token_info()
        elif command == "save":
            self.save_game()
        elif self.current_zone:
            try:
                self.current_zone.process_action(command)
            except Exception as e:
                self.ui.display_text(f"\nError processing command: {e}")
            
    def update_state(self):
        """Update game state."""
        if self.current_zone:
            try:
                # Check for zone-specific achievements
                if self.current_zone.name == "Wisdom Pond":
                    completed_challenges = len(self.player.completed_challenges)
                    if completed_challenges > 0:
                        self.achievement_manager.complete_achievement(
                            self.player.name,
                            "wisdom_seeker"
                        )
                    if completed_challenges >= self.current_zone.total_challenges:
                        self.achievement_manager.complete_achievement(
                            self.player.name,
                            "master_of_wisdom"
                        )
                        
                # Check for stream-related achievements
                if len(self.player.unlocked_streams) > 0:
                    self.achievement_manager.complete_achievement(
                        self.player.name,
                        "stream_walker"
                    )
                    
                # Check for collection achievements
                if len(self.player.inventory) > 0:
                    self.achievement_manager.complete_achievement(
                        self.player.name,
                        "collector"
                    )
                    
                # Check for exploration achievements
                visited_ponds = len(set(
                    challenge_id.split(':')[0]
                    for challenge_id in self.player.completed_challenges
                ))
                if visited_ponds >= 3:
                    self.achievement_manager.complete_achievement(
                        self.player.name,
                        "explorer"
                    )
            except ValueError as e:
                self.ui.display_text(f"\nError updating achievements: {e}")
    
    def render(self):
        """Render current game state."""
        if self.current_zone:
            self.current_zone.render(self.ui)
            
    def show_achievements(self):
        """Display achievement progress."""
        try:
            self.ui.display_text("\n=== Achievements ===")
            
            # Show total points and completion percentage
            total_points = self.achievement_manager.get_total_points(self.player.name)
            completion = self.achievement_manager.get_completion_percentage(self.player.name)
            self.ui.display_text(
                f"\nTotal Achievement Points: {total_points}"
                f"\nCompletion: {completion:.1f}%"
            )
            
            # Show completed achievements
            completed = self.achievement_manager.get_player_achievements(self.player.name)
            if completed:
                self.ui.display_text("\nCompleted Achievements:")
                for progress in completed.values():
                    if progress.completed:
                        achievement = self.achievement_manager.get_achievement(
                            progress.achievement_id
                        )
                        if achievement and not achievement.hidden:
                            completion_time = progress.completion_date.strftime(
                                "%Y-%m-%d %H:%M"
                            ) if progress.completion_date else "Unknown"
                            self.ui.display_text(
                                f"- {achievement.name} ({achievement.points} points)"
                                f"\n  {achievement.description}"
                                f"\n  Completed: {completion_time}"
                            )
                            
            # Show available achievements
            available = self.achievement_manager.get_available_achievements(
                self.player.name,
                include_hidden=False
            )
            if available:
                self.ui.display_text("\nAvailable Achievements:")
                for achievement in available:
                    progress = completed.get(achievement.id)
                    progress_str = f" - {progress.progress*100:.0f}%" if progress else ""
                    self.ui.display_text(
                        f"- {achievement.name} ({achievement.points} points)"
                        f"\n  {achievement.description}{progress_str}"
                    )
        except Exception as e:
            self.ui.display_text(f"\nError displaying achievements: {e}")
                
    def save_game(self, auto_save: bool = False):
        """Save current game state."""
        if self.player:
            try:
                self.player.save()
                self.achievement_manager.save_progress(self.player.name)
                if not auto_save:
                    self.ui.display_text("\nGame progress saved.")
                self.last_save_time = datetime.now()
            except Exception as e:
                self.ui.display_text(f"\nError saving game: {e}")
    
    def quit_game(self):
        """Clean up and exit the game."""
        self.ui.display_text("\nThank you for exploring the Vortex. Until we meet again...")
        exit(0) 
    
    async def show_token_info(self):
        """Display token information if available."""
        if not self.player or not hasattr(self.player, 'id'):
            return
            
        balance = self.token_service.get_balance(UUID(self.player.id))
        if balance is None:
            self.ui.display_text("\nNo token information available yet.")
            return
            
        self.ui.display_text(f"\nCurrent Token Balance: {balance}")
        
        # Show Bitcoin token balances and multipliers
        bitcoin_tokens = await self.token_service.get_bitcoin_token_balances(
            UUID(self.player.id),
            force_refresh=True
        )
        
        if bitcoin_tokens:
            self.ui.display_text("\nBitcoin Token Balances:")
            
            # Group tokens by type
            src20_tokens = []
            stamps = []
            for token in bitcoin_tokens:
                if token.balance > 0:
                    if token.token_type == BitcoinTokenType.SRC20:
                        src20_tokens.append(token)
                    else:  # STAMPS
                        stamps.append(token)
            
            # Show SRC-20 tokens
            if src20_tokens:
                self.ui.display_text("\nSRC-20 Tokens:")
                for token in src20_tokens:
                    multiplier = SPECIAL_SRC20_MULTIPLIERS.get(token.token_id)
                    multiplier_text = f" (+{multiplier}x multiplier)" if multiplier else ""
                    self.ui.display_text(
                        f"- {token.token_id}: {token.balance}{multiplier_text}"
                    )
            
            # Show STAMPS
            if stamps:
                self.ui.display_text("\nSTAMPS:")
                for token in stamps:
                    multiplier = SPECIAL_STAMPS_MULTIPLIERS.get(token.token_id)
                    multiplier_text = f" (+{multiplier}x multiplier)" if multiplier else ""
                    self.ui.display_text(
                        f"- {token.token_id}: {token.balance}{multiplier_text}"
                    )
            
            # Show total special token multiplier
            special_multiplier = await self.token_service._get_special_token_multiplier(
                UUID(self.player.id)
            )
            if special_multiplier > 1:
                self.ui.display_text(
                    f"\nTotal Token Multiplier: {special_multiplier}x "
                    "(from owned STAMPS and SRC-20 tokens)"
                )
        
        # Show recent transactions
        transactions = self.token_service.get_transaction_history(
            UUID(self.player.id),
            limit=5
        )
        if transactions:
            self.ui.display_text("\nRecent Transactions:")
            for tx in transactions:
                self.ui.display_text(
                    f"- {tx.description}: {tx.amount} tokens"
                )
    
    async def set_bitcoin_address(self, address: str):
        """Set the user's Bitcoin address for STAMPS/SRC20 tracking.
        
        Args:
            address: Bitcoin address to associate with the user
        """
        if not self.player or not hasattr(self.player, 'id'):
            return
            
        # Get user's token balance record
        balance = self.token_service.get_balance_record(UUID(self.player.id))
        if balance:
            balance.bitcoin_address = address
            self.token_service.db.commit()
            self.ui.display_text(f"\nBitcoin address set: {address}")
            
            # Fetch initial balances
            await self.show_token_info()
        else:
            self.ui.display_text("\nError: Could not set Bitcoin address.") 