"""
Manager for stream connections between ponds.
"""
from typing import List, Optional, Dict
from ..mythology.sefirot import PATHS, get_connected_paths, get_direct_connections
from ..core.constants import SEFIROT_TO_POND

class StreamManager:
    def __init__(self):
        self._stream_connections: Dict[str, List[str]] = {}
        self._initialize_streams()
        
    def _initialize_streams(self) -> None:
        """Initialize all possible stream connections based on Sefirot paths."""
        # Convert Sefirot connections to pond connections
        for path in PATHS.values():
            from_pond = SEFIROT_TO_POND[path["from"]]
            to_pond = SEFIROT_TO_POND[path["to"]]
            
            # Add bidirectional connections
            self._add_stream(from_pond, to_pond)
            self._add_stream(to_pond, from_pond)
    
    def _add_stream(self, from_pond: str, to_pond: str) -> None:
        """Add a one-way stream connection."""
        if from_pond not in self._stream_connections:
            self._stream_connections[from_pond] = []
        if to_pond not in self._stream_connections[from_pond]:
            self._stream_connections[from_pond].append(to_pond)
    
    def get_connected_ponds(self, pond_name: str) -> List[str]:
        """Get all ponds connected to the given pond."""
        return self._stream_connections.get(pond_name, [])
    
    def are_connected(self, pond1: str, pond2: str) -> bool:
        """Check if two ponds are directly connected."""
        return pond2 in self._stream_connections.get(pond1, [])
    
    def get_path_details(self, from_pond: str, to_pond: str) -> Optional[Dict]:
        """Get the details of the path connecting two ponds."""
        # Convert pond names back to Sefirot names
        from_sefirah = next(s for s, p in SEFIROT_TO_POND.items() if p == from_pond)
        to_sefirah = next(s for s, p in SEFIROT_TO_POND.items() if p == to_pond)
        
        # Find the path between these Sefirot
        for path in PATHS.values():
            if (path["from"] == from_sefirah and path["to"] == to_sefirah) or \
               (path["from"] == to_sefirah and path["to"] == from_sefirah):
                return path
        return None
    
    def get_pillar_ponds(self, pillar: str) -> List[str]:
        """Get all ponds in a particular pillar (mercy, severity, or balance)."""
        from ..mythology.sefirot import PILLARS
        return [SEFIROT_TO_POND[sefirah] for sefirah in PILLARS[pillar]]
    
    def get_symbolic_info(self, pond_name: str) -> Optional[Dict]:
        """Get symbolic associations for a pond."""
        from ..mythology.sefirot import SYMBOLS
        # Convert pond name back to Sefirah name
        sefirah = next(s for s, p in SEFIROT_TO_POND.items() if p == pond_name)
        return SYMBOLS.get(sefirah) 