"""
Tests for the LLM-powered dialogue system.
"""
import pytest
from unittest.mock import Mock, patch
from typing import Dict
from ...src.guides.llm_dialogue import (
    LLMDialogueGenerator,
    DialogueContext,
    DialogueError,
    ResponseValidationError
)
from ...src.core.user_profiling.profile_matrix import ProfileDimension
from ...src.mythology.archetype_manager import CulturalSystem

@pytest.fixture
def mock_llm():
    """Create a mock LLM client."""
    with patch("vortex.src.guides.llm_dialogue.DeepseekClient") as mock:
        client = Mock()
        mock.return_value = client
        yield client

@pytest.fixture
def dialogue_context():
    """Create a test dialogue context."""
    return DialogueContext(
        guide_name="Maat",
        guide_archetype="wisdom_keeper",
        cultural_system=CulturalSystem.EGYPTIAN.value,
        attributes={"wisdom", "justice", "truth"},
        profile={
            ProfileDimension.MORAL_ALIGNMENT: 0.8,
            ProfileDimension.EMPATHY: 0.7,
            ProfileDimension.WISDOM: 0.6
        },
        interaction_history=[],
        guidance_style={
            "balanced": 0.6,
            "ethical": 0.8,
            "nurturing": 0.5,
            "direct": 0.4
        }
    )

@pytest.fixture
def dialogue_generator(mock_llm):
    """Create a dialogue generator with mocked LLM."""
    return LLMDialogueGenerator()

def test_welcome_message_generation(dialogue_generator, dialogue_context, mock_llm):
    """Test welcome message generation."""
    mock_llm.generate.return_value = "Greetings, I am Maat. Welcome to your journey."
    
    response = dialogue_generator.generate_welcome(dialogue_context)
    
    assert "Maat" in response
    assert mock_llm.generate.called
    assert len(mock_llm.generate.call_args[0]) > 0

def test_response_generation(dialogue_generator, dialogue_context, mock_llm):
    """Test response generation."""
    mock_llm.generate.return_value = "As Maat, I understand your question about truth."
    
    response = dialogue_generator.generate_response(dialogue_context, "What is truth?")
    
    assert "Maat" in response
    assert mock_llm.generate.called
    assert len(dialogue_generator.conversation_memory) == 1

def test_response_validation(dialogue_generator, dialogue_context):
    """Test response validation."""
    # Test empty response
    with pytest.raises(ResponseValidationError):
        dialogue_generator._validate_response("", dialogue_context)
    
    # Test response without character name
    with pytest.raises(ResponseValidationError):
        dialogue_generator._validate_response("A generic response", dialogue_context)
    
    # Test too verbose response
    verbose_response = " ".join(["word"] * 150)
    with pytest.raises(ResponseValidationError):
        dialogue_generator._validate_response(verbose_response, dialogue_context)
    
    # Test repetitive response
    repetitive = "Maat says wisdom is wisdom, wisdom is truth, wisdom is wisdom"
    with pytest.raises(ResponseValidationError):
        dialogue_generator._validate_response(repetitive, dialogue_context)

def test_conversation_memory(dialogue_generator, dialogue_context, mock_llm):
    """Test conversation memory management."""
    mock_llm.generate.return_value = "As Maat, I hear you."
    
    # Test memory accumulation
    for i in range(5):
        dialogue_generator.generate_response(dialogue_context, f"Question {i}")
    
    assert len(dialogue_generator.conversation_memory) == 5
    
    # Test memory limit
    for i in range(10):
        dialogue_generator.generate_response(dialogue_context, f"Extra {i}")
    
    assert len(dialogue_generator.conversation_memory) == dialogue_generator.max_history

def test_fallback_responses(dialogue_generator, dialogue_context, mock_llm):
    """Test fallback response generation."""
    mock_llm.generate.side_effect = Exception("LLM Error")
    
    # Test welcome fallback
    welcome = dialogue_generator.generate_welcome(dialogue_context)
    assert "Maat" in welcome
    assert "journey" in welcome.lower()
    
    # Test response fallback
    response = dialogue_generator.generate_response(dialogue_context, "Hello")
    assert "Maat" in response
    assert "clearer" in response.lower()

def test_response_cleaning(dialogue_generator):
    """Test response cleaning functionality."""
    test_cases = [
        ('Hello\nWorld', 'Hello World'),
        ('Too  many    spaces', 'Too many spaces'),
        ('Response with "quotes"', 'Response with "quotes"'),
        ('Trailing quote"', 'Trailing quote'),
        ('\n\nNew lines\n\n', 'New lines')
    ]
    
    for input_text, expected in test_cases:
        assert dialogue_generator._clean_response(input_text) == expected

def test_profile_formatting(dialogue_generator, dialogue_context):
    """Test profile formatting."""
    formatted = dialogue_generator._format_profile(dialogue_context.profile)
    
    assert "MORAL_ALIGNMENT: 0.80" in formatted
    assert "EMPATHY: 0.70" in formatted
    assert "WISDOM: 0.60" in formatted

def test_guidance_style_adaptation(dialogue_generator, dialogue_context):
    """Test guidance style formatting and extraction."""
    primary_style = dialogue_generator._get_primary_guidance_style(dialogue_context.guidance_style)
    
    assert "ethical" in primary_style
    assert "0.8" in primary_style

def test_key_profile_traits(dialogue_generator, dialogue_context):
    """Test key profile trait extraction."""
    traits = dialogue_generator._get_key_profile_traits(dialogue_context.profile)
    
    assert "moral_alignment:0.8" in traits
    assert "empathy:0.7" in traits

def test_repetition_detection(dialogue_generator):
    """Test repetition detection in responses."""
    assert not dialogue_generator._has_significant_repetition("A normal response")
    assert dialogue_generator._has_significant_repetition("The wisdom of wisdom is wisdom")
    assert not dialogue_generator._has_significant_repetition("Short") 