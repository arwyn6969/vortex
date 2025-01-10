"""
Base class for AI-driven guides that assist players throughout their journey.
"""
from typing import Dict, Optional, List, TypedDict, Set
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.archetype_manager import ArchetypeManager, CulturalSystem, ArchetypeMapping

class InteractionRecord(TypedDict):
    """Type definition for interaction history records."""
    context: str
    profile: Dict[ProfileDimension, float]
    metadata: Optional[Dict]

class Guide:
    """Base class for all guides in the system."""
    
    def __init__(
        self,
        name: str,
        archetype_name: str,
        cultural_system: CulturalSystem,
        attributes: Set[str]
    ):
        self.name = name
        self.archetype_name = archetype_name
        self.cultural_system = cultural_system
        self.attributes = attributes
        self.archetype_manager = ArchetypeManager()
        self.interaction_history: List[InteractionRecord] = []
        
        # Load archetype mapping
        self.archetype_mapping = self.archetype_manager.get_archetype(archetype_name)
        if not self.archetype_mapping:
            raise ValueError(f"Invalid archetype name: {archetype_name}")
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Get personalized welcome message based on user profile."""
        raise NotImplementedError("Subclasses must implement get_welcome_message")
    
    def generate_response(
        self,
        user_input: str,
        profile: Dict[ProfileDimension, float],
        context: Optional[Dict] = None
    ) -> str:
        """Generate contextually appropriate response."""
        raise NotImplementedError("Subclasses must implement generate_response")
    
    def record_interaction(
        self,
        context: str,
        profile: Dict[ProfileDimension, float],
        metadata: Optional[Dict] = None
    ) -> None:
        """Record an interaction for future reference."""
        self.interaction_history.append({
            "context": context,
            "profile": profile,
            "metadata": metadata
        })
    
    def get_resonant_dimensions(self) -> Set[str]:
        """Get dimensions that resonate with this guide's archetype."""
        if self.archetype_mapping:
            return self.archetype_mapping.resonant_dimensions
        return set()
    
    def calculate_affinity(self, profile: Dict[ProfileDimension, float]) -> float:
        """Calculate guide's affinity with user profile."""
        if not self.archetype_mapping:
            return 0.0
            
        resonant_dims = self.get_resonant_dimensions()
        if not resonant_dims:
            return 0.5
            
        # Calculate average of resonant dimension values
        total = 0.0
        count = 0
        for dim_name in resonant_dims:
            try:
                dim = ProfileDimension(dim_name)
                if dim in profile:
                    total += profile[dim]
                    count += 1
            except ValueError:
                continue
                
        return total / count if count > 0 else 0.5
    
    def should_adapt_personality(
        self,
        profile: Dict[ProfileDimension, float],
        threshold: float = 0.3
    ) -> bool:
        """Determine if guide should adapt personality based on affinity."""
        return self.calculate_affinity(profile) < threshold 