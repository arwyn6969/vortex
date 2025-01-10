"""
Worker Visibility System - Manages the visibility of workers (both AI and human) and
facilitates indirect interactions between users through environmental traces.
"""
from typing import Dict, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

class VisibilityLevel(Enum):
    SECRET = "secret"      # Completely invisible to users
    SHADOW = "shadow"      # Leaves traces but identity hidden
    WHISPER = "whisper"    # Known to exist but details obscured
    PUBLIC = "public"      # Fully visible to other users

class InteractionTrace(Enum):
    ARTIFACT = "artifact"  # Created items
    GRAFFITI = "graffiti" # Markings or messages
    FOOTPRINT = "footprint"  # Environmental changes
    ECHO = "echo"         # Lingering effects
    STAMP = "stamp"       # Deliberate marks
    RESIDUE = "residue"   # Unintentional traces

@dataclass
class EnvironmentalTrace:
    """A trace left in the environment by a user or AI worker."""
    trace_id: str
    trace_type: InteractionTrace
    creator_id: str
    location: str
    timestamp: datetime
    decay_rate: float  # How quickly the trace fades (0-1)
    visibility: float  # How noticeable the trace is (0-1)
    content: Dict
    metadata: Dict

class WorkerVisibilityManager:
    """
    Manages worker visibility and their traces in the environment.
    Controls how users discover each other through indirect interactions.
    """
    
    def __init__(self):
        self.worker_visibility: Dict[str, VisibilityLevel] = {}
        self.active_traces: Dict[str, EnvironmentalTrace] = {}
        self.discovered_connections: Dict[str, Set[str]] = {}  # user -> discovered_users
        self.trace_interactions: Dict[str, List[Dict]] = {}  # trace -> interactions
        
    def register_worker(
        self,
        worker_id: str,
        visibility_level: VisibilityLevel,
        metadata: Optional[Dict] = None
    ) -> None:
        """Register a worker with their visibility level."""
        self.worker_visibility[worker_id] = visibility_level
        if worker_id not in self.discovered_connections:
            self.discovered_connections[worker_id] = set()
            
    def leave_trace(
        self,
        creator_id: str,
        trace_type: InteractionTrace,
        location: str,
        content: Dict,
        decay_rate: float = 0.1,
        visibility: float = 0.8,
        metadata: Optional[Dict] = None
    ) -> str:
        """Leave a trace in the environment."""
        if creator_id not in self.worker_visibility:
            raise ValueError(f"Unknown worker: {creator_id}")
            
        trace_id = f"trace_{uuid4()}"
        trace = EnvironmentalTrace(
            trace_id=trace_id,
            trace_type=trace_type,
            creator_id=creator_id,
            location=location,
            timestamp=datetime.now(),
            decay_rate=decay_rate,
            visibility=visibility,
            content=content,
            metadata=metadata or {}
        )
        
        self.active_traces[trace_id] = trace
        self.trace_interactions[trace_id] = []
        return trace_id
        
    def discover_trace(
        self,
        discoverer_id: str,
        location: str
    ) -> List[EnvironmentalTrace]:
        """
        Discover traces in a location based on their visibility and decay.
        Returns only traces that are still visible enough to be discovered.
        """
        current_time = datetime.now()
        visible_traces = []
        
        for trace in self.active_traces.values():
            if trace.location != location:
                continue
                
            # Calculate trace visibility based on time decay
            time_diff = (current_time - trace.timestamp).total_seconds()
            current_visibility = trace.visibility * (1 - trace.decay_rate * time_diff)
            
            if current_visibility > 0.1:  # Minimum visibility threshold
                visible_traces.append(trace)
                self._record_trace_interaction(discoverer_id, trace)
                
        return visible_traces
        
    def _record_trace_interaction(
        self,
        discoverer_id: str,
        trace: EnvironmentalTrace
    ) -> None:
        """Record an interaction with a trace and potentially create connection."""
        self.trace_interactions[trace.trace_id].append({
            "discoverer_id": discoverer_id,
            "timestamp": datetime.now()
        })
        
        # If discoverer and creator are different, create connection
        if discoverer_id != trace.creator_id:
            self.discovered_connections[discoverer_id].add(trace.creator_id)
            
    def get_discovered_users(self, user_id: str) -> Set[str]:
        """Get all users that this user has discovered through traces."""
        return self.discovered_connections.get(user_id, set())
        
    def get_trace_history(
        self,
        location: str,
        time_range: Optional[tuple] = None
    ) -> List[EnvironmentalTrace]:
        """Get history of traces in a location within time range."""
        traces = []
        for trace in self.active_traces.values():
            if trace.location != location:
                continue
                
            if time_range:
                start_time, end_time = time_range
                if start_time <= trace.timestamp <= end_time:
                    traces.append(trace)
            else:
                traces.append(trace)
                
        return traces
        
    def cleanup_old_traces(self, visibility_threshold: float = 0.1) -> None:
        """Remove traces that have decayed below visibility threshold."""
        current_time = datetime.now()
        traces_to_remove = []
        
        for trace_id, trace in self.active_traces.items():
            time_diff = (current_time - trace.timestamp).total_seconds()
            current_visibility = trace.visibility * (1 - trace.decay_rate * time_diff)
            
            if current_visibility <= visibility_threshold:
                traces_to_remove.append(trace_id)
                
        for trace_id in traces_to_remove:
            del self.active_traces[trace_id]
            del self.trace_interactions[trace_id]
            
    def get_worker_visibility(self, worker_id: str) -> Optional[VisibilityLevel]:
        """Get the visibility level of a worker."""
        return self.worker_visibility.get(worker_id)
        
    def update_worker_visibility(
        self,
        worker_id: str,
        new_level: VisibilityLevel
    ) -> None:
        """Update the visibility level of a worker."""
        if worker_id not in self.worker_visibility:
            raise ValueError(f"Unknown worker: {worker_id}")
            
        self.worker_visibility[worker_id] = new_level 