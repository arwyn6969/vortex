from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from scipy.stats import entropy, zscore, ks_2samp, anderson, shapiro, spearmanr
from scipy.spatial.distance import mahalanobis
from scipy.signal import find_peaks
from statsmodels.tsa.stattools import adfuller, acf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
import ruptures  # For change point detection
import joblib
from datetime import datetime, timedelta
import pandas as pd
from ..redis_config import RedisConfig
from .. import redis_service

class ProfileDimension(Enum):
    EMPATHY = "empathy"
    DECISION_MAKING = "decision_making"
    EMOTIONAL_RESPONSE = "emotional_response"
    CREATIVITY = "creativity"
    RISK_TOLERANCE = "risk_tolerance"
    STRATEGIC_THINKING = "strategic_thinking"
    MORAL_ALIGNMENT = "moral_alignment"
    ADAPTABILITY = "adaptability"  # How well they adapt to new situations
    CULTURAL_AWARENESS = "cultural_awareness"  # Respect and understanding of cultures
    RESILIENCE = "resilience"  # Ability to recover from challenges
    CURIOSITY = "curiosity"  # Drive to explore and learn
    PERSISTENCE = "persistence"  # Determination in face of challenges
    SOCIAL_AWARENESS = "social_awareness"  # Understanding of social dynamics
    SELF_REFLECTION = "self_reflection"  # Capacity for introspection
    WISDOM = "wisdom"  # Integration of knowledge and experience
    COGNITIVE_ENTROPY = "cognitive_entropy"  # Measure of thought pattern randomness/unpredictability
    TEMPORAL_AWARENESS = "temporal_awareness"  # Understanding and relation to time
    CONTEXTUAL_FLUIDITY = "contextual_fluidity"  # Ability to handle ambiguous/paradoxical situations
    METAPHORICAL_THINKING = "metaphorical_thinking"  # Capacity for abstract/symbolic reasoning
    SENSORY_INTEGRATION = "sensory_integration"  # How well physical/emotional experiences are processed
    QUANTUM_INTUITION = "quantum_intuition"  # Ability to grasp non-linear/quantum concepts
    EMERGENT_CREATIVITY = "emergent_creativity"  # Spontaneous generation of truly novel ideas
    DREAM_LOGIC = "dream_logic"  # Ability to work with non-standard logical frameworks
    SYNCHRONICITY_AWARENESS = "synchronicity_awareness"  # Recognition of meaningful coincidences
    CONSCIOUSNESS_DEPTH = "consciousness_depth"  # Levels of self-awareness and presence

