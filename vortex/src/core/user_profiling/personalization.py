from typing import Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass
from .profile_matrix import ProfileMatrix, ProfileDimension

T = TypeVar('T')

@dataclass
class ContentItem(Generic[T]):
    """Represents a piece of content that can be personalized."""
    content_id: str
    content: T
    dimension_weights: Dict[ProfileDimension, float]
    difficulty_level: float
    emotional_intensity: float
    creativity_required: float
    strategic_depth: float

class PersonalizationEngine:
    """Manages content personalization based on user profiles."""
    
    def __init__(self, profile_matrix: ProfileMatrix):
        self.profile_matrix = profile_matrix
        self.content_cache: Dict[str, List[ContentItem]] = {}
        
    def register_content(
        self,
        category: str,
        content_item: ContentItem
    ) -> None:
        """Register a new piece of content for personalization."""
        # Validate dimension weights
        if not content_item.dimension_weights:
            raise ValueError("Content item must have at least one dimension weight")
            
        total_weight = sum(content_item.dimension_weights.values())
        if not (0.9 <= total_weight <= 1.1):  # Allow small floating point variance
            raise ValueError(
                f"Dimension weights must sum to approximately 1.0, got {total_weight}"
            )
            
        # Validate numeric fields
        for field in ['difficulty_level', 'emotional_intensity', 
                     'creativity_required', 'strategic_depth']:
            value = getattr(content_item, field)
            if not 0 <= value <= 1:
                raise ValueError(
                    f"{field} must be between 0 and 1, got {value}"
                )
        
        if category not in self.content_cache:
            self.content_cache[category] = []
        self.content_cache[category].append(content_item)
        
    def get_personalized_content(
        self,
        user_id: str,
        category: str,
        count: int = 1
    ) -> List[ContentItem]:
        """Get personalized content items for a user."""
        if count < 1:
            raise ValueError("count must be positive")
            
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return []
            
        if category not in self.content_cache:
            return []
            
        if not self.content_cache[category]:
            return []
            
        # Calculate content scores based on user profile
        scored_content = []
        for item in self.content_cache[category]:
            score = self._calculate_content_score(item, profile.dimensions)
            scored_content.append((score, item))
            
        # Sort by score and return top items
        scored_content.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored_content[:count]]
        
    def _calculate_content_score(
        self,
        item: ContentItem,
        profile_dimensions: Dict[ProfileDimension, float]
    ) -> float:
        """Calculate how well content matches user profile."""
        score = 0.0
        total_weight = 0.0
        
        # Calculate weighted score based on dimension alignment
        for dimension, weight in item.dimension_weights.items():
            if dimension in profile_dimensions:
                profile_value = profile_dimensions[dimension]
                score += weight * (1.0 - abs(profile_value - self._get_content_dimension_value(item, dimension)))
                total_weight += weight
                
        return score / total_weight if total_weight > 0 else 0.0
        
    def _get_content_dimension_value(
        self,
        item: ContentItem,
        dimension: ProfileDimension
    ) -> float:
        """Get content's value for a specific dimension."""
        dimension_mapping = {
            ProfileDimension.DECISION_MAKING: item.difficulty_level,
            ProfileDimension.EMOTIONAL_RESPONSE: item.emotional_intensity,
            ProfileDimension.CREATIVITY: item.creativity_required,
            ProfileDimension.STRATEGIC_THINKING: item.strategic_depth,
        }
        return dimension_mapping.get(dimension, 0.5)
        
    def adapt_difficulty(
        self,
        user_id: str,
        current_difficulty: float,
        success_rate: float
    ) -> float:
        """Adapt content difficulty based on user performance."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return current_difficulty
            
        # Consider user's strategic thinking and decision making abilities
        strategic_ability = profile.dimensions.get(
            ProfileDimension.STRATEGIC_THINKING,
            0.5
        )
        decision_ability = profile.dimensions.get(
            ProfileDimension.DECISION_MAKING,
            0.5
        )
        
        # Calculate ideal difficulty
        target_success_rate = 0.7  # Aim for 70% success rate
        difficulty_delta = (success_rate - target_success_rate) * 0.2
        
        # Adjust based on user abilities
        ability_factor = (strategic_ability + decision_ability) / 2
        new_difficulty = current_difficulty - difficulty_delta
        
        # Scale difficulty change based on user ability
        new_difficulty += (ability_factor - 0.5) * 0.1
        
        # Ensure difficulty stays within bounds
        return max(0.1, min(1.0, new_difficulty))
        
    def get_emotional_intensity(
        self,
        user_id: str
    ) -> float:
        """Determine appropriate emotional intensity for content."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return 0.5
            
        emotional_capacity = profile.dimensions.get(
            ProfileDimension.EMOTIONAL_RESPONSE,
            0.5
        )
        empathy = profile.dimensions.get(ProfileDimension.EMPATHY, 0.5)
        
        # Blend emotional capacity and empathy to determine appropriate intensity
        return (emotional_capacity * 0.7 + empathy * 0.3)
        
    def get_creativity_level(
        self,
        user_id: str
    ) -> float:
        """Determine appropriate creativity level for content."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return 0.5
            
        creativity = profile.dimensions.get(ProfileDimension.CREATIVITY, 0.5)
        strategic = profile.dimensions.get(
            ProfileDimension.STRATEGIC_THINKING,
            0.5
        )
        
        # Blend creativity and strategic thinking
        return (creativity * 0.8 + strategic * 0.2) 