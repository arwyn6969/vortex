from typing import Dict, List, Optional, TypeVar
from dataclasses import dataclass
from enum import Enum
from .profile_matrix import ProfileMatrix, ProfileDimension, BehavioralProfile
from .personalization import PersonalizationEngine, ContentItem

class LearningPathNode:
    """Represents a node in the adaptive learning path."""
    def __init__(
        self,
        node_id: str,
        content: ContentItem,
        required_dimensions: Dict[ProfileDimension, float],
        next_nodes: List[str] = None
    ):
        self.node_id = node_id
        self.content = content
        self.required_dimensions = required_dimensions
        self.next_nodes = next_nodes or []

class AdaptiveLearningPath:
    """Manages dynamic learning paths that adapt to user progress and profile."""
    
    def __init__(
        self,
        profile_matrix: ProfileMatrix,
        personalization: PersonalizationEngine
    ):
        self.profile_matrix = profile_matrix
        self.personalization = personalization
        self.learning_nodes: Dict[str, LearningPathNode] = {}
        self.user_progress: Dict[str, List[str]] = {}  # user_id -> completed_nodes
        
    def add_node(self, node: LearningPathNode) -> None:
        """Add a new node to the learning path system."""
        self.learning_nodes[node.node_id] = node
        
    def get_next_nodes(
        self,
        user_id: str,
        current_node_id: Optional[str] = None
    ) -> List[LearningPathNode]:
        """Get available next nodes based on user's profile and progress."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return []
            
        completed_nodes = self.user_progress.get(user_id, [])
        
        # If no current node, find entry points
        if not current_node_id:
            return self._get_entry_nodes(profile)
            
        current_node = self.learning_nodes.get(current_node_id)
        if not current_node:
            return []
            
        # Filter next nodes based on requirements and user profile
        available_nodes = []
        for next_node_id in current_node.next_nodes:
            next_node = self.learning_nodes.get(next_node_id)
            if not next_node or next_node_id in completed_nodes:
                continue
                
            if self._meets_requirements(profile, next_node.required_dimensions):
                available_nodes.append(next_node)
                
        return self._sort_by_relevance(available_nodes, profile)
        
    def mark_node_completed(
        self,
        user_id: str,
        node_id: str,
        performance_score: float
    ) -> None:
        """Mark a node as completed and update user's profile."""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = []
            
        if node_id not in self.user_progress[user_id]:
            self.user_progress[user_id].append(node_id)
            
        # Update profile based on node completion
        node = self.learning_nodes.get(node_id)
        if node:
            self._update_profile_from_completion(user_id, node, performance_score)
            
    def get_recommended_path(
        self,
        user_id: str,
        max_nodes: int = 5
    ) -> List[LearningPathNode]:
        """Get a recommended sequence of nodes for the user."""
        profile = self.profile_matrix.get_profile(user_id)
        if not profile:
            return []
            
        path = []
        current_nodes = self._get_entry_nodes(profile)
        visited = set()
        
        while current_nodes and len(path) < max_nodes:
            # Get best next node
            next_node = self._get_best_next_node(current_nodes, profile, visited)
            if not next_node:
                break
                
            path.append(next_node)
            visited.add(next_node.node_id)
            
            # Update current_nodes with next node's connections
            current_nodes = [
                self.learning_nodes[node_id]
                for node_id in next_node.next_nodes
                if node_id not in visited
                and self._meets_requirements(profile, self.learning_nodes[node_id].required_dimensions)
            ]
            
        return path
        
    def _get_entry_nodes(self, profile: BehavioralProfile) -> List[LearningPathNode]:
        """Get suitable entry point nodes based on profile."""
        entry_nodes = []
        for node in self.learning_nodes.values():
            if self._meets_requirements(profile, node.required_dimensions):
                entry_nodes.append(node)
        return self._sort_by_relevance(entry_nodes, profile)
        
    def _meets_requirements(
        self,
        profile: BehavioralProfile,
        requirements: Dict[ProfileDimension, float]
    ) -> bool:
        """Check if profile meets node requirements."""
        for dimension, required_value in requirements.items():
            if profile.dimensions.get(dimension, 0) < required_value:
                return False
        return True
        
    def _sort_by_relevance(
        self,
        nodes: List[LearningPathNode],
        profile: BehavioralProfile
    ) -> List[LearningPathNode]:
        """Sort nodes by relevance to user's profile."""
        def get_relevance_score(node: LearningPathNode) -> float:
            score = 0.0
            for dim, value in node.content.dimension_weights.items():
                profile_value = profile.dimensions.get(dim, 0)
                score += value * (1.0 - abs(profile_value - node.content.difficulty_level))
            return score
            
        return sorted(nodes, key=get_relevance_score, reverse=True)
        
    def _get_best_next_node(
        self,
        nodes: List[LearningPathNode],
        profile: BehavioralProfile,
        visited: set
    ) -> Optional[LearningPathNode]:
        """Select the best next node from available options."""
        valid_nodes = [node for node in nodes if node.node_id not in visited]
        if not valid_nodes:
            return None
            
        return self._sort_by_relevance(valid_nodes, profile)[0]
        
    def _update_profile_from_completion(
        self,
        user_id: str,
        node: LearningPathNode,
        performance_score: float
    ) -> None:
        """Update user's profile based on node completion."""
        for dimension, weight in node.content.dimension_weights.items():
            # Calculate improvement based on performance and content difficulty
            improvement = (
                performance_score *
                weight *
                node.content.difficulty_level *
                0.1  # Scale factor to prevent too rapid growth
            )
            
            # Update profile with improvement
            self.profile_matrix.update_profile(
                user_id=user_id,
                dimension=dimension,
                value=improvement,
                confidence=0.7  # Moderate confidence in the improvement
            ) 