"""
Guide dialogue system using the new AI service implementation.
Provides dynamic, streaming interactions with mythological guides.
"""

from typing import Dict, Optional, List, AsyncGenerator, Any
from dataclasses import dataclass
from enum import Enum
import logging
from ..core.ai_service import AIService, ModelConfig, ModelProvider

logger = logging.getLogger(__name__)

class GuidanceStyle(Enum):
    """Different styles of guidance a guide can provide."""
    WISE = "wise"
    MYSTERIOUS = "mysterious"
    DIRECT = "direct"
    POETIC = "poetic"
    SOCRATIC = "socratic"

@dataclass
class GuidePersona:
    """Defines a guide's personality and characteristics."""
    name: str
    tradition: str
    style: GuidanceStyle
    description: str
    key_traits: List[str]
    
@dataclass
class DialogueContext:
    """Context for a dialogue interaction."""
    guide: GuidePersona
    user_profile: Dict[str, float]
    conversation_history: List[Dict[str, str]]
    current_location: Optional[str] = None
    current_quest: Optional[str] = None

class DialogueManager:
    """Manages dynamic dialogue interactions with guides."""
    
    def __init__(self, ai_service: AIService):
        """Initialize the dialogue manager.
        
        Args:
            ai_service: The AI service to use for generating responses
        """
        self.ai_service = ai_service
        
    def _create_system_prompt(self, context: DialogueContext) -> str:
        """Create the system prompt for the AI model.
        
        Args:
            context: Current dialogue context
            
        Returns:
            Formatted system prompt
        """
        guide = context.guide
        return f"""You are {guide.name}, a {guide.description} from the {guide.tradition} tradition.
Your guidance style is {guide.style.value} and you embody these traits: {', '.join(guide.key_traits)}.

Key aspects of your personality:
- Always maintain character consistency
- Speak in a way that reflects your tradition and style
- Draw upon {guide.tradition} wisdom and symbolism
- Adapt your guidance to the user's current spiritual development level

Current context:
- Location: {context.current_location or 'Unknown'}
- Active quest: {context.current_quest or 'None'}
- User's spiritual profile: {', '.join(f'{k}: {v:.2f}' for k, v in context.user_profile.items())}
"""

    async def generate_welcome(self, context: DialogueContext) -> str:
        """Generate a welcome message from the guide.
        
        Args:
            context: Current dialogue context
            
        Returns:
            Personalized welcome message
        """
        system = self._create_system_prompt(context)
        prompt = "Generate a warm welcome message for the user, introducing yourself and your role as a guide."
        
        try:
            return await self.ai_service.generate_text(
                prompt=prompt,
                system=system,
                temperature=0.7
            )
        except Exception as e:
            logger.error(f"Failed to generate welcome message: {e}")
            return f"Greetings, I am {context.guide.name}. I look forward to guiding you on your journey."
            
    async def generate_response(
        self,
        context: DialogueContext,
        user_message: str,
        stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        """Generate a response to the user's message.
        
        Args:
            context: Current dialogue context
            user_message: The user's message
            stream: Whether to stream the response
            
        Returns:
            Either a complete response or a stream of response chunks
        """
        system = self._create_system_prompt(context)
        
        # Add recent conversation history to the prompt
        history = "\n".join(
            f"{'User' if msg['role'] == 'user' else context.guide.name}: {msg['content']}"
            for msg in context.conversation_history[-5:]  # Last 5 messages
        )
        
        prompt = f"""Previous conversation:
{history}

User: {user_message}

Respond as {context.guide.name}:"""
        
        try:
            return await self.ai_service.generate_text(
                prompt=prompt,
                system=system,
                temperature=0.8,
                stream=stream
            )
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            if stream:
                async def error_stream():
                    yield "I apologize, but I need a moment to gather my thoughts."
                return error_stream()
            return "I apologize, but I need a moment to gather my thoughts."
            
    async def generate_quest_guidance(
        self,
        context: DialogueContext,
        quest_description: str,
        current_progress: float
    ) -> str:
        """Generate guidance specific to the user's current quest.
        
        Args:
            context: Current dialogue context
            quest_description: Description of the current quest
            current_progress: Progress through the quest (0.0 to 1.0)
            
        Returns:
            Quest-specific guidance
        """
        system = self._create_system_prompt(context)
        
        prompt = f"""The user is on this quest: {quest_description}
Current progress: {current_progress:.0%}

Provide guidance that:
1. Acknowledges their current progress
2. Offers wisdom relevant to their situation
3. Encourages further advancement
4. Relates to your tradition's teachings

Generate guidance:"""
        
        try:
            return await self.ai_service.generate_text(
                prompt=prompt,
                system=system,
                temperature=0.7
            )
        except Exception as e:
            logger.error(f"Failed to generate quest guidance: {e}")
            return f"Continue on your path with wisdom and courage. The way forward will reveal itself."
            
    async def generate_location_insight(
        self,
        context: DialogueContext,
        location_description: str,
        special_elements: List[str]
    ) -> str:
        """Generate mystical insights about the current location.
        
        Args:
            context: Current dialogue context
            location_description: Description of the location
            special_elements: List of special elements present
            
        Returns:
            Mystical insight about the location
        """
        system = self._create_system_prompt(context)
        
        prompt = f"""The user is in this location: {location_description}
Special elements present: {', '.join(special_elements)}

Provide mystical insight that:
1. Reveals deeper meaning of the location
2. Connects to your spiritual tradition
3. Hints at potential wisdom to be gained
4. Acknowledges any special elements

Generate insight:"""
        
        try:
            return await self.ai_service.generate_text(
                prompt=prompt,
                system=system,
                temperature=0.8
            )
        except Exception as e:
            logger.error(f"Failed to generate location insight: {e}")
            return "This place holds ancient wisdom. Be still and listen to its teachings." 