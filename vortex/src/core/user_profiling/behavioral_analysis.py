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
        
        # Analyze timing patterns
        timing_metrics = self.analyze_response_timing_patterns(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.DECISION_MAKING,
            timing_metrics['consistency'],
            confidence=0.4
        )
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.ADAPTABILITY,
            timing_metrics['adaptability'],
            confidence=0.4
        )
        
        # Analyze linguistic patterns
        linguistic_metrics = self.analyze_linguistic_patterns(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.STRATEGIC_THINKING,
            linguistic_metrics['cognitive_indicators'],
            confidence=0.5
        )
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.EMOTIONAL_RESPONSE,
            linguistic_metrics['emotional_content'],
            confidence=0.6
        )
        
        # Analyze decision making from interaction patterns
        decision_speed = np.mean([e.duration for e in recent_events])
        decision_consistency = self._calculate_pattern_variance(recent_events)
        
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
            for e in recent_events
            if 'emotional_value' in e.metadata
        ]
        
        if emotional_responses:
            emotional_variance = np.var(emotional_responses)
            emotional_depth = (
                emotional_variance * 0.3 +
                linguistic_metrics['emotional_content'] * 0.7
            )
            self.profile_matrix.update_profile(
                user_id,
                ProfileDimension.EMOTIONAL_RESPONSE,
                emotional_depth,
                confidence=0.6
            )
            
        # Analyze adaptability with combined metrics
        adaptability_score = (
            timing_metrics['adaptability'] * 0.4 +
            timing_metrics['micro_variance'] * 0.3 +
            linguistic_metrics['vocabulary_richness'] * 0.3
        )
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.ADAPTABILITY,
            adaptability_score,
            confidence=0.5
        )
        
        # Analyze curiosity through linguistic and timing patterns
        exploration_score = self._calculate_exploration_score(recent_events)
        curiosity_score = (
            exploration_score * 0.4 +
            linguistic_metrics['vocabulary_richness'] * 0.3 +
            timing_metrics['micro_variance'] * 0.3
        )
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.CURIOSITY,
            curiosity_score,
            confidence=0.4
        )
        
        # Analyze persistence
        persistence_score = self._calculate_persistence(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.PERSISTENCE,
            persistence_score,
            confidence=0.6
        )
        
        # Analyze social awareness
        social_score = self._calculate_social_awareness(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.SOCIAL_AWARENESS,
            social_score,
            confidence=0.5
        )
        
        # Analyze self-reflection
        reflection_score = self._calculate_reflection_score(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.SELF_REFLECTION,
            reflection_score,
            confidence=0.4
        )
        
        # Calculate wisdom score based on multiple factors
        wisdom_score = self._calculate_wisdom_score(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.WISDOM,
            wisdom_score,
            confidence=0.3
        )
        
        # Analyze cognitive entropy
        entropy_score = self._calculate_cognitive_entropy(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.COGNITIVE_ENTROPY,
            entropy_score,
            confidence=0.7
        )
        
        # Analyze temporal awareness
        temporal_score = self._calculate_temporal_awareness(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.TEMPORAL_AWARENESS,
            temporal_score,
            confidence=0.6
        )
        
        # Analyze contextual fluidity
        fluidity_score = self._calculate_contextual_fluidity(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.CONTEXTUAL_FLUIDITY,
            fluidity_score,
            confidence=0.5
        )
        
        # Analyze metaphorical thinking
        metaphor_score = self._calculate_metaphorical_thinking(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.METAPHORICAL_THINKING,
            metaphor_score,
            confidence=0.6
        )
        
        # Analyze sensory integration
        sensory_score = self._calculate_sensory_integration(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.SENSORY_INTEGRATION,
            sensory_score,
            confidence=0.5
        )
        
        # Analyze quantum intuition
        quantum_score = self._calculate_quantum_intuition(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.QUANTUM_INTUITION,
            quantum_score,
            confidence=0.4
        )
        
        # Analyze emergent creativity
        emergent_score = self._calculate_emergent_creativity(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.EMERGENT_CREATIVITY,
            emergent_score,
            confidence=0.6
        )
        
        # Analyze dream logic
        dream_logic_score = self._calculate_dream_logic(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.DREAM_LOGIC,
            dream_logic_score,
            confidence=0.5
        )
        
        # Analyze synchronicity awareness
        sync_score = self._calculate_synchronicity(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.SYNCHRONICITY_AWARENESS,
            sync_score,
            confidence=0.4
        )
        
        # Analyze consciousness depth
        consciousness_score = self._calculate_consciousness_depth(recent_events)
        self.profile_matrix.update_profile(
            user_id,
            ProfileDimension.CONSCIOUSNESS_DEPTH,
            consciousness_score,
            confidence=0.5
        )
        
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

    def analyze_response_timing_patterns(self, events: List[InteractionEvent]) -> Dict[str, float]:
        """Analyze micro-patterns in response timing.
        
        Returns:
            Dict with timing pattern metrics:
            - consistency: How consistent response times are across similar contexts
            - adaptability: How well timing adapts to context changes
            - micro_variance: Variance in micro-timing patterns
            - cognitive_load: Estimated cognitive load based on timing
        """
        if len(events) < 5:
            return {
                'consistency': 0.5,
                'adaptability': 0.5,
                'micro_variance': 0.5,
                'cognitive_load': 0.5
            }

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
            e.duration * (1 + len(e.metadata.get('response_text', ''))) / 1000
            for e in events
            if 'response_text' in e.metadata
        ]) if any('response_text' in e.metadata for e in events) else 0.5

        return {
            'consistency': min(1.0, max(0.0, consistency)),
            'adaptability': min(1.0, max(0.0, adaptability)),
            'micro_variance': min(1.0, max(0.0, micro_variance)),
            'cognitive_load': min(1.0, max(0.0, cognitive_load))
        }

    def analyze_linguistic_patterns(self, events: List[InteractionEvent]) -> Dict[str, float]:
        """Analyze linguistic patterns in user responses.
        
        Returns:
            Dict with linguistic metrics:
            - vocabulary_richness: Measure of vocabulary diversity
            - syntactic_complexity: Complexity of sentence structures
            - emotional_content: Density of emotional language
            - cognitive_indicators: Presence of analytical thinking markers
        """
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
                'cognitive_indicators': 0.5
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
        syntactic_complexity = min(1.0, avg_sentence_length / 20.0)  # Normalize to 0-1

        # Analyze emotional content
        emotional_indicators = [
            e.metadata.get('emotional_value', 0.5)
            for e in events
            if 'emotional_value' in e.metadata
        ]
        emotional_content = np.mean(emotional_indicators) if emotional_indicators else 0.5

        # Analyze cognitive indicators
        cognitive_words = {'because', 'therefore', 'however', 'if', 'then', 'thus', 'consequently'}
        cognitive_count = sum(
            1 for word in all_words 
            if word in cognitive_words
        )
        cognitive_indicators = min(1.0, cognitive_count / max(total_words, 1) * 10)

        return {
            'vocabulary_richness': min(1.0, max(0.0, vocabulary_richness)),
            'syntactic_complexity': min(1.0, max(0.0, syntactic_complexity)),
            'emotional_content': min(1.0, max(0.0, emotional_content)),
            'cognitive_indicators': min(1.0, max(0.0, cognitive_indicators))
        } 