from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import numpy as np

class ProfileDimension(Enum):
    EMPATHY = "empathy"
    DECISION_MAKING = "decision_making"
    EMOTIONAL_RESPONSE = "emotional_response"
    CREATIVITY = "creativity"
    RISK_TOLERANCE = "risk_tolerance"
    STRATEGIC_THINKING = "strategic_thinking"
    MORAL_ALIGNMENT = "moral_alignment"

@dataclass
class BehavioralProfile:
    """Represents a user's behavioral profile with various dimensions."""
    user_id: str
    dimensions: Dict[ProfileDimension, float]
    confidence_scores: Dict[ProfileDimension, float]
    is_human_probability: float
    last_updated: float  # timestamp
    interaction_count: int

class ProfileMatrix:
    """Manages behavioral profiling and analysis for users."""
    
    def __init__(self):
        self.profiles: Dict[str, BehavioralProfile] = {}
        
    def create_profile(self, user_id: str) -> BehavioralProfile:
        """Initialize a new behavioral profile for a user."""
        profile = BehavioralProfile(
            user_id=user_id,
            dimensions={dim: 0.5 for dim in ProfileDimension},
            confidence_scores={dim: 0.0 for dim in ProfileDimension},
            is_human_probability=0.5,
            last_updated=np.datetime64('now').astype(float),
            interaction_count=0
        )
        self.profiles[user_id] = profile
        return profile

    def update_profile(
        self,
        user_id: str,
        dimension: ProfileDimension,
        value: float,
        confidence: float
    ) -> None:
        """Update a specific dimension of a user's profile."""
        if user_id not in self.profiles:
            self.create_profile(user_id)
            
        profile = self.profiles[user_id]
        current_conf = profile.confidence_scores[dimension]
        new_conf = current_conf + confidence
        
        # Weighted average based on confidence
        current_val = profile.dimensions[dimension]
        profile.dimensions[dimension] = (
            (current_val * current_conf + value * confidence) / new_conf
        )
        profile.confidence_scores[dimension] = new_conf
        profile.interaction_count += 1
        profile.last_updated = np.datetime64('now').astype(float)

    def get_profile(self, user_id: str) -> Optional[BehavioralProfile]:
        """Retrieve a user's behavioral profile."""
        return self.profiles.get(user_id)

    def update_human_probability(
        self,
        user_id: str,
        probability: float,
        confidence: float
    ) -> None:
        """Update the probability that a user is human."""
        if user_id not in self.profiles:
            self.create_profile(user_id)
            
        profile = self.profiles[user_id]
        profile.is_human_probability = probability
        profile.last_updated = np.datetime64('now').astype(float)

    def get_personalization_vector(self, user_id: str) -> Dict[str, float]:
        """Generate a personalization vector for content adaptation."""
        profile = self.get_profile(user_id)
        if not profile:
            return {}
            
        return {
            dim.value: profile.dimensions[dim] * profile.confidence_scores[dim]
            for dim in ProfileDimension
        } 