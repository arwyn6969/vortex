"""
LLM-powered dialogue system for guide interactions using Deepseek-R1 70B.

This module provides intelligent, contextually-aware dialogue generation for mythological 
guides in the VORTEX system. It utilizes the Deepseek-R1 70B LLM to create personalized 
interactions based on user profiles, guide attributes, and conversation history.

The system handles:
- Welcome message generation tailored to guide personality and user profile
- Contextual responses to user inputs that maintain character consistency
- Conversation memory to provide coherent multi-turn dialogues
- Fallback mechanisms for error handling and content safety
"""
from typing import Dict, Optional, List, Tuple, Set
from dataclasses import dataclass
from collections import deque
import re
from ..core.user_profiling.profile_matrix import ProfileDimension
# Try Ollama first for local testing, fallback to Deepseek
try:
    from ..core.llm.ollama_client import OllamaClient, GenerationError, ModelLoadError
    USE_OLLAMA = True
except ImportError:
    from ..core.llm.deepseek_client import DeepseekClient, GenerationError, ModelLoadError
    USE_OLLAMA = False

class DialogueError(Exception):
    """Raised when dialogue generation fails.
    
    This exception indicates a failure in the dialogue generation process,
    such as API errors, timeouts, or malformed responses from the LLM.
    """
    pass

class ResponseValidationError(Exception):
    """Raised when generated response fails validation.
    
    This exception is raised when a response is successfully generated
    but fails to meet quality or safety requirements during validation.
    """
    pass

@dataclass
class DialogueContext:
    """Context for dialogue generation.
    
    This dataclass encapsulates all the contextual information needed to 
    generate appropriate dialogue for a specific guide-user interaction.
    
    Attributes:
        guide_name: The name of the mythological guide (e.g., "Thoth", "Isis")
        guide_archetype: The archetypal role of the guide (e.g., "Wisdom Keeper", "Healer")
        cultural_system: The mythological tradition (e.g., "Egyptian", "Norse")
        attributes: Set of character attributes affecting dialogue style
        profile: User's profile dimensions and values
        interaction_history: Record of previous guide-user interactions
        guidance_style: Dictionary mapping style dimensions to intensity values
    """
    guide_name: str
    guide_archetype: str
    cultural_system: str
    attributes: Set[str]
    profile: Dict[ProfileDimension, float]
    interaction_history: List[Dict]
    guidance_style: Dict[str, float]

