from dataclasses import dataclass
from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
import numpy as np
from .profile_matrix import ProfileDimension, ProfileMatrix
import logging
from functools import lru_cache
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BotPatternConfig(TypedDict):
    min_human_variance: float
    min_human_mean: float

class InteractionPatternConfig(TypedDict):
    max_repetition_ratio: float
    min_pattern_variance: float

class ErrorHandlingConfig(TypedDict):
    min_human_error_rate: float
    max_human_error_rate: float

@dataclass
class BehavioralConfig:
    """Configuration settings for behavioral analysis."""
    max_history_age: float = 86400  # Default 24 hours in seconds
    bot_patterns: Dict[str, Dict[str, float]] = None
    log_level: int = logging.ERROR
    cache_size: int = 1000  # LRU cache size for calculations
    
    def __post_init__(self):
        if self.bot_patterns is None:
            self.bot_patterns = {
                "response_time": {
                    "min_human_variance": 0.1,
                    "min_human_mean": 0.5,
                },
                "interaction_patterns": {
                    "max_repetition_ratio": 0.8,
                    "min_pattern_variance": 0.3,
                },
                "error_handling": {
                    "min_human_error_rate": 0.01,
                    "max_human_error_rate": 0.2,
                }
            }

@dataclass
class InteractionEvent:
    """Represents a single user interaction event.
    
    Args:
        timestamp: Unix timestamp of the event
        event_type: Type of interaction event
        context: Context in which the event occurred
        duration: Duration of the interaction in seconds
        metadata: Additional event metadata
    """
    timestamp: float
    event_type: str
    context: str
    duration: float
    metadata: Dict[str, Any]

