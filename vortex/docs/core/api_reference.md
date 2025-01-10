# Vortex of Enlightenment API Reference

## Core APIs

### Stream Manager API

#### StreamManager

```python
from vortex.core.stream_manager import StreamManager

class StreamManager:
    """Manages the flow between different ponds and handles state transitions."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the stream manager.
        
        Args:
            config: Configuration dictionary containing:
                - pond_configs: Pond initialization parameters
                - routing_rules: Stream routing rules
                - state_handlers: Custom state transition handlers
        """
        
    def route_to_pond(self, pond_name: str) -> bool:
        """Route the current stream to a specific pond.
        
        Args:
            pond_name: Name of the target pond
            
        Returns:
            bool: True if routing successful
        """
        
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current state of the stream manager.
        
        Returns:
            Dict containing:
                - current_pond: Current active pond
                - available_paths: List of available routing options
                - state_metadata: Additional state information
        """
```

### Profile Matrix API

#### ProfileMatrix

```python
from vortex.core.profile_matrix import ProfileMatrix

class ProfileMatrix:
    """Multi-dimensional user profile tracking and analysis."""
    
    def __init__(self, dimensions: List[str]) -> None:
        """Initialize the profile matrix.
        
        Args:
            dimensions: List of profile dimensions to track
        """
        
    def update(self, 
              dimension: str, 
              value: float, 
              context: Optional[Dict] = None) -> None:
        """Update a profile dimension.
        
        Args:
            dimension: The dimension to update
            value: New value for the dimension
            context: Optional context for the update
        """
        
    def analyze_patterns(self) -> List[Dict[str, Any]]:
        """Analyze behavioral patterns in the profile.
        
        Returns:
            List of identified patterns with metadata
        """
        
    @property
    def current_state(self) -> ProfileState:
        """Get the current profile state."""
```

## Pond APIs

### Base Pond Interface

```python
from vortex.zones.base_zone import BaseZone
from typing import Optional, Dict, Any

class BaseZone:
    """Base interface for all pond implementations."""
    
    def enter(self, context: Optional[Dict] = None) -> bool:
        """Enter the pond.
        
        Args:
            context: Optional entry context
            
        Returns:
            bool: True if entry successful
        """
        
    def process_input(self, 
                     input_data: str, 
                     profile: ProfileMatrix) -> Dict[str, Any]:
        """Process user input within the pond.
        
        Args:
            input_data: User input string
            profile: User's profile matrix
            
        Returns:
            Dict containing:
                - response: System response
                - state_changes: Any state changes
                - profile_updates: Profile update data
        """
        
    def generate_challenge(self, 
                         difficulty: float, 
                         profile: ProfileMatrix) -> Challenge:
        """Generate a new challenge.
        
        Args:
            difficulty: Target difficulty level
            profile: User's profile matrix
            
        Returns:
            Challenge object containing challenge data
        """
```

## Mythology Integration APIs

### Mythology Manager

```python
from vortex.mythology.manager import MythologyManager

class MythologyManager:
    """Manages integration of different mystical traditions."""
    
    def integrate_traditions(self, 
                           traditions: List[str], 
                           context: Dict[str, Any]) -> Integration:
        """Integrate multiple traditions.
        
        Args:
            traditions: List of traditions to integrate
            context: Integration context
            
        Returns:
            Integration object with combined wisdom
        """
        
    def get_sacred_geometry(self, 
                          pattern: str, 
                          dimensions: int) -> GeometryPattern:
        """Get sacred geometry patterns.
        
        Args:
            pattern: Pattern name
            dimensions: Number of dimensions
            
        Returns:
            GeometryPattern object
        """
```

## Usage Examples

### Basic Stream Management

```python
# Initialize the stream manager
config = {
    'pond_configs': DEFAULT_POND_CONFIGS,
    'routing_rules': DEFAULT_ROUTING_RULES,
    'state_handlers': custom_handlers
}
manager = StreamManager(config)

# Route to a pond
success = manager.route_to_pond('wisdom')
if success:
    current_state = manager.get_current_state()
    print(f"Current pond: {current_state['current_pond']}")
```

### Profile Management

```python
# Initialize profile matrix
dimensions = ['wisdom', 'empathy', 'expression', 'boundaries']
profile = ProfileMatrix(dimensions)

# Update profile
profile.update('wisdom', 0.8, context={'challenge': 'pattern_recognition'})
profile.update('empathy', 0.6, context={'interaction': 'helping_others'})

# Analyze patterns
patterns = profile.analyze_patterns()
for pattern in patterns:
    print(f"Pattern: {pattern['name']}, Confidence: {pattern['confidence']}")
```

### Challenge Generation

```python
# Initialize a pond
wisdom_pond = WisdomPond()

# Generate a challenge
profile = get_user_profile()  # Get current user profile
challenge = wisdom_pond.generate_challenge(
    difficulty=0.7,
    profile=profile
)

# Process challenge response
response = wisdom_pond.process_input(
    "The patterns connect through sacred geometry",
    profile
)
```

### Mythology Integration

```python
# Initialize mythology manager
manager = MythologyManager()

# Integrate traditions
integration = manager.integrate_traditions(
    traditions=['sefirot', 'mayan'],
    context={'focus': 'time_cycles'}
)

# Get sacred geometry
pattern = manager.get_sacred_geometry(
    pattern='flower_of_life',
    dimensions=2
)
```

## Error Handling

### Common Errors

```python
from vortex.exceptions import (
    PondNotFoundError,
    ProfileUpdateError,
    IntegrationError
)

try:
    manager.route_to_pond('nonexistent_pond')
except PondNotFoundError as e:
    print(f"Pond not found: {e}")

try:
    profile.update('invalid_dimension', 0.5)
except ProfileUpdateError as e:
    print(f"Profile update failed: {e}")
```

## Best Practices

1. **Profile Updates**
   - Always provide context with updates
   - Use appropriate value ranges
   - Handle update errors gracefully

2. **Stream Management**
   - Check routing success
   - Maintain state consistency
   - Handle transitions properly

3. **Challenge Generation**
   - Consider profile state
   - Maintain difficulty progression
   - Provide clear feedback

4. **Error Handling**
   - Use specific exceptions
   - Provide meaningful error messages
   - Implement proper recovery

## Type Definitions

```python
from typing import TypedDict, Union

class ProfileState(TypedDict):
    dimensions: Dict[str, float]
    metadata: Dict[str, Any]
    history: List[Dict[str, Any]]

class Challenge(TypedDict):
    type: str
    difficulty: float
    content: Dict[str, Any]
    metadata: Dict[str, Any]

class Integration(TypedDict):
    traditions: List[str]
    patterns: List[Dict[str, Any]]
    guidance: str
``` 