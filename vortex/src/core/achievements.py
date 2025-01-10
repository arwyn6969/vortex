"""
Achievement system for tracking player accomplishments.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Callable, Any
from pathlib import Path
import json
from .ui.terminal import TerminalUI

class AchievementCategory(Enum):
    """Categories of achievements."""
    EXPLORATION = auto()
    WISDOM = auto()
    MASTERY = auto()
    SOCIAL = auto()
    HIDDEN = auto()
    CHALLENGE = auto()
    COLLECTION = auto()
    PROGRESSION = auto()
    DISCOVERY = auto()
    SPECIAL = auto()

@dataclass
class AchievementTrigger:
    """Defines conditions for achievement completion."""
    condition: Callable[[Any], bool]
    progress_tracker: Optional[Callable[[Any], float]] = None
    required_value: float = 1.0

@dataclass
class Achievement:
    """Represents a single achievement that can be earned."""
    id: str
    name: str
    description: str
    category: AchievementCategory
    points: int
    hidden: bool = False
    prerequisites: Set[str] = None
    trigger: Optional[AchievementTrigger] = None
    unlock_message: Optional[str] = None
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = set()
        if self.unlock_message is None:
            self.unlock_message = f"Achievement Unlocked: {self.name}!"

@dataclass
class AchievementProgress:
    """Tracks progress towards an achievement."""
    achievement_id: str
    completed: bool
    completion_date: Optional[datetime]
    progress: float = 0.0  # 0.0 to 1.0
    unlock_timestamp: Optional[float] = None
    notification_shown: bool = False

class AchievementNotification:
    """Handles achievement unlock notifications."""
    
    def __init__(self, ui: TerminalUI):
        self.ui = ui
        self.notification_queue: List[Achievement] = []
        
    def queue_notification(self, achievement: Achievement) -> None:
        """Add achievement to notification queue."""
        self.notification_queue.append(achievement)
        
    def show_pending_notifications(self) -> None:
        """Display any pending achievement notifications."""
        while self.notification_queue:
            achievement = self.notification_queue.pop(0)
            self._show_notification(achievement)
            
    def _show_notification(self, achievement: Achievement) -> None:
        """Display a single achievement notification."""
        self.ui.display_text("\n" + "=" * 50)
        self.ui.display_text(achievement.unlock_message)
        self.ui.display_text(f"Points Earned: {achievement.points}")
        self.ui.display_text("=" * 50 + "\n")
        # TODO: Add sound effect when audio system is implemented
        # self.play_unlock_sound()

class AchievementManager:
    """Manages achievements and tracks progress."""
    
    def __init__(self, ui: TerminalUI):
        self.achievements: Dict[str, Achievement] = {}
        self.player_progress: Dict[str, Dict[str, AchievementProgress]] = {}
        self.notification_system = AchievementNotification(ui)
        self._load_achievements()
        
    def _load_achievements(self) -> None:
        """Load achievement definitions."""
        # Define base achievements
        self.register_achievement(Achievement(
            id="first_steps",
            name="First Steps",
            description="Begin your journey in the Vortex",
            category=AchievementCategory.PROGRESSION,
            points=10,
            unlock_message="Welcome to the Vortex! Your journey begins..."
        ))
        
        self.register_achievement(Achievement(
            id="wisdom_seeker",
            name="Wisdom Seeker",
            description="Complete your first challenge in the Wisdom Pond",
            category=AchievementCategory.WISDOM,
            points=20,
            unlock_message="The path of wisdom opens before you..."
        ))
        
        self.register_achievement(Achievement(
            id="stream_walker",
            name="Stream Walker",
            description="Unlock your first stream connection",
            category=AchievementCategory.EXPLORATION,
            points=15,
            unlock_message="You have discovered the flowing streams of knowledge!"
        ))
        
        self.register_achievement(Achievement(
            id="master_of_wisdom",
            name="Master of Wisdom",
            description="Complete all challenges in the Wisdom Pond",
            category=AchievementCategory.MASTERY,
            points=50,
            prerequisites={"wisdom_seeker"},
            unlock_message="You have mastered the depths of wisdom!"
        ))
        
        self.register_achievement(Achievement(
            id="collector",
            name="Collector",
            description="Collect your first item",
            category=AchievementCategory.COLLECTION,
            points=10
        ))
        
        self.register_achievement(Achievement(
            id="explorer",
            name="Explorer",
            description="Visit 3 different ponds",
            category=AchievementCategory.EXPLORATION,
            points=20
        ))
        
        self.register_achievement(Achievement(
            id="hidden_truth",
            name="???",
            description="???",
            category=AchievementCategory.HIDDEN,
            points=30,
            hidden=True,
            unlock_message="A hidden truth reveals itself..."
        ))
        
    def register_achievement(self, achievement: Achievement) -> None:
        """Register a new achievement definition."""
        if not achievement.id or not isinstance(achievement.id, str):
            raise ValueError("Invalid achievement ID")
        self.achievements[achievement.id] = achievement
        
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get achievement definition by ID."""
        if not achievement_id or not isinstance(achievement_id, str):
            raise ValueError("Invalid achievement ID")
        return self.achievements.get(achievement_id)
        
    def get_player_achievements(self, player_id: str) -> Dict[str, AchievementProgress]:
        """Get all achievement progress for a player."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
        return self.player_progress.get(player_id, {})
        
    def update_progress(
        self,
        player_id: str,
        achievement_id: str,
        progress: float
    ) -> None:
        """Update progress towards an achievement."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
        if not achievement_id or not isinstance(achievement_id, str):
            raise ValueError("Invalid achievement ID")
        if not isinstance(progress, (int, float)) or progress < 0:
            raise ValueError("Invalid progress value")
            
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {}
            
        if achievement_id not in self.player_progress[player_id]:
            self.player_progress[player_id][achievement_id] = AchievementProgress(
                achievement_id=achievement_id,
                completed=False,
                completion_date=None,
                progress=0.0
            )
            
        current_progress = self.player_progress[player_id][achievement_id]
        if not current_progress.completed:
            current_progress.progress = min(1.0, progress)
            if current_progress.progress >= 1.0:
                self.complete_achievement(player_id, achievement_id)
                
    def complete_achievement(
        self,
        player_id: str,
        achievement_id: str
    ) -> None:
        """Mark an achievement as completed."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
        if not achievement_id or not isinstance(achievement_id, str):
            raise ValueError("Invalid achievement ID")
            
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {}
            
        if achievement_id not in self.player_progress[player_id]:
            self.player_progress[player_id][achievement_id] = AchievementProgress(
                achievement_id=achievement_id,
                completed=False,
                completion_date=None,
                progress=0.0
            )
            
        progress = self.player_progress[player_id][achievement_id]
        achievement = self.get_achievement(achievement_id)
        
        if achievement and not progress.completed:
            now = datetime.now()
            progress.completed = True
            progress.completion_date = now
            progress.unlock_timestamp = now.timestamp()
            progress.progress = 1.0
            progress.notification_shown = False
            
            # Queue notification
            self.notification_system.queue_notification(achievement)
            
    def process_notifications(self) -> None:
        """Process and display pending achievement notifications."""
        self.notification_system.show_pending_notifications()
        
    def get_available_achievements(
        self,
        player_id: str,
        include_hidden: bool = False
    ) -> List[Achievement]:
        """Get list of achievements available to the player."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
            
        completed = {
            k for k, v in self.get_player_achievements(player_id).items()
            if v.completed
        }
        
        available = []
        for achievement in self.achievements.values():
            if achievement.hidden and not include_hidden:
                continue
                
            if achievement.id in completed:
                continue
                
            if achievement.prerequisites and not achievement.prerequisites.issubset(completed):
                continue
                
            available.append(achievement)
            
        return available
        
    def get_total_points(self, player_id: str) -> int:
        """Get total achievement points earned by player."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
            
        points = 0
        for progress in self.get_player_achievements(player_id).values():
            if progress.completed:
                achievement = self.get_achievement(progress.achievement_id)
                if achievement:
                    points += achievement.points
        return points
        
    def get_completion_percentage(self, player_id: str) -> float:
        """Get overall achievement completion percentage."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
            
        total = len([a for a in self.achievements.values() if not a.hidden])
        if total == 0:
            return 0.0
            
        completed = len([
            p for p in self.get_player_achievements(player_id).values()
            if p.completed and self.get_achievement(p.achievement_id)
            and not self.get_achievement(p.achievement_id).hidden
        ])
        
        return (completed / total) * 100
        
    def save_progress(
        self,
        player_id: str,
        save_dir: str = "saves"
    ) -> bool:
        """Save achievement progress to disk."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
        if not save_dir or not isinstance(save_dir, str):
            raise ValueError("Invalid save directory")
            
        try:
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)
            
            progress = self.get_player_achievements(player_id)
            progress_dict = {
                achievement_id: {
                    "completed": p.completed,
                    "completion_date": p.completion_date.isoformat() if p.completion_date else None,
                    "progress": p.progress,
                    "unlock_timestamp": p.unlock_timestamp,
                    "notification_shown": p.notification_shown
                }
                for achievement_id, p in progress.items()
            }
            
            file_path = save_path / f"{player_id.lower()}_achievements.json"
            with open(file_path, 'w') as f:
                json.dump(progress_dict, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error saving achievement progress: {e}")
            return False
            
    def load_progress(
        self,
        player_id: str,
        save_dir: str = "saves"
    ) -> bool:
        """Load achievement progress from disk."""
        if not player_id or not isinstance(player_id, str):
            raise ValueError("Invalid player ID")
        if not save_dir or not isinstance(save_dir, str):
            raise ValueError("Invalid save directory")
            
        try:
            save_path = Path(save_dir) / f"{player_id.lower()}_achievements.json"
            if not save_path.exists():
                return False
                
            with open(save_path, 'r') as f:
                progress_dict = json.load(f)
                
            self.player_progress[player_id] = {
                achievement_id: AchievementProgress(
                    achievement_id=achievement_id,
                    completed=data["completed"],
                    completion_date=datetime.fromisoformat(data["completion_date"]) if data["completion_date"] else None,
                    progress=data["progress"],
                    unlock_timestamp=data.get("unlock_timestamp"),
                    notification_shown=data.get("notification_shown", True)
                )
                for achievement_id, data in progress_dict.items()
            }
            
            return True
            
        except Exception as e:
            print(f"Error loading achievement progress: {e}")
            return False 