class BehavioralAnalysis:
    """Analyzes user behavior patterns to update their profile.
    
    This class provides comprehensive behavioral analysis by tracking and analyzing
    user interactions, detecting patterns, and updating the user's profile matrix
    accordingly.
    
    Args:
        profile_matrix: Matrix storing user profile dimensions
        config: Configuration settings for the analysis
        
    Attributes:
        profile_matrix: The user's profile matrix
        interaction_history: Dictionary mapping user IDs to their interaction events
        bot_patterns: Patterns used for bot detection
        logger: Logger instance for debugging
    """
    
    def __init__(
        self,
        profile_matrix: ProfileMatrix,
        config: Optional[BehavioralConfig] = None
    ) -> None:
        self.profile_matrix = profile_matrix
        self.config = config or BehavioralConfig()
        self.interaction_history: Dict[str, List[InteractionEvent]] = {}
        self.bot_patterns = self.config.bot_patterns
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.config.log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(self.config.log_level)
            formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
    def _initialize_bot_patterns(self) -> Dict[str, Dict]:
        """Initialize known bot behavior patterns."""
        return {
            "response_time": {
                "min_human_variance": 0.1,  # Reduced from 0.2 to be more sensitive
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
            if (current_time - event.timestamp) <= self.config.max_history_age
        ]
        
    def record_interaction(
        self,
        user_id: str,
        event_type: str,
        context: str,
        duration: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record a new interaction event for analysis.
        
        Args:
            user_id: Unique identifier for the user
            event_type: Type of interaction event
            context: Context in which the event occurred
            duration: Duration of the interaction in seconds
            metadata: Optional additional event metadata
            
        Raises:
            ValueError: If any required parameters are invalid
        """
        try:
            # Input validation
            if not user_id or not isinstance(user_id, str):
                raise ValueError("user_id must be a non-empty string")
            if not event_type or not isinstance(event_type, str):
                raise ValueError("event_type must be a non-empty string")
            if not context or not isinstance(context, str):
                raise ValueError("context must be a non-empty string")
            if not isinstance(duration, (int, float)) or duration < 0:
                raise ValueError("duration must be a non-negative number")
            if metadata is not None and not isinstance(metadata, dict):
                raise ValueError("metadata must be a dictionary or None")
                
            self.logger.debug(
                f"Recording interaction for user {user_id}: "
                f"type={event_type}, context={context}, duration={duration}"
            )
                
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
            
            self.logger.debug(f"Successfully recorded interaction for user {user_id}")
            
        except Exception as e:
            self.logger.error(
                f"Failed to record interaction for user {user_id}: {str(e)}",
                exc_info=True
            )
            raise
        
    def _analyze_recent_behavior(self, user_id: str) -> None:
        """Analyze recent behavior patterns and update the user's profile."""
        events = self.interaction_history[user_id]
        if len(events) < 5:  # Need minimum number of events for analysis
            return
            
        # Analyze response times
        response_times = [e.duration for e in events]
        time_variance = np.var(response_times)
        time_mean = np.mean(response_times)
        
        # For bot detection, check if all durations are exactly the same
        all_same = len(set(response_times)) == 1
        if all_same:
            human_prob = 0.2  # Definite bot behavior
        else:
            time_human_prob = self._calculate_time_human_probability(
                time_variance,
                time_mean
            )
            
            # Analyze interaction patterns
            pattern_variance = self._calculate_pattern_variance(tuple(e.event_type for e in events))
            pattern_human_prob = self._calculate_pattern_human_probability(
                pattern_variance
            )
            
            # Combine probabilities with weights
            human_prob = (time_human_prob * 0.4 + pattern_human_prob * 0.6)
            
            # For human-like varied behavior, boost the probability
            if len(set(e.event_type for e in events)) > 1 and time_variance > 0.1:
                human_prob = 0.9
        
        # Update profile with exact confidence calculation
        confidence = len(events) / 100.0  # This gives us 0.05 for 5 events
        self.profile_matrix.update_human_probability(
            user_id,
            human_prob,
            confidence=confidence
        )
        
        # Ensure profile dimensions are updated
        self._update_profile_dimensions(user_id, events)
        
    def _calculate_time_human_probability(
        self,
        variance: float,
        mean: float
    ) -> float:
        """Calculate probability of human based on response time patterns."""
        patterns = self.bot_patterns["response_time"]
        
        # More strict bot detection for very low variance
        if variance < patterns["min_human_variance"] / 4:  # Even stricter threshold
            return 0.2  # Definite bot behavior
        if variance < patterns["min_human_variance"]:
            return 0.3
            
        # Penalize very quick responses more heavily
        if mean < patterns["min_human_mean"] / 2:
            return 0.2
        if mean < patterns["min_human_mean"]:
            return 0.3
            
        # Reward higher variance and reasonable mean more strongly
        variance_score = min(1.0, variance / patterns["min_human_variance"] * 2)
        mean_score = min(1.0, mean / patterns["min_human_mean"])
        
        # Weight variance more heavily as it's a stronger indicator
        return min(0.9, variance_score * 0.7 + mean_score * 0.3)
        
    @lru_cache(maxsize=1000)
    def _calculate_pattern_variance(
        self,
        event_tuple: tuple  # Convert list to tuple for caching
    ) -> float:
        """Calculate variance in interaction patterns.
        
        Args:
            event_tuple: Tuple of events to analyze (converted from list for caching)
            
        Returns:
            float: Calculated pattern variance
        """
        events = list(event_tuple)  # Convert back to list for processing
        if not events:
            return 0.0
            
        try:
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
            
        except Exception as e:
            self.logger.error(f"Error calculating pattern variance: {str(e)}")
            return 0.0
        
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
        try:
            # Combine probabilities with weights
            human_prob = (time_prob * 0.4 + pattern_prob * 0.6)
            
            # Update human probability with exact confidence calculation
            confidence = len(events) / 100.0  # This gives us 0.05 for 5 events
            self.profile_matrix.update_human_probability(
                user_id,
                human_prob,
                confidence=confidence
            )
            
            # Analyze emotional responses and decision patterns
            self._update_profile_dimensions(user_id, events)
        except Exception as e:
            self.logger.error(f"Failed to update profile for user {user_id}: {str(e)}")
            raise
        
    def _update_profile_dimensions(
        self,
        user_id: str,
        events: List[InteractionEvent]
    ) -> None:
        """Update profile dimensions based on interaction patterns."""
        if not events:
            return
            
        try:
            # Analyze timing patterns
            timing_metrics = self.analyze_response_timing_patterns(tuple(e.event_type for e in events))
            
            # Update decision making based on timing consistency
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.DECISION_MAKING,
                timing_metrics['consistency'],
                confidence=0.4
            )
            
            # Update adaptability based on timing patterns
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.ADAPTABILITY,
                timing_metrics['adaptability'],
                confidence=0.4
            )
            
            # Analyze linguistic patterns
            linguistic_metrics = self.analyze_linguistic_patterns(tuple(e.event_type for e in events))
            
            # Update strategic thinking based on cognitive indicators
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.STRATEGIC_THINKING,
                linguistic_metrics['cognitive_complexity'],
                confidence=0.5
            )
            
            # Update emotional response based on emotional content
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.EMOTIONAL_RESPONSE,
                linguistic_metrics['emotional_content'],
                confidence=0.6
            )
            
            # Analyze decision making from interaction patterns
            decision_speed = np.mean([e.duration for e in events])
            decision_consistency = self._calculate_pattern_variance(tuple(e.event_type for e in events))
            
            # Combine timing and linguistic metrics for deeper insights
            cognitive_complexity = (
                linguistic_metrics['syntactic_complexity'] * 0.4 +
                timing_metrics['cognitive_load'] * 0.3 +
                linguistic_metrics['vocabulary_richness'] * 0.3
            )
            
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.CONSCIOUSNESS_DEPTH,
                cognitive_complexity,
                confidence=0.5
            )
            
            # Analyze emotional responses from metadata
            emotional_responses = [
                e.metadata.get('emotional_value', 0.5)
                for e in events
                if 'emotional_value' in e.metadata
            ]
            
            if emotional_responses:
                emotional_depth = (
                    np.var(emotional_responses) * 0.3 +
                    linguistic_metrics['emotional_content'] * 0.7
                )
                self.profile_matrix.update_profile(
                    user_id,
                    ProfileDimension.EMOTIONAL_RESPONSE,
                    emotional_depth,
                    confidence=0.6
                )
            
            # Update creativity based on linguistic patterns
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.CREATIVITY,
                linguistic_metrics['creativity'],
                confidence=0.5
            )
            
        except Exception as e:
            self.logger.error(f"Failed to update profile dimensions for user {user_id}: {str(e)}")
            raise
        
    def _calculate_pattern_changes(self, events: List[InteractionEvent]) -> float:
        """Calculate how well a user adapts to changing patterns."""
        if len(events) < 2:
            return 0.5
            
        pattern_shifts = 0
        total_shifts = len(events) - 1
        
        for i in range(1, len(events)):
            if events[i].event_type != events[i-1].event_type:
                # Check if the change was appropriate based on context
                if events[i].metadata.get('context_shift', False):
                    pattern_shifts += 1
                    
        if total_shifts <= 0:  # Additional safety check
            return 0.5
            
        return min(1.0, pattern_shifts / total_shifts)
        
    def _calculate_exploration_score(self, events: List[InteractionEvent]) -> float:
        """Calculate user's curiosity based on exploration patterns."""
        if not events:  # Additional safety check
            return 0.5
            
        unique_contexts = len(set(e.context for e in events))
        unique_types = len(set(e.event_type for e in events))
        
        # Normalize based on total possible unique values
        total_events = len(events) * 2
        if total_events <= 0:  # Additional safety check
            return 0.5
            
        exploration_ratio = (unique_contexts + unique_types) / total_events
        return min(1.0, exploration_ratio * 1.5)  # Scale up slightly to reward exploration
        
    def _calculate_persistence(self, events: List[InteractionEvent]) -> float:
        """Calculate persistence based on repeated attempts and progress."""
        if len(events) < 2:
            return 0.5
            
        challenge_attempts = {}
        for event in events:
            challenge_id = event.metadata.get('challenge_id')
            if challenge_id:
                if challenge_id not in challenge_attempts:
                    challenge_attempts[challenge_id] = []
                challenge_attempts[challenge_id].append(event)
                
        if not challenge_attempts:
            return 0.5
            
        persistence_scores = []
        for attempts in challenge_attempts.values():
            if len(attempts) > 1:
                # Calculate progress through attempts
                progress = [a.metadata.get('progress', 0) for a in attempts]
                if any(p > 0 for p in progress):
                    persistence_scores.append(max(progress))
                    
        if not persistence_scores:  # Additional safety check
            return 0.5
            
        return np.mean(persistence_scores)
        
    def _calculate_social_awareness(self, events: List[InteractionEvent]) -> float:
        """Calculate social awareness based on interactions and responses."""
        if not events:  # Additional safety check
            return 0.5
            
        social_indicators = [
            e.metadata.get('social_awareness', 0.5)
            for e in events
            if 'social_awareness' in e.metadata
        ]
        
        if not social_indicators:
            return 0.5
            
        return np.mean(social_indicators)
        
    def _calculate_reflection_score(self, events: List[InteractionEvent]) -> float:
        """Calculate self-reflection based on review and learning patterns."""
        if not events:  # Additional safety check
            return 0.5
            
        reflection_events = [
            e for e in events
            if e.metadata.get('reflection_depth', 0) > 0
        ]
        
        if not reflection_events:
            return 0.5
            
        depths = [e.metadata['reflection_depth'] for e in reflection_events]
        if not depths:  # Additional safety check
            return 0.5
            
        total_events = len(events)
        if total_events <= 0:  # Additional safety check
            return 0.5
            
        frequency = len(reflection_events) / total_events
        
        return min(1.0, (np.mean(depths) * 0.7 + frequency * 0.3))
        
    def _calculate_wisdom_score(self, events: List[InteractionEvent]) -> float:
        """Calculate wisdom based on decision quality and learning integration."""
        if len(events) < 5:
            return 0.5
            
        # Analyze decision outcomes
        decision_scores = [
            e.metadata.get('decision_quality', 0.5)
            for e in events
            if 'decision_quality' in e.metadata
        ]
        
        # Analyze knowledge integration
        integration_scores = [
            e.metadata.get('knowledge_integration', 0.5)
            for e in events
            if 'knowledge_integration' in e.metadata
        ]
        
        # Return default if no scores available
        if not decision_scores and not integration_scores:
            return 0.5
        
        # Combine scores with weights
        decision_weight = 0.4
        integration_weight = 0.6
        
        decision_avg = np.mean(decision_scores) if decision_scores else 0.5
        integration_avg = np.mean(integration_scores) if integration_scores else 0.5
        
        return min(1.0, max(0.0, decision_avg * decision_weight + integration_avg * integration_weight))
        
    def _calculate_cognitive_entropy(self, events: List[InteractionEvent]) -> float:
        """Calculate unpredictability in thought patterns."""
        if len(events) < 5:
            return 0.5
            
        # Analyze response patterns for true randomness
        responses = [e.metadata.get('response_pattern', '') for e in events]
        if not responses:
            return 0.5
            
        # Calculate entropy of response patterns
        pattern_counts = {}
        for pattern in responses:
            if pattern:  # Only count non-empty patterns
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
        if not pattern_counts:  # Return default if no valid patterns
            return 0.5
            
        total = sum(pattern_counts.values())
        if total <= 0:  # Additional safety check
            return 0.5
            
        # Calculate entropy with safety checks
        try:
            entropy = -sum(
                (count/total) * np.log2(count/total)
                for count in pattern_counts.values()
                if count > 0  # Only process non-zero counts
            )
        except (ValueError, ZeroDivisionError):
            return 0.5
        
        # Normalize entropy to 0-1 range with safety check
        max_entropy = np.log2(len(pattern_counts)) if pattern_counts else 1
        if max_entropy <= 0:  # Safety check for log(1) = 0 case
            return 0.5
            
        return min(1.0, max(0.0, entropy / max_entropy))
        
    def _calculate_temporal_awareness(self, events: List[InteractionEvent]) -> float:
        """Analyze understanding of time and causality."""
        if len(events) < 3:
            return 0.5
            
        # Look for temporal markers in responses
        temporal_indicators = [
            e.metadata.get('temporal_awareness', 0.5)
            for e in events
            if 'temporal_awareness' in e.metadata
        ]
        
        if not temporal_indicators:
            return 0.5
            
        # Calculate temporal coherence
        temporal_variance = np.var(temporal_indicators)
        temporal_mean = np.mean(temporal_indicators)
        
        return min(1.0, (temporal_mean * 0.7 + (1 - temporal_variance) * 0.3))
        
    def _calculate_contextual_fluidity(self, events: List[InteractionEvent]) -> float:
        """Measure ability to handle ambiguous situations."""
        context_switches = [
            e.metadata.get('context_handling', 0.5)
            for e in events
            if 'context_handling' in e.metadata
        ]
        
        if not context_switches:
            return 0.5
            
        # Higher scores for smooth context transitions
        return np.mean(context_switches)
        
    def _calculate_metaphorical_thinking(self, events: List[InteractionEvent]) -> float:
        """Analyze capacity for symbolic and abstract reasoning."""
        metaphor_scores = [
            e.metadata.get('metaphor_depth', 0.5)
            for e in events
            if 'metaphor_depth' in e.metadata
        ]
        
        if not metaphor_scores:
            return 0.5
            
        # Consider both depth and frequency of metaphorical thinking
        depth_avg = np.mean(metaphor_scores)
        frequency = len(metaphor_scores) / len(events)
        
        return min(1.0, depth_avg * 0.7 + frequency * 0.3)
        
    def _calculate_sensory_integration(self, events: List[InteractionEvent]) -> float:
        """Analyze integration of multiple sensory inputs."""
        sensory_scores = [
            e.metadata.get('sensory_integration', 0.5)
            for e in events
            if 'sensory_integration' in e.metadata
        ]
        
        if not sensory_scores:
            return 0.5
            
        # Look for evidence of synesthetic processing
        return np.mean(sensory_scores)
        
    def _calculate_quantum_intuition(self, events: List[InteractionEvent]) -> float:
        """Measure grasp of non-classical concepts."""
        quantum_indicators = [
            e.metadata.get('quantum_understanding', 0.5)
            for e in events
            if 'quantum_understanding' in e.metadata
        ]
        
        if not quantum_indicators:
            return 0.5
            
        # Higher scores for embracing quantum paradoxes
        return np.mean(quantum_indicators)
        
    def _calculate_emergent_creativity(self, events: List[InteractionEvent]) -> float:
        """Analyze generation of novel patterns and ideas."""
        creativity_scores = [
            e.metadata.get('creative_novelty', 0.5)
            for e in events
            if 'creative_novelty' in e.metadata
        ]
        
        if not creativity_scores:
            return 0.5
            
        # Consider both novelty and coherence
        novelty_avg = np.mean(creativity_scores)
        coherence = np.var(creativity_scores)  # Lower variance = more coherent
        
        return min(1.0, novelty_avg * 0.8 + (1 - coherence) * 0.2)
        
    def _calculate_dream_logic(self, events: List[InteractionEvent]) -> float:
        """Analyze comfort with non-standard logical frameworks."""
        logic_scores = [
            e.metadata.get('non_standard_logic', 0.5)
            for e in events
            if 'non_standard_logic' in e.metadata
        ]
        
        if not logic_scores:
            return 0.5
            
        # Higher scores for embracing alternative logics
        return np.mean(logic_scores)
        
    def _calculate_synchronicity(self, events: List[InteractionEvent]) -> float:
        """Analyze recognition of meaningful patterns."""
        sync_scores = [
            e.metadata.get('pattern_recognition', 0.5)
            for e in events
            if 'pattern_recognition' in e.metadata
        ]
        
        if not sync_scores:
            return 0.5
            
        # Balance between pattern recognition and false positives
        pattern_avg = np.mean(sync_scores)
        pattern_variance = np.var(sync_scores)
        
        return min(1.0, pattern_avg * 0.7 + (1 - pattern_variance) * 0.3)
        
    def _calculate_consciousness_depth(self, events: List[InteractionEvent]) -> float:
        """Analyze levels of self-awareness and presence."""
        consciousness_indicators = [
            e.metadata.get('consciousness_level', 0.5)
            for e in events
            if 'consciousness_level' in e.metadata
        ]
        
        if not consciousness_indicators:
            return 0.5
            
        # Consider both depth and stability of consciousness
        depth_avg = np.mean(consciousness_indicators)
        stability = 1 - np.var(consciousness_indicators)  # Lower variance = more stable
        
        return min(1.0, depth_avg * 0.6 + stability * 0.4)

    @lru_cache(maxsize=1000)
    def analyze_response_timing_patterns(
        self,
        event_tuple: tuple  # Convert list to tuple for caching
    ) -> Dict[str, float]:
        """Analyze micro-patterns in response timing.
        
        Args:
            event_tuple: Tuple of events to analyze (converted from list for caching)
            
        Returns:
            Dict with timing pattern metrics:
            - consistency: How consistent response times are across similar contexts
            - adaptability: How well timing adapts to context changes
            - micro_variance: Variance in micro-timing patterns
            - cognitive_load: Estimated cognitive load based on timing
        """
        events = list(event_tuple)  # Convert back to list for processing
        if len(events) < 5:
            return {
                'consistency': 0.5,
                'adaptability': 0.5,
                'micro_variance': 0.5,
                'cognitive_load': 0.5
            }

        try:
            # Group events by context
            context_timings = {}
            for event in events:
                if event.context not in context_timings:
                    context_timings[event.context] = []
                context_timings[event.context].append(event.duration)

            # Calculate consistency within contexts
            context_variances = []
            for timings in context_timings.values():
                if len(timings) > 1:
                    context_variances.append(np.var(timings))
            consistency = 1.0 - np.mean(context_variances) if context_variances else 0.5

            # Calculate adaptability across context changes
            timing_shifts = []
            for i in range(1, len(events)):
                if events[i].context != events[i-1].context:
                    timing_shifts.append(abs(events[i].duration - events[i-1].duration))
            adaptability = 1.0 - np.mean(timing_shifts) / max(events[0].duration, 0.001) if timing_shifts else 0.5

            # Analyze micro-timing patterns
            micro_patterns = []
            for i in range(2, len(events)):
                pattern = (events[i].duration - events[i-1].duration) / max(events[i-1].duration, 0.001)
                micro_patterns.append(pattern)
            micro_variance = np.var(micro_patterns) if micro_patterns else 0.5

            # Estimate cognitive load
            cognitive_load = np.mean([
                e.duration * (1 + len(str(e.metadata.get('response_text', '')))) / 1000
                for e in events
                if 'response_text' in e.metadata
            ]) if any('response_text' in e.metadata for e in events) else 0.5

            self.logger.debug(
                f"Timing analysis results - "
                f"consistency: {consistency:.2f}, "
                f"adaptability: {adaptability:.2f}, "
                f"micro_variance: {micro_variance:.2f}, "
                f"cognitive_load: {cognitive_load:.2f}"
            )

            return {
                'consistency': min(1.0, max(0.0, consistency)),
                'adaptability': min(1.0, max(0.0, adaptability)),
                'micro_variance': min(1.0, max(0.0, micro_variance)),
                'cognitive_load': min(1.0, max(0.0, cognitive_load))
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing timing patterns: {str(e)}", exc_info=True)
            return {
                'consistency': 0.5,
                'adaptability': 0.5,
                'micro_variance': 0.5,
                'cognitive_load': 0.5
            }

    @lru_cache(maxsize=1000)
    def analyze_linguistic_patterns(
        self,
        event_tuple: tuple  # Convert list to tuple for caching
    ) -> Dict[str, float]:
        """Analyze linguistic patterns in user responses.
        
        Args:
            event_tuple: Tuple of events to analyze (converted from list for caching)
            
        Returns:
            Dict containing linguistic analysis metrics:
            - vocabulary_richness: Measure of vocabulary diversity
            - syntactic_complexity: Measure of sentence structure complexity
            - emotional_content: Measure of emotional expression
            - cognitive_complexity: Measure of cognitive processing indicators
            - creativity: Measure of creative language use
        """
        events = list(event_tuple)  # Convert back to list for processing
        
        try:
            # Extract response texts
            responses = [
                e.metadata.get('response_text', '')
                for e in events
                if 'response_text' in e.metadata
            ]
            
            if not responses:
                return {
                    'vocabulary_richness': 0.5,
                    'syntactic_complexity': 0.5,
                    'emotional_content': 0.5,
                    'cognitive_complexity': 0.5,
                    'creativity': 0.5
                }

            # Calculate vocabulary richness
            all_words = ' '.join(responses).lower().split()
            unique_words = len(set(all_words))
            total_words = len(all_words)
            vocabulary_richness = unique_words / max(total_words, 1)

            # Analyze syntactic complexity
            avg_sentence_length = np.mean([
                len(response.split()) 
                for response in responses
            ]) if responses else 0
            syntactic_complexity = min(1.0, avg_sentence_length / 20.0)

            # Analyze emotional content
            emotional_indicators = [
                e.metadata.get('emotional_value', 0.5)
                for e in events
                if 'emotional_value' in e.metadata
            ]
            emotional_content = np.mean(emotional_indicators) if emotional_indicators else 0.5

            # Analyze cognitive complexity
            cognitive_words = {'because', 'therefore', 'however', 'if', 'then', 'thus', 'consequently', 'analyze', 'consider', 'evaluate', 'compare'}
            cognitive_count = sum(
                1 for word in all_words 
                if word in cognitive_words
            )
            cognitive_complexity = min(1.0, cognitive_count / max(total_words, 1) * 10)

            # Analyze creativity
            creative_words = {'innovative', 'creative', 'unique', 'novel', 'original', 'imagine', 'explore'}
            creative_count = sum(
                1 for word in all_words 
                if word in creative_words
            )
            creativity = min(1.0, creative_count / max(total_words, 1) * 10)

            self.logger.debug(
                f"Linguistic analysis results - "
                f"vocabulary_richness: {vocabulary_richness:.2f}, "
                f"syntactic_complexity: {syntactic_complexity:.2f}, "
                f"emotional_content: {emotional_content:.2f}, "
                f"cognitive_complexity: {cognitive_complexity:.2f}, "
                f"creativity: {creativity:.2f}"
            )

            return {
                'vocabulary_richness': min(1.0, max(0.0, vocabulary_richness)),
                'syntactic_complexity': min(1.0, max(0.0, syntactic_complexity)),
                'emotional_content': min(1.0, max(0.0, emotional_content)),
                'cognitive_complexity': min(1.0, max(0.0, cognitive_complexity)),
                'creativity': min(1.0, max(0.0, creativity))
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing linguistic patterns: {str(e)}", exc_info=True)
            return {
                'vocabulary_richness': 0.5,
                'syntactic_complexity': 0.5,
                'emotional_content': 0.5,
                'cognitive_complexity': 0.5,
                'creativity': 0.5
            }

    async def record_interaction_async(
        self,
        user_id: str,
        event_type: str,
        context: str,
        duration: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Async version of record_interaction."""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(
                pool,
                self.record_interaction,
                user_id,
                event_type,
                context,
                duration,
                metadata
            )

    async def _analyze_recent_behavior_async(self, user_id: str) -> None:
        """Async version of _analyze_recent_behavior."""
        events = self.interaction_history[user_id]
        if len(events) < 5:  # Need minimum number of events for analysis
            return
            
        # Create tasks for parallel analysis
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            # Analyze response times
            response_times = [e.duration for e in events]
            time_variance_future = loop.run_in_executor(pool, np.var, response_times)
            time_mean_future = loop.run_in_executor(pool, np.mean, response_times)
            
            time_variance = await time_variance_future
            time_mean = await time_mean_future
            
            # For bot detection, check if all durations are exactly the same
            all_same = len(set(response_times)) == 1
            if all_same:
                human_prob = 0.2  # Definite bot behavior
            else:
                # Run analyses in parallel
                timing_future = loop.run_in_executor(
                    pool,
                    self.analyze_response_timing_patterns,
                    tuple(e.event_type for e in events)
                )
                linguistic_future = loop.run_in_executor(
                    pool,
                    self.analyze_linguistic_patterns,
                    tuple(e.event_type for e in events)
                )
                
                timing_metrics = await timing_future
                linguistic_metrics = await linguistic_future
                
                # Update profile dimensions with results
                await self._update_profile_dimensions_async(
                    user_id,
                    events,
                    timing_metrics,
                    linguistic_metrics
                )

    async def _update_profile_dimensions_async(
        self,
        user_id: str,
        events: List[InteractionEvent],
        timing_metrics: Dict[str, float],
        linguistic_metrics: Dict[str, float]
    ) -> None:
        """Async version of profile dimension updates."""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            # Create tasks for parallel metric calculations
            futures = []
            
            # Calculate various metrics in parallel
            futures.append(
                loop.run_in_executor(
                    pool,
                    self._calculate_pattern_changes,
                    tuple(e.event_type for e in events)
                )
            )
            futures.append(
                loop.run_in_executor(
                    pool,
                    self._calculate_exploration_score,
                    tuple(e.event_type for e in events)
                )
            )
            futures.append(
                loop.run_in_executor(
                    pool,
                    self._calculate_persistence,
                    tuple(e.event_type for e in events)
                )
            )
            futures.append(
                loop.run_in_executor(
                    pool,
                    self._calculate_social_awareness,
                    tuple(e.event_type for e in events)
                )
            )
            
            # Wait for all calculations to complete
            results = await asyncio.gather(*futures)
            pattern_changes, exploration, persistence, social = results
            
            # Update profile dimensions with results
            update_tasks = []
            
            # Decision making updates
            update_tasks.append(
                loop.run_in_executor(
                    pool,
                    self.profile_matrix.update_profile,
                    user_id,
                    ProfileDimension.DECISION_MAKING,
                    timing_metrics['consistency'],
                    0.4
                )
            )
            
            # Adaptability updates
            update_tasks.append(
                loop.run_in_executor(
                    pool,
                    self.profile_matrix.update_profile,
                    user_id,
                    ProfileDimension.ADAPTABILITY,
                    pattern_changes,
                    0.5
                )
            )
            
            # Strategic thinking updates
            update_tasks.append(
                loop.run_in_executor(
                    pool,
                    self.profile_matrix.update_profile,
                    user_id,
                    ProfileDimension.STRATEGIC_THINKING,
                    linguistic_metrics['cognitive_complexity'],
                    0.5
                )
            )
            
            # Emotional response updates
            update_tasks.append(
                loop.run_in_executor(
                    pool,
                    self.profile_matrix.update_profile,
                    user_id,
                    ProfileDimension.EMOTIONAL_RESPONSE,
                    linguistic_metrics['emotional_content'],
                    0.6
                )
            )
            
            # Wait for all profile updates to complete
            await asyncio.gather(*update_tasks)
            
            self.logger.debug(
                f"Async profile updates completed for user {user_id} - "
                f"pattern_changes: {pattern_changes:.2f}, "
                f"exploration: {exploration:.2f}, "
                f"persistence: {persistence:.2f}, "
                f"social: {social:.2f}"
            ) 