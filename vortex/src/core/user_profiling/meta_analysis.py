from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import numpy as np
from datetime import datetime, timedelta
import json
import zlib
import base64
from pathlib import Path
from .profile_matrix import ProfileMatrix, ProfileDimension, BehavioralProfile

@dataclass
class DimensionCorrelation:
    """Represents correlation between two dimensions."""
    dimension1: ProfileDimension
    dimension2: ProfileDimension
    correlation: float
    confidence: float
    sample_size: int

@dataclass
class DimensionTrend:
    """Represents temporal trend in a dimension."""
    dimension: ProfileDimension
    slope: float  # Rate of change
    r_squared: float  # Goodness of fit
    time_span: timedelta
    data_points: int

@dataclass
class ConsistencyMetric:
    """Represents consistency analysis for a dimension."""
    dimension: ProfileDimension
    variance: float
    stability_score: float
    oscillation_frequency: float
    sample_size: int

class MetaAnalysis:
    """Analyzes patterns and relationships across profile dimensions."""
    
    def __init__(
        self,
        profile_matrix: ProfileMatrix,
        storage_path: Optional[str] = None
    ):
        self.profile_matrix = profile_matrix
        self.temporal_data: Dict[str, Dict[ProfileDimension, List[Tuple[float, datetime]]]] = {}
        self.min_correlation_samples = 10
        self.min_trend_samples = 5
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.storage_path = storage_path or "data/meta_analysis"
        self._ensure_storage_path()
        
    def _ensure_storage_path(self) -> None:
        """Ensure storage directory exists."""
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        
    def _get_user_storage_path(self, user_id: str) -> str:
        """Get storage path for user data."""
        return str(Path(self.storage_path) / f"{user_id}.json.gz")
        
    def save_user_data(self, user_id: str) -> None:
        """Save user's temporal data to disk."""
        if user_id not in self.temporal_data:
            return
            
        # Convert temporal data to serializable format
        serializable_data = {
            str(dim): [
                (value, dt.isoformat())
                for value, dt in data
            ]
            for dim, data in self.temporal_data[user_id].items()
        }
        
        # Compress and save
        json_data = json.dumps(serializable_data)
        compressed = zlib.compress(json_data.encode())
        encoded = base64.b64encode(compressed).decode()
        
        with open(self._get_user_storage_path(user_id), 'w') as f:
            json.dump({'data': encoded}, f)
            
    def load_user_data(self, user_id: str) -> None:
        """Load user's temporal data from disk."""
        path = self._get_user_storage_path(user_id)
        if not Path(path).exists():
            return
            
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            # Decompress and parse
            decoded = base64.b64decode(data['data'])
            decompressed = zlib.decompress(decoded)
            loaded_data = json.loads(decompressed)
            
            # Convert back to internal format
            self.temporal_data[user_id] = {
                ProfileDimension(dim): [
                    (value, datetime.fromisoformat(dt))
                    for value, dt in data
                ]
                for dim, data in loaded_data.items()
            }
        except Exception as e:
            print(f"Error loading data for user {user_id}: {e}")
            
    def cleanup_inactive_users(self, max_age: timedelta = timedelta(days=90)) -> None:
        """Remove data for inactive users."""
        current_time = datetime.now()
        users_to_remove = []
        
        for user_id, user_data in self.temporal_data.items():
            # Find most recent activity
            latest_time = max(
                (max(dt for _, dt in dim_data) if dim_data else datetime.min)
                for dim_data in user_data.values()
            )
            
            if current_time - latest_time > max_age:
                # Archive data before removing
                self.save_user_data(user_id)
                users_to_remove.append(user_id)
                
        for user_id in users_to_remove:
            del self.temporal_data[user_id]
            
    def _get_cached_result(
        self,
        user_id: str,
        cache_key: str,
        max_age: timedelta = timedelta(minutes=5)
    ) -> Optional[Any]:
        """Get cached result if still valid."""
        if user_id not in self._cache:
            return None
            
        cache_entry = self._cache[user_id].get(cache_key)
        if not cache_entry:
            return None
            
        timestamp, value = cache_entry
        if datetime.now() - timestamp > max_age:
            return None
            
        return value
        
    def _cache_result(
        self,
        user_id: str,
        cache_key: str,
        value: Any
    ) -> None:
        """Cache a result with timestamp."""
        if user_id not in self._cache:
            self._cache[user_id] = {}
        self._cache[user_id][cache_key] = (datetime.now(), value)
        
    def analyze_dimension_correlations(
        self,
        user_id: str,
        min_confidence: float = 0.7
    ) -> List[DimensionCorrelation]:
        """Analyze correlations between different dimensions with caching."""
        # Check cache first
        cache_key = f"correlations_{min_confidence}"
        cached = self._get_cached_result(user_id, cache_key)
        if cached is not None:
            return cached
            
        # Calculate if not cached
        correlations = super().analyze_dimension_correlations(user_id, min_confidence)
        self._cache_result(user_id, cache_key, correlations)
        return correlations
        
    def update_temporal_data(
        self,
        user_id: str,
        profile: BehavioralProfile
    ) -> None:
        """Update temporal data and manage storage."""
        super().update_temporal_data(user_id, profile)
        
        # Clear caches on update
        if user_id in self._cache:
            self._cache[user_id].clear()
            
        # Periodically save to disk (every 100 updates)
        if profile.interaction_count % 100 == 0:
            self.save_user_data(user_id)
            
    def get_dimension_clusters(
        self,
        user_id: str,
        min_correlation: float = 0.6
    ) -> List[List[ProfileDimension]]:
        """Get dimension clusters with caching."""
        cache_key = f"clusters_{min_correlation}"
        cached = self._get_cached_result(user_id, cache_key)
        if cached is not None:
            return cached
            
        clusters = super().get_dimension_clusters(user_id, min_correlation)
        self._cache_result(user_id, cache_key, clusters)
        return clusters 