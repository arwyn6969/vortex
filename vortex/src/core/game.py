"""
Core game functionality.
"""
from typing import Optional, Dict, List
import time
from pathlib import Path
from datetime import datetime

from ..core.ui.terminal import TerminalUI
from ..core.user_profiling.questionnaire import VoightKampffQuestionnaire
from ..core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension
from ..guides.guide_factory import GuideFactory
from ..core.player import Player
from ..core.engine import CoreEngine
from ..core.achievements import AchievementManager
from ..core.location_manager import LocationManager
from ..core.dialogue_manager import DialogueManager
from ..core.command_processor import CommandProcessor, CommandResult

class Game:
    """Core game class."""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.ui = TerminalUI()
        self.profile_matrix = ProfileMatrix()
        self.questionnaire = VoightKampffQuestionnaire()
        self.guide_factory = GuideFactory()
        self.engine = CoreEngine()
        self.current_guide = None
        self.achievement_manager = AchievementManager(self.ui)
        self.last_save_time = datetime.now()
        
        # Initialize managers
        self.location_manager = LocationManager(self.ui, self.engine)
        self.dialogue_manager = DialogueManager(self.ui, self.guide_factory, self.profile_matrix)
        self.command_processor = CommandProcessor(
            self.ui,
            self.location_manager,
            self.dialogue_manager,
            self.achievement_manager
        )
        
        # Subscribe to engine events
        self.engine.event_bus.subscribe("game_init", self._on_game_init)
        self.engine.event_bus.subscribe("game_end", self._on_game_end)
        
    def _on_location_changed(self, data: dict):
        """Handle location change events."""
        if self.player and data and "location" in data:
            self.player.current_pond = data["location"]
            self._check_exploration_achievements()
            
    def _on_game_init(self, data: Optional[dict] = None):
        """Handle game initialization events."""
        if self.player:
            self.achievement_manager.complete_achievement(self.player.name, "first_steps")
            
    def _on_game_end(self, data: Optional[dict] = None):
        """Handle game end events."""
        if self.player:
            self._save_game()
            
    def _check_exploration_achievements(self):
        """Check and update exploration-based achievements."""
        if not self.player:
            return
            
        # Track unique locations visited
        visited_locations = set(self.player.visited_locations) if hasattr(self.player, 'visited_locations') else set()
        visited_locations.add(self.player.current_pond)
        self.player.visited_locations = list(visited_locations)
        
        # Check explorer achievement
        if len(visited_locations) >= 3:
            self.achievement_manager.complete_achievement(self.player.name, "explorer")
            
    def _save_game(self):
        """Save current game state."""
        if self.player:
            try:
                save_dir = Path("saves")
                save_dir.mkdir(parents=True, exist_ok=True)
                self.achievement_manager.save_progress(self.player.name)
                self.last_save_time = datetime.now()
            except Exception as e:
                self.ui.display_text(f"\nError saving game: {e}")
        
    def start(self):
        """Initialize and start the game."""
        try:
            self.ui.clear_screen()
            self.show_welcome()
            if self.get_player_consent():
                self.create_player()
                initial_profile = self.run_questionnaire()
                if initial_profile:
                    self.profile_matrix.update_profile(self.player.name, initial_profile)
                    self.assign_guide()
                    self.engine.start()  # Start the core engine
                    self.start_game_loop()
        except Exception as e:
            self.ui.display_text(f"\nCritical error starting game: {e}")
            if self.player:
                self._save_game()  # Attempt emergency save
            raise
            
    def show_welcome(self):
        """Display the welcome message."""
        welcome_text = """
        ╔══════════════════════════════════════════════╗
        ║        The Vortex of Enlightenment           ║
        ╚══════════════════════════════════════════════╝
        
        Welcome, seeker of wisdom. You stand at the threshold 
        of a journey through mystical waters and ancient knowledge.
        
        Here, in the Vortex, you will:
        • Explore sacred pools of wisdom
        • Commune with mythological guides
        • Unlock the depths of your consciousness
        • Discover profound truths about yourself
        
        Your choices will shape your path, and your responses
        will determine which guides resonate with your spirit.
        """
        self.ui.display_text(welcome_text)
            
    def get_player_consent(self) -> bool:
        """Get player's consent to start the game."""
        self.ui.display_text(
            "\nBefore we begin your journey, we need to understand your essence "
            "through a series of questions inspired by the Voight-Kampff test."
        )
        response = self.ui.get_input("\nAre you ready to begin? (Y/N) ")
        return response.lower() in ['y', 'yes']
    
    def create_player(self):
        """Create a new player instance."""
        while True:
            try:
                name = self.ui.get_input("\nEnter your name, seeker of wisdom: ")
                if name.strip():
                    self.player = Player(name)
                    self.player.current_pond = "Central Hub"
                    self.profile_matrix.create_profile(name)
                    break
                self.ui.display_text("Please enter a valid name.")
            except ValueError as e:
                self.ui.display_text(f"\nError: {e}")
                self.ui.display_text("Please try again.")
            
    def run_questionnaire(self) -> Optional[Dict[ProfileDimension, float]]:
        """Run the initial questionnaire and return the profile."""
        try:
            self.ui.display_text(
                "\nI will now present you with a series of scenarios. "
                "Your responses will help determine your starting point in the Vortex. "
                "Please answer thoughtfully and honestly - there are no right or wrong answers."
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
                    
                # Display question with context
                try:
                    if hasattr(question, 'context') and question.context:
                        self.ui.display_text(f"\n{question.context}")
                    self.ui.display_text(f"\n{question.text}")
                except Exception as e:
                    self.ui.display_text(f"Error displaying question {i+1}: {str(e)}")
                    continue
                    
                # Get response
                try:
                    response = self.ui.get_input("\nYour response: ")
                    if not response.strip():
                        self.ui.display_text("Please provide a response.")
                        response = self.ui.get_input("\nYour response: ")
                except Exception as e:
                    self.ui.display_text(f"Error processing response: {str(e)}")
                    continue
                
                # Process response
                try:
                    impacts = self.questionnaire.analyze_response(question, response)
                    for dimension, value in impacts.items():
                        if dimension not in profile_updates:
                            profile_updates[dimension] = 0.0
                        profile_updates[dimension] += value / total_questions
                except Exception as e:
                    self.ui.display_text(f"Error analyzing response: {str(e)}")
                    continue
                
                # Add a thoughtful pause between questions
                self.ui.display_text("\n...")
                time.sleep(1)
            
            # Normalize values to ensure they're within bounds
            for dimension in profile_updates:
                profile_updates[dimension] = max(0.0, min(1.0, profile_updates[dimension]))
            
            return profile_updates
            
        except Exception as e:
            self.ui.display_text(f"Critical error in questionnaire: {str(e)}")
            return None
            
    def assign_guide(self):
        """Assign an appropriate guide based on player's behavioral profile."""
        if not self.player:
            return

        # Retrieve the behavioral profile object
        profile_obj = self.profile_matrix.get_profile(self.player.name)
        if not profile_obj:
            return
        # Use the dimensions dict for guide selection and welcome
        profile_map = profile_obj.dimensions

        suitable_guides = self.guide_factory.find_suitable_guides(profile_map)
        if suitable_guides:
            self.current_guide = suitable_guides[0]
            # Initialize dialogue manager with the new guide
            self.dialogue_manager.initialize_dialogue(
                self.current_guide.name,
                self.player.name,
                self.player.current_pond
            )
            welcome = self.current_guide.get_welcome_message(profile_map)
            self.ui.display_text(f"\n{welcome}")
            self.dialogue_manager.add_to_history(self.current_guide.name, welcome)
        else:
            # Fallback to Thoth as default guide
            self.current_guide = self.guide_factory.create_guide("thoth")
            if self.current_guide:
                self.dialogue_manager.initialize_dialogue(
                    "thoth",
                    self.player.name,
                    self.player.current_pond
                )
                welcome = self.current_guide.get_welcome_message(profile_map)
                self.ui.display_text(f"\n{welcome}")
                self.dialogue_manager.add_to_history("thoth", welcome)
                
    def show_location(self):
        """Display current location information."""
        if not self.player or not self.player.current_pond:
            return
        self.location_manager.show_location_description()
                
    def handle_command(self, command: str) -> bool:
        """Handle player commands."""
        if not command:
            return True
            
        parts = command.lower().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in ['quit', 'exit']:
            self._on_game_end(None)
            return False
            
        elif cmd == 'help':
            self.show_help()
            
        elif cmd == 'look':
            self.show_location()
            
        elif cmd == 'go':
            if not args:
                self.ui.display_text("Go where? Please specify a destination.")
                return True
                
            destination = ' '.join(args)
            if self.location_manager.move_to(destination):
                # Update dialogue manager with new location
                self.dialogue_manager.update_location(self.player.current_pond)
                
        elif cmd == 'achievements':
            self._show_achievements()
            
        elif cmd == 'inventory':
            if self.player and self.player.inventory:
                self.ui.display_text("\nYou are carrying:")
                for item in self.player.inventory:
                    self.ui.display_text(f"  • {item}")
            else:
                self.ui.display_text("\nYour inventory is empty.")
                
        else:
            # Try to get a response from the current guide
            response = self.dialogue_manager.get_guide_response(command)
            if response:
                self.ui.display_text(f"\n{response}")
            else:
                self.ui.display_text(f"Unknown command: '{command}'. Type 'help' for available commands.")
            
        # Process any pending achievement notifications
        self.achievement_manager.process_notifications()
        return True
        
    def _show_achievements(self):
        """Display achievement progress."""
        if not self.player:
            return
            
        total_points = self.achievement_manager.get_total_points(self.player.name)
        completion = self.achievement_manager.get_completion_percentage(self.player.name)
        
        self.ui.display_text(f"\nAchievement Progress:")
        self.ui.display_text(f"Total Points: {total_points}")
        self.ui.display_text(f"Completion: {completion:.1f}%\n")
        
        completed = self.achievement_manager.get_player_achievements(self.player.name)
        if completed:
            self.ui.display_text("Completed Achievements:")
            for progress in completed.values():
                if progress.completed:
                    achievement = self.achievement_manager.get_achievement(progress.achievement_id)
                    if achievement and not achievement.hidden:
                        self.ui.display_text(f"• {achievement.name} ({achievement.points} points)")
                        self.ui.display_text(f"  {achievement.description}")
        
    def show_help(self):
        """Display available commands."""
        help_text = """
        Available Commands:
        • look          - Examine your surroundings
        • go [place]    - Move to a connected location
        • inventory     - Check your inventory
        • achievements  - View your achievements
        • help         - Show this help message
        • quit         - Exit the game
        """
        self.ui.display_text(help_text)
        
    def start_game_loop(self):
        """Start the main game loop."""
        self.ui.display_text("\nYour journey begins...")
        self.show_location()
        
        running = True
        while running:
            command = self.ui.get_input("\n> ")
            result = self.command_processor.process_command(command.strip())
            
            if result.status == CommandResult.Status.EXIT:
                running = False
                if result.message:
                    self.ui.display_text(result.message)
                    
        self.ui.display_text("\nThank you for exploring the Vortex of Enlightenment.") 