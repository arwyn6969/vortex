"""Token-related achievements."""

from typing import Dict
from ..achievements import Achievement, AchievementCategory, AchievementTrigger

TOKEN_ACHIEVEMENTS: Dict[str, Achievement] = {
    "token_discovery": Achievement(
        id="token_discovery",
        name="Token Discovery",
        description="Discover the hidden token system by accumulating enough tokens",
        category=AchievementCategory.HIDDEN,
        points=50,
        hidden=True,
        unlock_message="You've discovered the hidden token system! Keep earning tokens through your actions."
    ),
    
    "token_milestone_1000": Achievement(
        id="token_milestone_1000",
        name="Token Collector",
        description="Accumulate 1,000 tokens",
        category=AchievementCategory.PROGRESSION,
        points=100,
        prerequisites={"token_discovery"},
        unlock_message="You've accumulated 1,000 tokens! Your journey in the token economy begins."
    ),
    
    "token_milestone_10000": Achievement(
        id="token_milestone_10000",
        name="Token Master",
        description="Accumulate 10,000 tokens",
        category=AchievementCategory.PROGRESSION,
        points=250,
        prerequisites={"token_milestone_1000"},
        unlock_message="You've accumulated 10,000 tokens! Your mastery of the token system grows."
    ),
    
    "token_milestone_100000": Achievement(
        id="token_milestone_100000",
        name="Token Legend",
        description="Accumulate 100,000 tokens",
        category=AchievementCategory.PROGRESSION,
        points=500,
        prerequisites={"token_milestone_10000"},
        unlock_message="You've accumulated 100,000 tokens! You are now a legend in the token economy."
    ),
    
    "multiplier_master": Achievement(
        id="multiplier_master",
        name="Multiplier Master",
        description="Have 3 or more active token multipliers at once",
        category=AchievementCategory.SPECIAL,
        points=150,
        prerequisites={"token_discovery"},
        unlock_message="You've mastered the art of token multiplication!"
    ),
    
    "keystroke_king": Achievement(
        id="keystroke_king",
        name="Keystroke King",
        description="Earn tokens from 10,000 keystrokes",
        category=AchievementCategory.PROGRESSION,
        points=200,
        prerequisites={"token_discovery"},
        unlock_message="Your fingers have danced across the keyboard 10,000 times, earning you this royal title!"
    ),
    
    "spending_spree": Achievement(
        id="spending_spree",
        name="Spending Spree",
        description="Spend 5,000 tokens in a single transaction",
        category=AchievementCategory.SPECIAL,
        points=300,
        prerequisites={"token_milestone_10000"},
        unlock_message="Big spender! You've made a significant investment in the system."
    ),
    
    "token_efficiency": Achievement(
        id="token_efficiency",
        name="Token Efficiency",
        description="Maintain a token earning rate of 10 tokens per minute for 5 minutes",
        category=AchievementCategory.SPECIAL,
        points=250,
        prerequisites={"token_discovery"},
        unlock_message="You've achieved peak token earning efficiency!"
    ),
    
    "daily_dedication": Achievement(
        id="daily_dedication",
        name="Daily Dedication",
        description="Earn tokens on 7 consecutive days",
        category=AchievementCategory.PROGRESSION,
        points=150,
        prerequisites={"token_discovery"},
        unlock_message="Your dedication to daily token earning has been rewarded!"
    ),
    
    "token_philanthropist": Achievement(
        id="token_philanthropist",
        name="Token Philanthropist",
        description="Help another user earn their first tokens",
        category=AchievementCategory.SOCIAL,
        points=200,
        prerequisites={"token_milestone_1000"},
        unlock_message="Your generosity in sharing the token system has been recognized!"
    )
}

def register_token_achievements(achievement_manager):
    """Register all token-related achievements with the achievement manager."""
    for achievement in TOKEN_ACHIEVEMENTS.values():
        achievement_manager.register_achievement(achievement) 