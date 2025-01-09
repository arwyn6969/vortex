# Profile Matrix Documentation

The Profile Matrix is the core component of the behavioral profiling system, responsible for maintaining and updating user behavioral profiles.

## Overview

The Profile Matrix tracks multiple dimensions of user behavior and maintains confidence scores for each dimension. It uses a weighted update system to ensure that new observations are incorporated proportionally to their confidence level.

## Components

### ProfileDimension Enum

Defines the key behavioral dimensions tracked:
- `EMPATHY`: Ability to understand and share feelings
- `DECISION_MAKING`: Decision-making style and effectiveness
- `EMOTIONAL_RESPONSE`: Emotional reaction patterns
- `CREATIVITY`: Creative thinking and problem-solving
- `RISK_TOLERANCE`: Attitude towards risk
- `STRATEGIC_THINKING`: Strategic planning ability
- `MORAL_ALIGNMENT`: Ethical decision-making tendencies

### BehavioralProfile Class

Represents a user's behavioral profile with:
- `user_id`: Unique identifier
- `dimensions`: Current values for each dimension (0.0-1.0)
- `confidence_scores`: Confidence in each dimension's value
- `is_human_probability`: Likelihood the user is human
- `last_updated`: Timestamp of last update
- `interaction_count`: Total number of interactions

## Key Methods

### create_profile
```python
def create_profile(self, user_id: str) -> BehavioralProfile
```
Creates a new profile with default values:
- All dimensions initialized to 0.5
- Zero confidence scores
- 50% human probability
- Current timestamp
- Zero interactions

### update_profile
```python
def update_profile(
    self,
    user_id: str,
    dimension: ProfileDimension,
    value: float,
    confidence: float
) -> None
```
Updates a specific dimension:
- Uses weighted average based on confidence
- Automatically creates profile if needed
- Updates interaction count and timestamp

### get_personalization_vector
```python
def get_personalization_vector(self, user_id: str) -> Dict[str, float]
```
Generates a vector for content adaptation:
- Returns dimension values weighted by confidence
- Used by the personalization engine

## Usage Example

```python
profile_matrix = ProfileMatrix()

# Create or update a profile
profile_matrix.update_profile(
    user_id="user123",
    dimension=ProfileDimension.EMPATHY,
    value=0.8,
    confidence=0.6
)

# Get profile for personalization
profile = profile_matrix.get_profile("user123")
if profile:
    print(f"Empathy level: {profile.dimensions[ProfileDimension.EMPATHY]}")
```

## Implementation Details

### Confidence Weighting
The system uses confidence scores to weight updates:
```python
new_value = (current_val * current_conf + value * confidence) / new_conf
```

### Human Probability
Updated separately from dimensions:
```python
profile.is_human_probability = probability
```

### Timestamp Management
Uses numpy datetime64 for precise timestamping:
```python
last_updated = np.datetime64('now').astype(float)
``` 