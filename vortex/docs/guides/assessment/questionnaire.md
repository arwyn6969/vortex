# Voight-Kampff Questionnaire Documentation

The Voight-Kampff Questionnaire is an advanced assessment system inspired by the fictional test from "Do Androids Dream of Electric Sheep?" It evaluates users across multiple behavioral dimensions while helping distinguish between human and bot users.

## Overview

The questionnaire presents carefully crafted scenarios designed to:
- Measure emotional responses
- Assess decision-making patterns
- Gauge empathy levels
- Evaluate moral reasoning
- Detect bot-like behavior patterns

## Components

### Question Class

Represents a profiling question with:
- `id`: Unique identifier
- `text`: The question text
- `options`: List of possible responses
- `dimension_impacts`: How each dimension is affected
- `human_detection_weight`: Importance for human/bot detection

## Question Types

### Empathy Assessment
Example:
```python
Question(
    id="empathy_1",
    text="You find an injured animal on your way home. What's your immediate response?",
    options=[
        "Take it to a vet immediately",
        "Call animal services for help",
        "Leave it be - nature takes its course",
        "Take a photo to post online"
    ],
    dimension_impacts={
        ProfileDimension.EMPATHY: 1.0,
        ProfileDimension.DECISION_MAKING: 0.5,
        ProfileDimension.EMOTIONAL_RESPONSE: 0.8
    },
    human_detection_weight=0.8
)
```

### Creative Thinking
Example:
```python
Question(
    id="creativity_1",
    text="You have unlimited resources for one day. What do you create?",
    options=[
        "A solution to a global problem",
        "A piece of art that moves people",
        "A revolutionary technology",
        "A perfect moment with loved ones"
    ],
    dimension_impacts={
        ProfileDimension.CREATIVITY: 1.0,
        ProfileDimension.MORAL_ALIGNMENT: 0.6,
        ProfileDimension.STRATEGIC_THINKING: 0.4
    },
    human_detection_weight=0.6
)
```

## Key Methods

### get_question
```python
def get_question(self, index: int) -> Optional[Question]
```
Retrieves a specific question:
- Returns None if index is out of range
- Questions are presented in a specific order

### analyze_response
```python
def analyze_response(
    self,
    question: Question,
    option_index: int
) -> Dict[str, float]
```
Analyzes user responses:
- Validates input values
- Applies response weights
- Calculates dimension impacts
- Assesses human probability

## Response Analysis

### Weight System
Responses are weighted based on position:
```python
weights = [1.0, 0.7, 0.3, 0.0]
```
- First option: Full weight (1.0)
- Second option: High weight (0.7)
- Third option: Low weight (0.3)
- Fourth option: Zero weight (0.0)

### Impact Calculation
```python
impacts = {
    dim: value * weight
    for dim, value in question.dimension_impacts.items()
}
```

### Human Probability
```python
impacts['human_probability'] = question.human_detection_weight * weight
```

## Usage Example

```python
questionnaire = VoightKampffQuestionnaire()

# Get and process a question
question = questionnaire.get_question(0)
if question:
    print(f"Question: {question.text}")
    for i, option in enumerate(question.options):
        print(f"{i+1}. {option}")
        
    # Analyze user's response (example: user chose first option)
    impacts = questionnaire.analyze_response(question, 0)
    print(f"Response impacts: {impacts}")
```

## Implementation Notes

### Input Validation
```python
if not isinstance(option_index, int):
    raise ValueError("option_index must be an integer")

if option_index < 0 or option_index >= len(question.options):
    raise ValueError(f"option_index must be between 0 and {len(question.options)-1}")
```

### Question Design Principles
1. Emotional engagement
2. No right/wrong answers
3. Multiple valid interpretations
4. Subtle behavioral indicators
5. Cultural neutrality 