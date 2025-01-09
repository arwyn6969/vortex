"""
Base class for AI-driven guides that assist players throughout their journey.
"""
from typing import Dict, Optional, List, TypedDict
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem

class InteractionRecord(TypedDict):
    """Type definition for interaction history records."""
    context: str
    profile: Dict[ProfileDimension, float]
    metadata: Optional[Dict]

class Guide:
    def __init__(self, name: str, archetype: str):
        """Initialize a new guide.
        
        Args:
            name: The guide's name
            archetype: The guide's archetype (e.g., "Mentor", "Sage", "Trickster")
        """
        self.name = name
        self.archetype = archetype
        self.personality_traits: Dict[str, float] = {}
        self.knowledge_domains: List[str] = []
        self.interaction_history: List[InteractionRecord] = []
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate a personalized welcome message based on player's profile.
        
        Args:
            profile: The player's current profile dimensions
            
        Returns:
            str: A personalized welcome message
        """
        # Adapt tone based on player's profile
        strategic = profile.get(ProfileDimension.STRATEGIC_THINKING, 0.0)
        emotional = profile.get(ProfileDimension.EMOTIONAL_AWARENESS, 0.0)
        
        if strategic > emotional:
            return f"Greetings. I am {self.name}, and I shall guide you through this journey with wisdom and purpose."
        else:
            return f"Welcome, seeker. I am {self.name}, and I'm here to support your journey of discovery."
            
    def get_guidance_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate contextual guidance based on player's profile.
        
        Args:
            profile: The player's current profile dimensions
            
        Returns:
            str: Personalized guidance message
        """
        # Analyze profile to determine areas of growth
        lowest_dimension = min(profile.items(), key=lambda x: x[1])
        highest_dimension = max(profile.items(), key=lambda x: x[1])
        
        return (
            f"I sense great potential in your {highest_dimension[0].value}. "
            f"Perhaps we could explore ways to enhance your {lowest_dimension[0].value}?"
        )
        
    def get_contextual_response(
        self,
        profile: Dict[ProfileDimension, float],
        context: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """Generate a contextual response based on the current situation.
        
        Args:
            profile: The player's current profile
            context: The current context or topic
            metadata: Additional information about the context
            
        Returns:
            str: A contextually appropriate response
        """
        # Record interaction
        self.interaction_history.append({
            'context': context,
            'profile': profile,
            'metadata': metadata
        })
        
        # Generate response based on archetype and context
        if self.archetype == "Mentor":
            return self._generate_mentor_response(context, profile)
        elif self.archetype == "Sage":
            return self._generate_sage_response(context, profile)
        elif self.archetype == "Trickster":
            return self._generate_trickster_response(context, profile)
        else:
            return self._generate_default_response(context, profile)
            
    def suggest_challenges(
        self,
        profile: Dict[ProfileDimension, float],
        available_challenges: List[ContentItem]
    ) -> List[ContentItem]:
        """Suggest appropriate challenges based on player's profile.
        
        Args:
            profile: The player's current profile
            available_challenges: List of available challenges
            
        Returns:
            List[ContentItem]: Sorted list of recommended challenges
        """
        # Calculate challenge suitability scores
        scored_challenges = []
        for challenge in available_challenges:
            score = self._calculate_challenge_suitability(challenge, profile)
            scored_challenges.append((score, challenge))
            
        # Sort by suitability and return top challenges
        scored_challenges.sort(reverse=True)
        return [challenge for _, challenge in scored_challenges]
        
    def _calculate_challenge_suitability(
        self,
        challenge: ContentItem,
        profile: Dict[ProfileDimension, float]
    ) -> float:
        """Calculate how suitable a challenge is for the player.
        
        Args:
            challenge: The challenge to evaluate
            profile: The player's current profile
            
        Returns:
            float: Suitability score (0-1)
        """
        total_score = 0.0
        weights = 0.0
        
        for dimension, required_value in challenge.requirements.items():
            if dimension in profile:
                player_value = profile[dimension]
                # Challenges slightly above player's level are preferred
                difficulty_factor = 1.2
                ideal_value = player_value * difficulty_factor
                
                # Calculate how close the challenge is to the ideal difficulty
                dimension_score = 1.0 - abs(required_value - ideal_value) / ideal_value
                dimension_weight = challenge.dimension_weights.get(dimension, 1.0)
                
                total_score += dimension_score * dimension_weight
                weights += dimension_weight
                
        return total_score / weights if weights > 0 else 0.0
        
    def _generate_mentor_response(
        self,
        context: str,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Generate a response in the style of a mentor archetype."""
        return (
            f"Consider this, my student: {context}. "
            "What insights can you draw from this situation?"
        )
        
    def _generate_sage_response(
        self,
        context: str,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Generate a response in the style of a sage archetype."""
        return (
            f"In the ancient wisdom, we find that {context} "
            "holds deeper meaning than first appears."
        )
        
    def _generate_trickster_response(
        self,
        context: str,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Generate a response in the style of a trickster archetype."""
        return (
            f"Ah, but have you considered looking at {context} "
            "from an entirely different angle? *winks*"
        )
        
    def _generate_default_response(
        self,
        context: str,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Generate a default response when no specific archetype is matched."""
        return f"Let us explore {context} together and see what we discover." 