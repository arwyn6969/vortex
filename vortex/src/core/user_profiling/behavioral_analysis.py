from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from .profile_matrix import ProfileDimension, ProfileMatrix

@dataclass
class InteractionEvent:
    """Represents a single user interaction event."""
    timestamp: float
    event_type: str
    context: str
    duration: float
    metadata: Dict[str, any]

class BehavioralAnalysis:
    """Analyzes user behavior patterns to update their profile."""
    
    def __init__(self, profile_matrix: ProfileMatrix, max_history_age: float = 86400):
        self.profile_matrix = profile_matrix
        self.interaction_history: Dict[str, List[InteractionEvent]] = {}
        self.bot_patterns = self._initialize_bot_patterns()
        self.max_history_age = max_history_age  # Default 24 hours in seconds
        
    def _initialize_bot_patterns(self) -> Dict[str, Dict]:
        """Initialize known bot behavior patterns."""
        return {
            "response_time": {
                "min_human_variance": 0.2,  # Minimum variance in response times
                "min_human_mean": 0.5,      # Minimum mean response time (seconds)
            },
            "interaction_patterns": {
                "max_repetition_ratio": 0.8,  # Maximum ratio of repeated actions
                "min_pattern_variance": 0.3,  # Minimum variance in interaction patterns
            },
            "error_handling": {
                "min_human_error_rate": 0.01,  # Minimum error rate for humans
                "max_human_error_rate": 0.2,   # Maximum error rate for humans
            }
        }
        
    def _cleanup_old_events(self, user_id: str) -> None:
        """Remove events older than max_history_age."""
        if user_id not in self.interaction_history:
            return
            
        current_time = datetime.now().timestamp()
        self.interaction_history[user_id] = [
            event for event in self.interaction_history[user_id]
            if (current_time - event.timestamp) <= self.max_history_age
        ]
        
    def record_interaction(
        self,
        user_id: str,
        event_type: str,
        context: str,
        duration: float,
        metadata: Dict[str, any] = None
    ) -> None:
        """Record a new interaction event for analysis."""
        self._cleanup_old_events(user_id)
        
        if user_id not in self.interaction_history:
            self.interaction_history[user_id] = []
            
        event = InteractionEvent(
            timestamp=datetime.now().timestamp(),
            event_type=event_type,
            context=context,
            duration=duration,
            metadata=metadata or {}
        )
        
        self.interaction_history[user_id].append(event)
        self._analyze_recent_behavior(user_id)
        
    def _analyze_recent_behavior(self, user_id: str) -> None:
        """Analyze recent behavior patterns and update the user's profile."""
        events = self.interaction_history[user_id]
        if len(events) < 5:  # Need minimum number of events for analysis
            return
            
        # Analyze response times
        response_times = [e.duration for e in events]
        time_variance = np.var(response_times)
        time_mean = np.mean(response_times)
        
        # Calculate human probability based on response patterns
        time_human_prob = self._calculate_time_human_probability(
            time_variance,
            time_mean
        )
        
        # Analyze interaction patterns
        pattern_variance = self._calculate_pattern_variance(events)
        pattern_human_prob = self._calculate_pattern_human_probability(
            pattern_variance
        )
        
        # Update profile with new analysis
        self._update_profile_from_analysis(
            user_id,
            time_human_prob,
            pattern_human_prob,
            events
        )
        
    def _calculate_time_human_probability(
        self,
        variance: float,
        mean: float
    ) -> float:
        """Calculate probability of human based on response time patterns."""
        patterns = self.bot_patterns["response_time"]
        
        if variance < patterns["min_human_variance"]:
            return 0.2
        if mean < patterns["min_human_mean"]:
            return 0.3
            
        # Higher variance and reasonable mean suggests human behavior
        return min(0.9, (variance * 0.5 + mean * 0.5))
        
    def _calculate_pattern_variance(
        self,
        events: List[InteractionEvent]
    ) -> float:
        """Calculate variance in interaction patterns."""
        if not events:
            return 0.0
            
        # Convert events to numerical representation
        event_types = [e.event_type for e in events]
        unique_types = list(set(event_types))
        
        if not unique_types:
            return 0.0
            
        # Calculate normalized frequencies
        total_events = len(events)
        type_frequencies = [
            events.count(t) / total_events
            for t in unique_types
        ]
        
        # If only one type, variance is 0
        if len(type_frequencies) == 1:
            return 0.0
            
        return float(np.var(type_frequencies))
        
    def _calculate_pattern_human_probability(
        self,
        pattern_variance: float
    ) -> float:
        """Calculate probability of human based on interaction patterns."""
        patterns = self.bot_patterns["interaction_patterns"]
        
        if pattern_variance < patterns["min_pattern_variance"]:
            return 0.3
            
        return min(0.95, pattern_variance * 2)
        
    def _update_profile_from_analysis(
        self,
        user_id: str,
        time_prob: float,
        pattern_prob: float,
        events: List[InteractionEvent]
    ) -> None:
        """Update user profile based on behavioral analysis."""
        # Combine probabilities with weights
        human_prob = (time_prob * 0.4 + pattern_prob * 0.6)
        
        # Update human probability
        self.profile_matrix.update_human_probability(
            user_id,
            human_prob,
            confidence=min(0.8, len(events) / 100)
        )
        
        # Analyze emotional responses and decision patterns
        self._update_profile_dimensions(user_id, events)
        
    def _update_profile_dimensions(
        self,
        user_id: str,
        events: List[InteractionEvent]
    ) -> None:
        """Update profile dimensions based on interaction patterns."""
        recent_events = events[-20:]  # Analyze last 20 events
        
        # Analyze decision making from interaction patterns
        decision_speed = np.mean([e.duration for e in recent_events])
        decision_consistency = self._calculate_pattern_variance(recent_events)
        
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.DECISION_MAKING,
            1.0 - (decision_speed / 10.0),  # Faster decisions -> higher score
            confidence=0.3
        )
        
        # Analyze emotional responses from metadata
        emotional_responses = [
            e.metadata.get('emotional_value', 0.5)
            for e in recent_events
            if 'emotional_value' in e.metadata
        ]
        
        if emotional_responses:
            emotional_variance = np.var(emotional_responses)
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.EMOTIONAL_RESPONSE,
                emotional_variance,
                confidence=0.4
            ) 