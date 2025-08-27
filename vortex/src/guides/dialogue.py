from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

@dataclass
class GuidePersona:
    """Defines a guide's personality and characteristics."""
    name: str
    tradition: str
    style: "GuidanceStyle"
    description: str
    key_traits: List[str]

class GuidanceStyle(Enum):
    """Different styles of guidance a guide can provide."""
    WISE = "wise"
    MYSTERIOUS = "mysterious"
    DIRECT = "direct"
    POETIC = "poetic"
    SOCRATIC = "socratic"

@dataclass
class DialogueContext:
    """Context for a dialogue interaction."""
    guide: GuidePersona
    user_profile: Dict[str, float]
    conversation_history: List[Dict[str, Any]]
    current_location: Optional[str] = None
    current_quest: Optional[str] = None

class DialogueManager:
    """Stub dialogue manager for playtesting harness."""
    def __init__(self, ai_service: Any):
        self.ai_service = ai_service

    async def generate_welcome(self, context: DialogueContext) -> str:
        """Generate a welcome message. Stubbed for tests."""
        return ""

    async def generate_response(self, context: DialogueContext, user_input: str) -> str:
        """Generate a response. Stubbed for tests."""
        return "" 