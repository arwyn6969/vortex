"""
Command processing functionality for the VORTEX system.

This module handles command parsing and execution, extracting command-specific
functionality to improve separation of concerns and maintainability.
"""
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum, auto

from ..core.ui.terminal import TerminalUI
from ..core.location_manager import LocationManager
from ..core.dialogue_manager import DialogueManager
from ..core.achievements import AchievementManager

class CommandResult:
    """Represents the result of a command execution."""
    class Status(Enum):
        SUCCESS = auto()
        FAILURE = auto()
        EXIT = auto()
        
    def __init__(self, status: Status, message: Optional[str] = None):
        self.status = status
        self.message = message

@dataclass
class Command:
    """Represents a game command."""
    name: str
    handler: Callable[..., CommandResult]
    help_text: str
    usage: str
    aliases: List[str] = None

class CommandProcessor:
    """
    Manages command processing including parsing and execution.
    
    This class consolidates command processing logic to improve modularity
    and provide better command handling.
    """
    
    def __init__(
        self,
        ui: TerminalUI,
        location_manager: LocationManager,
        dialogue_manager: DialogueManager,
        achievement_manager: AchievementManager
    ):
        """
        Initialize the command processor.
        
        Args:
            ui: User interface for command feedback
            location_manager: Manager for location-related commands
            dialogue_manager: Manager for dialogue-related commands
            achievement_manager: Manager for achievement-related commands
        """
        self.ui = ui
        self.location_manager = location_manager
        self.dialogue_manager = dialogue_manager
        self.achievement_manager = achievement_manager
        
        # Initialize commands
        self.commands: Dict[str, Command] = {}
        self._register_commands()
        
        # Command aliases for quick lookup
        self.aliases: Dict[str, str] = {}
        self._build_aliases()
        
    def _register_commands(self):
        """Register all available commands."""
        self.commands = {
            "help": Command(
                name="help",
                handler=self._handle_help,
                help_text="Show available commands",
                usage="help [command]",
                aliases=["?", "commands"]
            ),
            "quit": Command(
                name="quit",
                handler=self._handle_quit,
                help_text="Exit the game",
                usage="quit",
                aliases=["exit"]
            ),
            "look": Command(
                name="look",
                handler=self._handle_look,
                help_text="Examine your surroundings",
                usage="look",
                aliases=["l"]
            ),
            "go": Command(
                name="go",
                handler=self._handle_go,
                help_text="Move to a connected location",
                usage="go <place>",
                aliases=["move", "travel"]
            ),
            "inventory": Command(
                name="inventory",
                handler=self._handle_inventory,
                help_text="Check your inventory",
                usage="inventory",
                aliases=["inv", "i"]
            ),
            "achievements": Command(
                name="achievements",
                handler=self._handle_achievements,
                help_text="View your achievements",
                usage="achievements",
                aliases=["ach"]
            )
        }
        
    def _build_aliases(self):
        """Build the alias lookup dictionary."""
        self.aliases.clear()
        for cmd_name, cmd in self.commands.items():
            self.aliases[cmd_name] = cmd_name
            if cmd.aliases:
                for alias in cmd.aliases:
                    self.aliases[alias] = cmd_name
                    
    def _handle_help(self, args: List[str]) -> CommandResult:
        """Handle the help command."""
        if not args:
            # Show general help
            help_text = "\nAvailable Commands:\n"
            for cmd in self.commands.values():
                help_text += f"  {cmd.usage:20} - {cmd.help_text}\n"
            self.ui.display_text(help_text)
            return CommandResult(CommandResult.Status.SUCCESS)
            
        # Show help for specific command
        cmd_name = args[0].lower()
        cmd_name = self.aliases.get(cmd_name)
        if cmd_name and cmd_name in self.commands:
            cmd = self.commands[cmd_name]
            help_text = f"\n{cmd.name.upper()}\n"
            help_text += f"Usage: {cmd.usage}\n"
            help_text += f"Description: {cmd.help_text}\n"
            if cmd.aliases:
                help_text += f"Aliases: {', '.join(cmd.aliases)}\n"
            self.ui.display_text(help_text)
            return CommandResult(CommandResult.Status.SUCCESS)
            
        self.ui.display_text(f"Unknown command: '{args[0]}'")
        return CommandResult(CommandResult.Status.FAILURE)
        
    def _handle_quit(self, args: List[str]) -> CommandResult:
        """Handle the quit command."""
        return CommandResult(CommandResult.Status.EXIT, "Thank you for playing!")
        
    def _handle_look(self, args: List[str]) -> CommandResult:
        """Handle the look command."""
        self.location_manager.show_location_description()
        return CommandResult(CommandResult.Status.SUCCESS)
        
    def _handle_go(self, args: List[str]) -> CommandResult:
        """Handle the go command."""
        if not args:
            return CommandResult(
                CommandResult.Status.FAILURE,
                "Go where? Please specify a destination."
            )
            
        destination = ' '.join(args)
        if self.location_manager.move_to(destination):
            return CommandResult(CommandResult.Status.SUCCESS)
        return CommandResult(CommandResult.Status.FAILURE)
        
    def _handle_inventory(self, args: List[str]) -> CommandResult:
        """Handle the inventory command."""
        # Note: This is a placeholder. The actual inventory handling
        # should be moved to a dedicated InventoryManager class.
        return CommandResult(
            CommandResult.Status.SUCCESS,
            "Your inventory is empty."
        )
        
    def _handle_achievements(self, args: List[str]) -> CommandResult:
        """Handle the achievements command."""
        # For now, we'll use a fixed player ID since we don't have a proper player system yet
        player_id = "BotUser"  # This should be passed from the game context

        # Process any pending notifications first
        self.achievement_manager.process_notifications()

        # Get achievement statistics
        total_points = self.achievement_manager.get_total_points(player_id)
        completion = self.achievement_manager.get_completion_percentage(player_id)

        # Display achievement progress
        self.ui.display_text(f"\nAchievement Progress:")
        self.ui.display_text(f"Total Points: {total_points}")
        self.ui.display_text(f"Completion: {completion:.1f}%\n")

        # Get and display completed achievements
        player_achievements = self.achievement_manager.get_player_achievements(player_id)
        completed_count = sum(1 for progress in player_achievements.values() if progress.completed)

        if completed_count > 0:
            self.ui.display_text("Completed Achievements:")
            for progress in player_achievements.values():
                if progress.completed:
                    achievement = self.achievement_manager.get_achievement(progress.achievement_id)
                    if achievement and not achievement.hidden:
                        self.ui.display_text(f"• {achievement.name} ({achievement.points} points)")
                        self.ui.display_text(f"  {achievement.description}")
        else:
            self.ui.display_text("No achievements completed yet. Keep exploring!")

        return CommandResult(CommandResult.Status.SUCCESS)
        
    def process_command(self, command_str: str) -> CommandResult:
        """
        Process a command string and execute the appropriate action.
        
        Args:
            command_str: The raw command string from the user
            
        Returns:
            A CommandResult indicating the outcome
        """
        if not command_str:
            return CommandResult(CommandResult.Status.SUCCESS)
            
        # Parse command and arguments
        parts = command_str.lower().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Look up command (including aliases)
        cmd_name = self.aliases.get(cmd)
        if cmd_name and cmd_name in self.commands:
            result = self.commands[cmd_name].handler(args)
            if result.message:
                self.ui.display_text(result.message)
            return result
            
        # If no built-in command matches, try dialogue
        response = self.dialogue_manager.get_guide_response(command_str)
        if response:
            self.ui.display_text(f"\n{response}")
            return CommandResult(CommandResult.Status.SUCCESS)
            
        # Unknown command
        self.ui.display_text(
            f"Unknown command: '{command_str}'. "
            "Type 'help' for available commands."
        )
        return CommandResult(CommandResult.Status.FAILURE) 