class LLMDialogueGenerator:
    """Handles LLM-powered dialogue generation for guides.
    
    This class manages the generation of contextually appropriate dialogue for 
    mythological guides, ensuring responses maintain character consistency,
    cultural appropriateness, and relevance to the user's profile and history.
    
    The generator utilizes the Deepseek-R1 LLM with carefully crafted prompts
    to create personalized interactions with appropriate tone and content.
    """
    
    def __init__(self, max_history: int = 10):
        """Initialize dialogue generator.

        Args:
            max_history: Maximum number of interactions to keep in memory.
                Default is 10 turns, which balances context richness with
                token efficiency.
        """
        try:
            if USE_OLLAMA:
                self.llm = OllamaClient()
                print("🤖 Using Ollama client for local LLM testing")
            else:
                self.llm = DeepseekClient()
                print("🌐 Using Deepseek client")
        except ModelLoadError as e:
            # If LLM fails to load, fallback to no LLM
            self.llm = None
            print(f"⚠️  LLM client failed to load: {e}")
        self.max_history = max_history
        self.conversation_memory = deque(maxlen=max_history)
        
    def generate_welcome(self, context: DialogueContext) -> str:
        """Generate a personalized welcome message.

        Creates an initial greeting from a guide to the user that reflects
        the guide's mythological character, cultural background, and responds
        to the user's profile characteristics.

        Args:
            context: Dialogue context containing guide and user information

        Returns:
            A personalized welcome message from the guide to the user

        Raises:
            DialogueError: If message generation fails completely
            ResponseValidationError: If generated content fails validation
        """
        try:
            if not self.llm:
                raise GenerationError("LLM not available")

            prompt = self._create_welcome_prompt(context)
            response = self.llm.generate(
                prompt,
                max_length=256,
                temperature=0.7,
                stop_sequences=["\n", "User:", "Human:"]
            )

            self._validate_response(response, context)
            return self._clean_response(response)

        except (GenerationError, ResponseValidationError) as e:
            return self._generate_fallback_welcome(context, str(e))
        
    def generate_response(self, context: DialogueContext, user_input: str) -> str:
        """Generate a contextually appropriate response.

        Creates a response from the guide to user input that maintains character
        consistency, considers conversation history, and adapts to the user's profile.

        Args:
            context: Dialogue context containing guide and user information
            user_input: The user's message to respond to

        Returns:
            A contextually appropriate response from the guide

        Raises:
            DialogueError: If response generation fails completely
            ResponseValidationError: If generated content fails validation
        """
        try:
            if not self.llm:
                raise GenerationError("LLM not available")

            # Update conversation memory
            self._update_memory(context, user_input)

            prompt = self._create_response_prompt(context, user_input)
            response = self.llm.generate(
                prompt,
                max_length=512,
                temperature=0.8,
                stop_sequences=["\n\n", "User:", "Human:"]
            )

            self._validate_response(response, context)
            cleaned_response = self._clean_response(response)

            # Record successful response
            self._record_successful_response(context, user_input, cleaned_response)
            return cleaned_response

        except (GenerationError, ResponseValidationError) as e:
            return self._generate_fallback_response(context, user_input, str(e))
    
    def _create_welcome_prompt(self, context: DialogueContext) -> str:
        """Create prompt for welcome message generation.
        
        Constructs a detailed prompt instructing the LLM how to generate
        an appropriate welcome message for the specific guide-user context.
        
        Args:
            context: Dialogue context with guide and user information
            
        Returns:
            Formatted prompt string for the LLM
        """
        return f"""You are {context.guide_name}, a {context.guide_archetype} from {context.cultural_system} mythology.
Your attributes are: {', '.join(context.attributes)}.

Your role is to guide users through their journey of self-discovery and growth.
Generate a warm, personalized welcome message that reflects your character and resonates with the user's profile:

User Profile:
{self._format_profile(context.profile)}

Requirements:
1. Embody your mythological role while being approachable
2. Reference your cultural background subtly
3. Show understanding of the user's profile
4. Set a tone matching your attributes
5. Keep the message concise but meaningful

{context.guide_name}'s response:"""
        
    def _create_response_prompt(self, context: DialogueContext, user_input: str) -> str:
        """Create prompt for response generation.
        
        Constructs a detailed prompt instructing the LLM how to generate
        an appropriate response to user input based on the guide's character
        and the conversation context.
        
        Args:
            context: Dialogue context with guide and user information
            user_input: The user message to respond to
            
        Returns:
            Formatted prompt string for the LLM
        """
        recent_history = self._format_recent_history(self.conversation_memory)
        
        return f"""You are {context.guide_name}, a {context.guide_archetype} from {context.cultural_system} mythology.
Your attributes are: {', '.join(context.attributes)}.
Your guidance style preferences are: {self._format_guidance_style(context.guidance_style)}

Based on the user's profile:
{self._format_profile(context.profile)}

{recent_history}
User: {user_input}

Requirements for your response:
1. Maintain your mythological character and wisdom
2. Adapt to the user's profile: {self._get_key_profile_traits(context.profile)}
3. Provide guidance aligned with your attributes: {', '.join(list(context.attributes)[:3])}
4. Match your current guidance style: {self._get_primary_guidance_style(context.guidance_style)}
5. Keep responses concise and focused
6. Show understanding of previous context when relevant

{context.guide_name}'s response:"""
        
    def _validate_response(self, response: str, context: DialogueContext) -> None:
        """Validate generated response meets requirements.
        
        Checks that the generated content meets quality standards,
        maintains character consistency, and has appropriate length.
        
        Args:
            response: The generated response text
            context: The dialogue context used for generation
            
        Raises:
            ResponseValidationError: If the response fails validation
        """
        if not response or len(response.strip()) < 10:
            raise ResponseValidationError("Response too short or empty")
            
        # Check for character consistency
        if context.guide_name.lower() not in response.lower():
            raise ResponseValidationError("Response lacks character voice")
            
        # Check for appropriate length
        if len(response.split()) > 100:  # Adjust threshold as needed
            raise ResponseValidationError("Response too verbose")
            
        # Check for repetition
        if self._has_significant_repetition(response):
            raise ResponseValidationError("Response contains significant repetition")
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the generated response.
        
        Removes artifacts, extra whitespace, and unwanted patterns from
        the LLM-generated text to create a clean final response.
        
        Args:
            response: Raw generated response text
            
        Returns:
            Cleaned and formatted response text
        """
        # Remove any artifacts or unwanted patterns
        response = re.sub(r'[\n\r]+', ' ', response)
        response = re.sub(r'\s+', ' ', response)
        response = re.sub(r'["\']$', '', response)  # Remove trailing quotes
        return response.strip()
    
    def _update_memory(self, context: DialogueContext, user_input: str) -> None:
        """Update conversation memory with new interaction.
        
        Adds the user's input and the current context to the conversation
        memory for reference in future responses.
        
        Args:
            context: Current dialogue context
            user_input: User's message text
        """
        self.conversation_memory.append({
            "user": user_input,
            "context": {
                "profile": context.profile,
                "guidance_style": context.guidance_style
            }
        })
    
    def _record_successful_response(
        self,
        context: DialogueContext,
        user_input: str,
        response: str
    ) -> None:
        """Record successful response in conversation memory.
        
        Updates the most recent interaction in memory with the 
        successfully generated response.
        
        Args:
            context: Current dialogue context
            user_input: The user message that was responded to
            response: The successfully generated response
        """
        if self.conversation_memory and self.conversation_memory[-1]["user"] == user_input:
            self.conversation_memory[-1]["response"] = response
    
    def _generate_fallback_welcome(self, context: DialogueContext, error: str) -> str:
        """Generate a safe fallback welcome message.
        
        Creates a simple, safe welcome message when normal generation fails.
        
        Args:
            context: Dialogue context
            error: Description of the error that occurred
            
        Returns:
            A simple fallback welcome message
        """
        return f"Greetings, I am {context.guide_name}. I look forward to guiding you on your journey."
    
    def _generate_fallback_response(
        self,
        context: DialogueContext,
        user_input: str,
        error: str
    ) -> str:
        """Generate a safe fallback response.
        
        Creates a simple, safe response when normal generation fails.
        
        Args:
            context: Dialogue context
            user_input: The user's message
            error: Description of the error that occurred
            
        Returns:
            A simple fallback response
        """
        return (
            f"As {context.guide_name}, I hear your words. Let us explore this "
            "matter further when our connection is clearer."
        )
    
    def _format_profile(self, profile: Dict[ProfileDimension, float]) -> str:
        """Format profile dimensions for prompt inclusion.
        
        Converts the user's profile data into a string format suitable
        for inclusion in the LLM prompt.
        
        Args:
            profile: Dictionary mapping profile dimensions to values
            
        Returns:
            Formatted string representation of the profile
        """
        return "\n".join(f"- {dim.name}: {value:.2f}" for dim, value in profile.items())
        
    def _format_guidance_style(self, style: Dict[str, float]) -> str:
        """Format guidance style preferences for prompt inclusion.
        
        Converts the guide's style preferences into a string format
        suitable for inclusion in the LLM prompt.
        
        Args:
            style: Dictionary mapping style dimensions to intensity values
            
        Returns:
            Formatted string representation of guidance style
        """
        return ", ".join(f"{k}: {v:.2f}" for k, v in style.items())
    
    def _format_recent_history(self, history: deque) -> str:
        """Format recent conversation history.
        
        Converts the conversation history into a string format
        suitable for inclusion in the LLM prompt.
        
        Args:
            history: Deque containing conversation history entries
            
        Returns:
            Formatted string representation of recent conversation
        """
        if not history:
            return ""
            
        formatted = "Recent interactions:\n"
        for interaction in list(history)[-3:]:  # Last 3 interactions
            formatted += f"User: {interaction['user']}\n"
            if "response" in interaction:
                formatted += f"{interaction['response']}\n"
        return formatted + "\n"
    
    def _get_key_profile_traits(self, profile: Dict[ProfileDimension, float]) -> str:
        """Extract key traits from profile for prompt guidance.
        
        Identifies significant traits in the user profile to highlight
        in the prompt for the LLM.
        
        Args:
            profile: Dictionary mapping profile dimensions to values
            
        Returns:
            String highlighting key profile traits
        """
        significant_traits = [
            f"{dim.name.lower()}:{value:.1f}"
            for dim, value in profile.items()
            if value > 0.7 or value < 0.3
        ]
        return ", ".join(significant_traits[:3]) if significant_traits else "balanced"
    
    def _get_primary_guidance_style(self, style: Dict[str, float]) -> str:
        """Get primary guidance style for prompt context.
        
        Identifies the most prominent guidance style to emphasize
        in the LLM prompt.
        
        Args:
            style: Dictionary mapping style dimensions to intensity values
            
        Returns:
            String describing primary guidance style
        """
        if not style:
            return "balanced"
        primary_style = max(style.items(), key=lambda x: x[1])
        return f"{primary_style[0]} ({primary_style[1]:.1f})"
    
    def _has_significant_repetition(self, text: str) -> bool:
        """Check if text contains significant repetition.
        
        Analyzes the generated text for unwanted repetitive phrases,
        which might indicate low-quality LLM output.
        
        Args:
            text: The text to analyze for repetition
            
        Returns:
            True if significant repetition is detected, False otherwise
        """
        words = text.lower().split()
        if len(words) < 5:
            return False
            
        # Check for repeated phrases
        phrases = [" ".join(words[i:i+3]) for i in range(len(words)-2)]
        phrase_count = {}
        for phrase in phrases:
            if phrase in phrase_count:
                return True
            phrase_count[phrase] = 1
            
        return False 