@dataclass
class BehavioralProfile:
    """Represents a user's behavioral profile with various dimensions."""
    user_id: str
    dimensions: Dict[ProfileDimension, float]
    confidence_scores: Dict[ProfileDimension, float]
    is_human_probability: float
    last_updated: float  # timestamp
    interaction_count: int
    dimension_correlations: Dict[Tuple[ProfileDimension, ProfileDimension], float] = None
    feature_importance: Dict[ProfileDimension, float] = None

    def to_dict(self) -> dict:
        """Convert BehavioralProfile to a JSON-serializable dict."""
        return {
            'user_id': self.user_id,
            'dimensions': {dim.value: val for dim, val in self.dimensions.items()},
            'confidence_scores': {dim.value: val for dim, val in self.confidence_scores.items()},
            'is_human_probability': self.is_human_probability,
            'last_updated': self.last_updated,
            'interaction_count': self.interaction_count,
            'dimension_correlations': {f"{dim1.value},{dim2.value}": corr for (dim1, dim2), corr in (self.dimension_correlations or {}).items()},
            'feature_importance': {dim.value: val for dim, val in (self.feature_importance or {}).items()}
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BehavioralProfile':
        """Create BehavioralProfile from a dict."""
        dimensions = {ProfileDimension(k): v for k, v in data['dimensions'].items()}
        confidence_scores = {ProfileDimension(k): v for k, v in data['confidence_scores'].items()}
        dimension_correlations = None
        if data.get('dimension_correlations') is not None:
            dimension_correlations = {}
            for key, corr in data['dimension_correlations'].items():
                dim1_str, dim2_str = key.split(',', 1)
                dimension_correlations[(ProfileDimension(dim1_str), ProfileDimension(dim2_str))] = corr
        feature_importance = None
        if data.get('feature_importance') is not None:
            feature_importance = {ProfileDimension(k): v for k, v in data['feature_importance'].items()}
        return cls(
            user_id=data['user_id'],
            dimensions=dimensions,
            confidence_scores=confidence_scores,
            is_human_probability=data['is_human_probability'],
            last_updated=data['last_updated'],
            interaction_count=data['interaction_count'],
            dimension_correlations=dimension_correlations,
            feature_importance=feature_importance
        )

class ProfileMatrix:
    """Manages behavioral profiling and analysis for users with ML enhancement."""
    
    DECAY_FACTOR = 0.95  # Decay factor for historical data
    MAX_HISTORY_SIZE = 100  # Maximum number of historical states to keep
    CORRELATION_THRESHOLD = 0.7  # Threshold for significant dimension correlations
    MIN_HISTORY_FOR_ADVANCED = 20  # Minimum history for advanced anomaly detection
    
    def __init__(self):
        self.profiles: Dict[str, BehavioralProfile] = {}
        self.scaler = StandardScaler()
        self.robust_scaler = RobustScaler()
        
        # Multiple anomaly detectors for ensemble approach
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=200
        )
        self.local_outlier_factor = LocalOutlierFactor(
            contamination=0.1,
            novelty=True,
            n_neighbors=20
        )
        self.robust_covariance = EllipticEnvelope(
            contamination=0.1,
            random_state=42,
            support_fraction=0.8
        )
        self.one_class_svm = OneClassSVM(
            kernel='rbf',
            nu=0.1,
            gamma='scale'
        )
        
        self.pca = PCA(n_components=0.95)
        self.pattern_history: Dict[str, List[Dict[ProfileDimension, float]]] = {}
        self.dimension_groups: List[Set[ProfileDimension]] = self._initialize_dimension_groups()
        self.covariance_matrix: Optional[np.ndarray] = None
        self.mean_vector: Optional[np.ndarray] = None
        
        # Add new attributes for adaptive grouping and prediction
        self.dimension_clusters: Dict[str, List[Set[ProfileDimension]]] = {}
        self.prediction_models: Dict[str, Dict[ProfileDimension, Prophet]] = {}
        self.last_cluster_update: Dict[str, datetime] = {}
        self.CLUSTER_UPDATE_INTERVAL = timedelta(hours=1)  # Update clusters hourly
        
    def _initialize_dimension_groups(self) -> List[Set[ProfileDimension]]:
        """Initialize related dimension groups for cross-dimensional analysis."""
        return [
            {ProfileDimension.EMPATHY, ProfileDimension.SOCIAL_AWARENESS, ProfileDimension.MORAL_ALIGNMENT},
            {ProfileDimension.CREATIVITY, ProfileDimension.EMERGENT_CREATIVITY, ProfileDimension.METAPHORICAL_THINKING},
            {ProfileDimension.WISDOM, ProfileDimension.SELF_REFLECTION, ProfileDimension.CONSCIOUSNESS_DEPTH},
            {ProfileDimension.QUANTUM_INTUITION, ProfileDimension.DREAM_LOGIC, ProfileDimension.SYNCHRONICITY_AWARENESS},
            {ProfileDimension.CONTEXTUAL_FLUIDITY, ProfileDimension.ADAPTABILITY, ProfileDimension.TEMPORAL_AWARENESS}
        ]

    def create_profile(self, user_id: str) -> BehavioralProfile:
        """Initialize a new behavioral profile for a user."""
        profile = BehavioralProfile(
            user_id=user_id,
            dimensions={dim: 0.5 for dim in ProfileDimension},
            confidence_scores={dim: 0.1 for dim in ProfileDimension},  # Start with low confidence
            is_human_probability=0.5,
            last_updated=datetime.now().timestamp(),
            interaction_count=0
        )
        self.profiles[user_id] = profile
        self.pattern_history[user_id] = []
        return profile

    def update_profile(self, user_id: str, updates: Dict[ProfileDimension, float]) -> None:
        """Update multiple dimensions of a user's profile at once."""
        if user_id not in self.profiles:
            self.create_profile(user_id)
            
        profile = self.profiles[user_id]
        
        # Update each dimension
        for dimension, value in updates.items():
            # Ensure value is within bounds
            value = max(0.0, min(1.0, value))
            
            # Calculate confidence based on cross-dimensional analysis
            confidence = self._calculate_cross_dimensional_confidence(
                user_id, dimension, value
            )
            
            # Update the dimension with the new value
            current_conf = profile.confidence_scores[dimension]
            new_conf = current_conf + confidence
            
            # Weighted average based on confidence
            current_val = profile.dimensions[dimension]
            profile.dimensions[dimension] = (
                (current_val * current_conf + value * confidence) / new_conf
            )
            profile.confidence_scores[dimension] = new_conf
            
        # Update metadata
        profile.interaction_count += 1
        profile.last_updated = datetime.now().timestamp()
        
        # Store state in pattern history
        if user_id not in self.pattern_history:
            self.pattern_history[user_id] = []
            
        # Add current state to history
        current_state = {dim: profile.dimensions[dim] for dim in ProfileDimension}
        self.pattern_history[user_id].append(current_state)
        
        # Trim history if needed
        if len(self.pattern_history[user_id]) > self.MAX_HISTORY_SIZE:
            self.pattern_history[user_id] = self.pattern_history[user_id][-self.MAX_HISTORY_SIZE:]
            
        # Apply temporal decay to historical data
        self._apply_temporal_decay(user_id)
        
        # Update correlations and feature importance
        self._update_dimension_correlations(user_id)
        self._update_feature_importance(user_id)
        
        # Update human probability using ML analysis
        self._update_human_probability_ml(user_id)
        
        # Trigger adaptive dimension grouping
        self._update_adaptive_dimension_groups(user_id)
        
        # Update prediction models
        for dimension in updates:
            if user_id in self.prediction_models and dimension in self.prediction_models[user_id]:
                # Clear the model to force retraining with new data
                self.prediction_models[user_id][dimension] = Prophet(
                    changepoint_prior_scale=0.05,
                    seasonality_prior_scale=0.1,
                    seasonality_mode='multiplicative'
                )

    def _apply_temporal_decay(self, user_id: str) -> None:
        """Apply decay factor to historical data."""
        history = self.pattern_history[user_id]
        for state in history:
            for dim in ProfileDimension:
                state[dim] *= self.DECAY_FACTOR

    def _calculate_cross_dimensional_confidence(
        self,
        user_id: str,
        dimension: ProfileDimension,
        value: float
    ) -> float:
        """Calculate confidence based on related dimensions."""
        profile = self.profiles[user_id]
        
        # Find the dimension group containing the target dimension
        related_dims = set()
        for group in self.dimension_groups:
            if dimension in group:
                related_dims = group
                break
        
        if not related_dims:
            return 1.0
        
        # Calculate consistency with related dimensions
        related_values = [profile.dimensions[dim] for dim in related_dims if dim != dimension]
        if not related_values:
            return 1.0
            
        # Calculate how well the new value fits with related dimensions
        mean_related = np.mean(related_values)
        std_related = np.std(related_values) if len(related_values) > 1 else 1.0
        
        # Higher confidence if value is consistent with related dimensions
        z_score = abs(value - mean_related) / std_related if std_related > 0 else 0
        return 1.0 / (1.0 + z_score)

    def _update_dimension_correlations(self, user_id: str) -> None:
        """Update correlations between dimensions."""
        history = self.pattern_history[user_id]
        if len(history) < 5:
            return
            
        profile = self.profiles[user_id]
        correlations = {}
        
        # Calculate correlations between all dimension pairs
        dimensions = list(ProfileDimension)
        for i, dim1 in enumerate(dimensions):
            for dim2 in dimensions[i+1:]:
                values1 = [state[dim1] for state in history]
                values2 = [state[dim2] for state in history]
                corr = np.corrcoef(values1, values2)[0, 1]
                if abs(corr) >= self.CORRELATION_THRESHOLD:
                    correlations[(dim1, dim2)] = corr
        
        profile.dimension_correlations = correlations

    def _update_feature_importance(self, user_id: str) -> None:
        """Update feature importance using PCA."""
        history = self.pattern_history[user_id]
        if len(history) < 5:
            return
            
        profile = self.profiles[user_id]
        X = np.array([list(state.values()) for state in history])
        X = self.scaler.fit_transform(X)
        
        # Fit PCA and get feature importance
        self.pca.fit(X)
        components = np.abs(self.pca.components_)
        importance = np.sum(components, axis=0) / np.sum(components)
        
        profile.feature_importance = {
            dim: imp for dim, imp in zip(ProfileDimension, importance)
        }

    def _calculate_temporal_confidence(
        self,
        user_id: str,
        dimension: ProfileDimension,
        value: float
    ) -> float:
        """Calculate confidence based on temporal consistency."""
        history = self.pattern_history[user_id]
        if len(history) < 2:
            return 1.0
            
        recent_values = [state[dimension] for state in history[-5:]]
        std_dev = np.std(recent_values) if len(recent_values) > 1 else 1.0
        
        # Higher confidence for consistent behavior
        return 1.0 / (1.0 + std_dev)

    def _detect_pattern_anomalies(
        self,
        user_id: str,
        dimension: ProfileDimension,
        value: float
    ) -> float:
        """Enhanced anomaly detection using multiple methods and ensemble scoring."""
        history = self.pattern_history[user_id]
        if len(history) < 10:
            return 1.0
            
        # Prepare data
        X = np.array([list(state.values()) for state in history[-20:]])
        X_current = np.array(list(history[-1].values())).reshape(1, -1)
        
        # Basic standardization
        X_scaled = self.scaler.fit_transform(X)
        X_current_scaled = self.scaler.transform(X_current)
        
        # Robust standardization for outlier-resistant scaling
        X_robust = self.robust_scaler.fit_transform(X)
        X_current_robust = self.robust_scaler.transform(X_current)
        
        scores = []
        
        # 1. Isolation Forest Score
        if len(history) >= self.MIN_HISTORY_FOR_ADVANCED:
            self.isolation_forest.fit(X_scaled)
            if_score = self.isolation_forest.score_samples(X_current_scaled)[0]
            scores.append(self._normalize_score(if_score))
        
        # 2. Local Outlier Factor Score
        if len(history) >= self.MIN_HISTORY_FOR_ADVANCED:
            self.local_outlier_factor.fit(X_robust)
            lof_score = self.local_outlier_factor.score_samples(X_current_robust)[0]
            scores.append(self._normalize_score(lof_score))
        
        # 3. Robust Covariance Score
        if len(history) >= self.MIN_HISTORY_FOR_ADVANCED:
            try:
                self.robust_covariance.fit(X_robust)
                rc_score = self.robust_covariance.score_samples(X_current_robust)[0]
                scores.append(self._normalize_score(rc_score))
            except Exception:
                # Fallback if covariance estimation fails
                pass
        
        # 4. One-Class SVM Score
        if len(history) >= self.MIN_HISTORY_FOR_ADVANCED:
            try:
                self.one_class_svm.fit(X_scaled)
                svm_score = self.one_class_svm.score_samples(X_current_scaled)[0]
                scores.append(self._normalize_score(svm_score))
            except Exception:
                # Fallback if SVM fails
                pass
        
        # 5. Statistical Anomaly Scores
        stat_scores = self._calculate_statistical_anomaly_scores(
            history, dimension, value
        )
        scores.extend(stat_scores)
        
        # Combine scores with weighted average
        # Give more weight to statistical scores when history is limited
        if len(scores) > 0:
            if len(history) < self.MIN_HISTORY_FOR_ADVANCED:
                # Weight statistical scores more heavily with limited history
                final_score = np.mean(scores)
            else:
                # Weight ML model scores more heavily with sufficient history
                ml_scores = scores[:4]  # First 4 scores are from ML models
                stat_scores = scores[4:]  # Remaining scores are statistical
                
                ml_weight = 0.7
                stat_weight = 0.3
                
                final_score = (
                    ml_weight * np.mean(ml_scores) +
                    stat_weight * np.mean(stat_scores)
                    if ml_scores else np.mean(stat_scores)
                )
            
            return max(0.1, min(1.0, final_score))
        
        return 1.0  # Default to full confidence if no scores available

    def _normalize_score(self, score: float) -> float:
        """Normalize anomaly scores to [0,1] range where 1 is normal."""
        # Convert to probability-like score where higher means more normal
        return 1.0 / (1.0 + np.exp(-score))

    def _calculate_statistical_anomaly_scores(
        self,
        history: List[Dict[ProfileDimension, float]],
        dimension: ProfileDimension,
        value: float
    ) -> List[float]:
        """Calculate statistical anomaly scores using multiple advanced methods."""
        scores = []
        
        # Extract recent values for the dimension
        recent_values = np.array([state[dimension] for state in history[-20:]])
        current_value = value
        
        if len(recent_values) < 5:
            return [1.0]  # Not enough data for advanced statistics
            
        try:
            # 1. Z-score based anomaly score (existing)
            z = abs(zscore(recent_values)[-1])
            scores.append(1.0 / (1.0 + z))
            
            # 2. Mahalanobis distance (existing, enhanced)
            X = np.array([list(state.values()) for state in history])
            if len(X) > 1:
                # Use Robust covariance estimation
                cov = self._robust_covariance_estimate(X)
                mean = np.median(X, axis=0)  # Use median for robustness
                current = np.array(list(history[-1].values()))
                
                self.covariance_matrix = cov
                self.mean_vector = mean
                
                m_dist = mahalanobis(current, mean, np.linalg.pinv(cov))
                scores.append(1.0 / (1.0 + m_dist))
            
            # 3. ARIMA-based prediction score
            if len(recent_values) >= 10:
                arima_score = self._calculate_arima_score(recent_values, current_value)
                scores.append(arima_score)
            
            # 4. Change point detection score
            change_point_score = self._calculate_change_point_score(recent_values, current_value)
            scores.append(change_point_score)
            
            # 5. Stationarity score (Augmented Dickey-Fuller test)
            adf_stat, adf_pvalue = adfuller(recent_values)[:2]
            stationarity_score = 1.0 / (1.0 + np.exp(-adf_stat))  # Higher score for more stationary
            scores.append(stationarity_score)
            
            # 6. Distribution similarity score
            if len(recent_values) >= 10:
                dist_score = self._calculate_distribution_similarity(recent_values, current_value)
                scores.append(dist_score)
            
            # 7. Autocorrelation-based score
            if len(recent_values) >= 10:
                acf_score = self._calculate_autocorrelation_score(recent_values)
                scores.append(acf_score)
            
            # 8. Peak analysis score
            peak_score = self._calculate_peak_score(recent_values, current_value)
            scores.append(peak_score)
            
            # 9. Robust regression score
            if len(recent_values) >= 5:
                reg_score = self._calculate_robust_regression_score(recent_values, current_value)
                scores.append(reg_score)
            
            # 10. Entropy change score
            entropy_score = self._calculate_entropy_change_score(recent_values, current_value)
            scores.append(entropy_score)
            
        except Exception as e:
            # Fallback to basic statistical measures if advanced methods fail
            if not scores:
                return [1.0]
        
        return scores

    def _robust_covariance_estimate(self, X: np.ndarray) -> np.ndarray:
        """Calculate robust covariance matrix using Minimum Covariance Determinant."""
        try:
            # Use median absolute deviation for robust scaling
            mad = np.median(np.abs(X - np.median(X, axis=0)), axis=0)
            X_scaled = X / (mad + 1e-6)  # Avoid division by zero
            
            # Calculate robust covariance
            cov = np.cov(X_scaled.T, aweights=self._huber_weights(X_scaled))
            return cov
        except Exception:
            # Fallback to regular covariance if robust estimation fails
            return np.cov(X.T)

    def _huber_weights(self, X: np.ndarray, k: float = 1.345) -> np.ndarray:
        """Calculate Huber weights for robust estimation."""
        # Compute Mahalanobis distances
        dists = np.sum((X - np.median(X, axis=0)) ** 2, axis=1)
        weights = np.minimum(1, k / np.sqrt(dists + 1e-6))
        return weights

    def _calculate_arima_score(
        self,
        values: np.ndarray,
        current_value: float
    ) -> float:
        """Calculate anomaly score using ARIMA prediction."""
        try:
            # Fit ARIMA model
            model = ARIMA(values[:-1], order=(1, 0, 1))
            results = model.fit()
            
            # Get prediction and confidence interval
            forecast = results.forecast(steps=1)
            pred = forecast[0]
            
            # Calculate score based on prediction error
            error = abs(current_value - pred)
            return 1.0 / (1.0 + error)
        except Exception:
            return 1.0

    def _calculate_change_point_score(
        self,
        values: np.ndarray,
        current_value: float
    ) -> float:
        """Calculate score based on change point detection."""
        try:
            # Use binary segmentation for change point detection
            model = Binseg(model="l2").fit(values.reshape(-1, 1))
            change_points = model.predict(n_bkps=3)
            
            # Check if current point is near a change point
            if change_points:
                min_dist = min(abs(len(values) - cp) for cp in change_points)
                return 1.0 / (1.0 + min_dist)
            return 1.0
        except Exception:
            return 1.0

    def _calculate_distribution_similarity(
        self,
        values: np.ndarray,
        current_value: float
    ) -> float:
        """Calculate similarity between recent and historical distributions."""
        try:
            # Split data into recent and historical
            split_idx = len(values) // 2
            historical = values[:split_idx]
            recent = values[split_idx:]
            
            # Perform Kolmogorov-Smirnov test
            ks_stat, _ = ks_2samp(historical, recent)
            
            # Calculate Anderson-Darling test
            ad_stat = anderson(recent).statistic
            
            # Combine scores
            combined_score = (1.0 / (1.0 + ks_stat) + 1.0 / (1.0 + ad_stat)) / 2
            return combined_score
        except Exception:
            return 1.0

    def _calculate_autocorrelation_score(self, values: np.ndarray) -> float:
        """Calculate score based on autocorrelation structure."""
        try:
            # Calculate autocorrelation
            acf_values = acf(values, nlags=min(10, len(values) - 1))
            
            # Score based on stability of autocorrelation
            acf_stability = 1.0 / (1.0 + np.std(acf_values))
            return acf_stability
        except Exception:
            return 1.0

    def _calculate_peak_score(
        self,
        values: np.ndarray,
        current_value: float
    ) -> float:
        """Calculate score based on peak analysis."""
        try:
            # Find peaks in the data
            peaks, _ = find_peaks(values)
            
            if len(peaks) > 0:
                # Calculate typical peak characteristics
                peak_heights = values[peaks]
                peak_mean = np.mean(peak_heights)
                peak_std = np.std(peak_heights) if len(peak_heights) > 1 else 1.0
                
                # Score based on how well current value fits peak pattern
                z_score = abs(current_value - peak_mean) / (peak_std + 1e-6)
                return 1.0 / (1.0 + z_score)
            return 1.0
        except Exception:
            return 1.0

    def _calculate_robust_regression_score(
        self,
        values: np.ndarray,
        current_value: float
    ) -> float:
        """Calculate score using robust regression prediction."""
        try:
            # Create time index
            X = np.arange(len(values)).reshape(-1, 1)
            y = values
            
            # Calculate Theil-Sen slope
            diffs = []
            for i in range(len(X)):
                for j in range(i + 1, len(X)):
                    slope = (y[j] - y[i]) / (X[j] - X[i])
                    diffs.append(slope)
            
            slope = np.median(diffs)
            intercept = np.median(y - slope * X.ravel())
            
            # Predict next value
            pred = slope * len(values) + intercept
            
            # Score based on prediction error
            error = abs(current_value - pred)
            return 1.0 / (1.0 + error)
        except Exception:
            return 1.0

    def _calculate_entropy_change_score(
        self,
        values: np.ndarray,
        current_value: float
    ) -> float:
        """Calculate score based on entropy changes."""
        try:
            # Calculate entropy of windows with and without current value
            window_size = min(10, len(values))
            
            # Entropy of recent window without current value
            recent_entropy = entropy(np.histogram(values[-window_size:], bins='auto')[0])
            
            # Entropy with current value
            with_current = np.append(values[-window_size:], current_value)
            new_entropy = entropy(np.histogram(with_current, bins='auto')[0])
            
            # Score based on entropy change
            entropy_change = abs(new_entropy - recent_entropy)
            return 1.0 / (1.0 + entropy_change)
        except Exception:
            return 1.0

    def _update_human_probability_ml(self, user_id: str) -> None:
        """Update human probability using enhanced ML analysis."""
        profile = self.profiles[user_id]
        history = self.pattern_history[user_id]
        
        if len(history) < 10:
            return
            
        # Calculate base features
        features = {
            'temporal_consistency': self._calculate_temporal_consistency(user_id),
            'pattern_complexity': self._calculate_pattern_complexity(user_id),
            'response_variability': self._calculate_response_variability(user_id)
        }
        
        # Add anomaly-based features
        anomaly_scores = []
        for dim in ProfileDimension:
            current_value = profile.dimensions[dim]
            score = self._detect_pattern_anomalies(user_id, dim, current_value)
            anomaly_scores.append(score)
        
        features['anomaly_consistency'] = np.mean(anomaly_scores)
        features['anomaly_variability'] = np.std(anomaly_scores)
        
        # Calculate human probability with enhanced feature set
        human_prob = (
            features['temporal_consistency'] * 0.25 +
            features['pattern_complexity'] * 0.25 +
            features['response_variability'] * 0.25 +
            features['anomaly_consistency'] * 0.15 +
            (1.0 - features['anomaly_variability']) * 0.10  # Lower variability is more human-like
        )
        
        profile.is_human_probability = max(0.0, min(1.0, human_prob))

    def _calculate_temporal_consistency(self, user_id: str) -> float:
        """Calculate consistency of behavior over time."""
        history = self.pattern_history[user_id]
        if len(history) < 2:
            return 0.5
            
        differences = []
        for i in range(1, len(history)):
            prev_state = np.array(list(history[i-1].values()))
            curr_state = np.array(list(history[i].values()))
            differences.append(np.mean(np.abs(curr_state - prev_state)))
            
        return 1.0 / (1.0 + np.mean(differences))

    def _calculate_pattern_complexity(self, user_id: str) -> float:
        """Calculate complexity of behavior patterns using entropy and PCA."""
        history = self.pattern_history[user_id]
        if len(history) < 5:
            return 0.5
            
        # Convert history to numpy array
        X = np.array([list(state.values()) for state in history])
        X = self.scaler.fit_transform(X)
        
        # Calculate complexity using PCA explained variance
        self.pca.fit(X)
        explained_variance_ratio = self.pca.explained_variance_ratio_
        
        # Higher complexity if we need more components to explain variance
        complexity_score = entropy(explained_variance_ratio)
        
        # Combine with traditional entropy measure
        traditional_entropy = np.mean([np.std(X[:, i]) for i in range(X.shape[1])])
        
        return min(1.0, (complexity_score + traditional_entropy) / 2)

    def _calculate_response_variability(self, user_id: str) -> float:
        """Calculate variability in responses."""
        history = self.pattern_history[user_id]
        if len(history) < 5:
            return 0.5
            
        # Calculate variability across all dimensions
        variabilities = []
        for dim in ProfileDimension:
            values = [state[dim] for state in history]
            variabilities.append(np.std(values) if len(values) > 1 else 0)
            
        # Normalize variability
        return min(1.0, np.mean(variabilities) * 2)

    def get_personalization_vector(self, user_id: str) -> Dict[str, float]:
        """Generate an ML-enhanced personalization vector for content adaptation."""
        profile = self.get_profile(user_id)
        if not profile:
            return {}
            
        # Calculate confidence-weighted dimensions
        base_vector = {
            dim.value: profile.dimensions[dim] * profile.confidence_scores[dim]
            for dim in ProfileDimension
        }
        
        # Add ML-derived features
        if user_id in self.pattern_history and len(self.pattern_history[user_id]) > 5:
            # Add basic metrics
            base_vector.update({
                'temporal_consistency': self._calculate_temporal_consistency(user_id),
                'pattern_complexity': self._calculate_pattern_complexity(user_id),
                'response_variability': self._calculate_response_variability(user_id)
            })
            
            # Add dimension correlation insights
            if profile.dimension_correlations:
                for (dim1, dim2), corr in profile.dimension_correlations.items():
                    base_vector[f'correlation_{dim1.value}_{dim2.value}'] = corr
            
            # Add feature importance insights
            if profile.feature_importance:
                for dim, importance in profile.feature_importance.items():
                    base_vector[f'importance_{dim.value}'] = importance
            
        return base_vector

    def get_profile(self, user_id: str) -> Optional[BehavioralProfile]:
        """Get a user's behavioral profile with Redis caching."""
        # Try to get from Redis cache first
        cache_key = RedisConfig.USER_PROFILE_CACHE.format(user_id=user_id)
        cached_profile = redis_service.cache_get(cache_key)
        
        if cached_profile:
            return BehavioralProfile.from_dict(cached_profile)
        
        # If not in cache, get from memory
        profile = self.profiles.get(user_id)
        
        # Cache the profile if found
        if profile:
            redis_service.cache_set(
                cache_key,
                profile.to_dict(),
                ttl=RedisConfig.default_cache_ttl
            )
        
        return profile

    def update_full_profile(self, user_id: str, profile: BehavioralProfile) -> None:
        """Update a user's behavioral profile with Redis caching."""
        self.profiles[user_id] = profile
        
        # Update Redis cache
        cache_key = RedisConfig.USER_PROFILE_CACHE.format(user_id=user_id)
        redis_service.cache_set(
            cache_key,
            profile.to_dict(),
            ttl=RedisConfig.default_cache_ttl
        )
        
        # Publish update event
        redis_service.publish(
            RedisConfig.USER_UPDATES,
            {
                "type": "profile_update",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    def delete_profile(self, user_id: str) -> bool:
        """Delete a user's behavioral profile and clear cache."""
        if user_id in self.profiles:
            del self.profiles[user_id]
            
            # Clear Redis cache
            cache_key = RedisConfig.USER_PROFILE_CACHE.format(user_id=user_id)
            redis_service.cache_delete(cache_key)
            
            # Publish deletion event
            redis_service.publish(
                RedisConfig.USER_UPDATES,
                {
                    "type": "profile_delete",
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            return True
        return False

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

    def _update_adaptive_dimension_groups(self, user_id: str) -> None:
        """Dynamically update dimension groups based on correlation patterns."""
        profile = self.profiles.get(user_id)
        if not profile or profile.interaction_count < self.MIN_HISTORY_FOR_ADVANCED:
            return

        # Check if we need to update clusters
        now = datetime.now()
        if (user_id in self.last_cluster_update and 
            now - self.last_cluster_update[user_id] < self.CLUSTER_UPDATE_INTERVAL):
            return

        # Prepare correlation matrix
        dimensions = list(ProfileDimension)
        n_dimensions = len(dimensions)
        correlation_matrix = np.zeros((n_dimensions, n_dimensions))
        
        for i, dim1 in enumerate(dimensions):
            for j, dim2 in enumerate(dimensions):
                if i != j:
                    key = (dim1, dim2)
                    correlation_matrix[i, j] = profile.dimension_correlations.get(key, 0)

        # Apply DBSCAN clustering with adaptive epsilon
        best_clusters = None
        best_score = -1
        
        for eps in np.arange(0.3, 0.8, 0.1):
            clustering = DBSCAN(eps=eps, min_samples=2).fit(correlation_matrix)
            if len(set(clustering.labels_)) > 1:  # Ensure we have actual clusters
                score = silhouette_score(correlation_matrix, clustering.labels_)
                if score > best_score:
                    best_score = score
                    best_clusters = clustering.labels_

        if best_clusters is not None:
            # Form dimension groups based on clusters
            new_groups = []
            unique_clusters = set(best_clusters)
            for cluster_id in unique_clusters:
                if cluster_id != -1:  # Skip noise points
                    cluster_dimensions = {dimensions[i] for i, label in enumerate(best_clusters) 
                                       if label == cluster_id}
                    new_groups.append(cluster_dimensions)
            
            self.dimension_clusters[user_id] = new_groups
            self.last_cluster_update[user_id] = now

    def predict_future_behavior(self, user_id: str, 
                              dimension: ProfileDimension, 
                              horizon_days: int = 7) -> Dict[str, List[float]]:
        """Predict future behavior for a given dimension using Prophet."""
        profile = self.profiles.get(user_id)
        if not profile or profile.interaction_count < self.MIN_HISTORY_FOR_ADVANCED:
            return {"dates": [], "predictions": [], "lower_bound": [], "upper_bound": []}

        # Initialize or get the prediction model for this dimension
        if user_id not in self.prediction_models:
            self.prediction_models[user_id] = {}
        
        if dimension not in self.prediction_models[user_id]:
            self.prediction_models[user_id][dimension] = Prophet(
                changepoint_prior_scale=0.05,
                seasonality_prior_scale=0.1,
                seasonality_mode='multiplicative'
            )

        # Prepare historical data
        history = self.pattern_history.get(user_id, [])
        if not history:
            return {"dates": [], "predictions": [], "lower_bound": [], "upper_bound": []}

        df = pd.DataFrame({
            'ds': pd.date_range(end=datetime.now(), 
                              periods=len(history), 
                              freq='H'),
            'y': [h.get(dimension, 0) for h in history]
        })

        # Fit the model and make predictions
        model = self.prediction_models[user_id][dimension]
        model.fit(df)
        
        future = model.make_future_dataframe(periods=horizon_days * 24, freq='H')
        forecast = model.predict(future)
        
        # Extract predictions and confidence intervals
        predictions = forecast['yhat'].tolist()[-horizon_days * 24:]
        lower_bound = forecast['yhat_lower'].tolist()[-horizon_days * 24:]
        upper_bound = forecast['yhat_upper'].tolist()[-horizon_days * 24:]
        dates = forecast['ds'].tolist()[-horizon_days * 24:]
        
        return {
            "dates": dates,
            "predictions": predictions,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        } 

# Alias for test compatibility: allow importing BehavioralMatrix
BehavioralMatrix = ProfileMatrix 