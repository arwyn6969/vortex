"""Tests for the guide dialogue system."""

import pytest
from typing import AsyncGenerator
from src.guides.dialogue import (
    DialogueManager,
    DialogueContext,
    GuidePersona,
    GuidanceStyle
)
from src.core.ai_service import AIService, ModelConfig, ModelProvider

@pytest.fixture
def ai_service():
    """Fixture for AI service with test configuration."""
    config = ModelConfig(
        provider=ModelProvider.OLLAMA,
        model_name="hermes3",
        api_base="http://localhost:11434"
    )
    return AIService(default_config=config)

@pytest.fixture
def guide_persona():
    """Fixture for a test guide persona."""
    return GuidePersona(
        name="Thoth",
        tradition="Egyptian",
        style=GuidanceStyle.WISE,
        description="Ancient Egyptian god of wisdom and knowledge",
        key_traits=["wise", "scholarly", "mystical", "precise"]
    )

@pytest.fixture
def dialogue_context(guide_persona):
    """Fixture for dialogue context."""
    return DialogueContext(
        guide=guide_persona,
        user_profile={
            "wisdom": 0.7,
            "intuition": 0.6,
            "knowledge": 0.8
        },
        conversation_history=[],
        current_location="Library of Ancient Wisdom",
        current_quest="Seeking the Emerald Tablets"
    )

@pytest.fixture
def dialogue_manager(ai_service):
    """Fixture for dialogue manager."""
    return DialogueManager(ai_service)

@pytest.mark.asyncio
async def test_welcome_generation(dialogue_manager, dialogue_context):
    """Test welcome message generation."""
    welcome = await dialogue_manager.generate_welcome(dialogue_context)
    assert isinstance(welcome, str)
    assert dialogue_context.guide.name in welcome
    assert len(welcome) > 0

@pytest.mark.asyncio
async def test_response_generation(dialogue_manager, dialogue_context):
    """Test basic response generation."""
    response = await dialogue_manager.generate_response(
        dialogue_context,
        "What is the nature of wisdom?"
    )
    assert isinstance(response, str)
    assert len(response) > 0
    assert dialogue_context.guide.tradition.lower() in response.lower()

@pytest.mark.asyncio
async def test_streaming_response(dialogue_manager, dialogue_context):
    """Test streaming response generation."""
    stream = await dialogue_manager.generate_response(
        dialogue_context,
        "Tell me about the mysteries of life.",
        stream=True
    )
    assert isinstance(stream, AsyncGenerator)
    
    chunks = []
    async for chunk in stream:
        chunks.append(chunk)
        
    assert len(chunks) > 0
    combined = "".join(chunks)
    assert dialogue_context.guide.name in combined

@pytest.mark.asyncio
async def test_quest_guidance(dialogue_manager, dialogue_context):
    """Test quest-specific guidance generation."""
    guidance = await dialogue_manager.generate_quest_guidance(
        dialogue_context,
        "Find the hidden temple of wisdom",
        0.5
    )
    assert isinstance(guidance, str)
    assert len(guidance) > 0
    # Should mention progress or encouragement
    assert any(word in guidance.lower() for word in ["progress", "continue", "path", "forward"])

@pytest.mark.asyncio
async def test_location_insight(dialogue_manager, dialogue_context):
    """Test location-specific insight generation."""
    insight = await dialogue_manager.generate_location_insight(
        dialogue_context,
        "An ancient temple with hieroglyphic inscriptions",
        ["sacred pool", "eternal flame", "wisdom scrolls"]
    )
    assert isinstance(insight, str)
    assert len(insight) > 0
    # Should mention at least one special element
    assert any(element.lower() in insight.lower() 
              for element in ["pool", "flame", "scrolls"])

@pytest.mark.asyncio
async def test_conversation_history_influence(dialogue_manager, dialogue_context):
    """Test that conversation history influences responses."""
    # Add some history
    dialogue_context.conversation_history = [
        {"role": "user", "content": "What is the path to wisdom?"},
        {"role": "assistant", "content": "The path to wisdom begins with understanding oneself."},
        {"role": "user", "content": "How do I understand myself?"}
    ]
    
    response = await dialogue_manager.generate_response(
        dialogue_context,
        "Can you elaborate on that?"
    )
    assert isinstance(response, str)
    assert len(response) > 0
    # Response should reference previous conversation about self-understanding
    assert any(word in response.lower() for word in ["self", "understand", "wisdom"])

@pytest.mark.asyncio
async def test_error_handling(dialogue_manager, dialogue_context, monkeypatch):
    """Test graceful handling of AI service errors."""
    
    # Make AI service fail
    async def mock_failed_generate(*args, **kwargs):
        raise Exception("AI service error")
        
    monkeypatch.setattr(
        dialogue_manager.ai_service,
        "generate_text",
        mock_failed_generate
    )
    
    # Test welcome message fallback
    welcome = await dialogue_manager.generate_welcome(dialogue_context)
    assert isinstance(welcome, str)
    assert dialogue_context.guide.name in welcome
    
    # Test response fallback
    response = await dialogue_manager.generate_response(
        dialogue_context,
        "Hello?"
    )
    assert isinstance(response, str)
    assert "apologize" in response.lower()
    
    # Test streaming fallback
    stream = await dialogue_manager.generate_response(
        dialogue_context,
        "Hello?",
        stream=True
    )
    chunks = []
    async for chunk in stream:
        chunks.append(chunk)
    assert len(chunks) > 0
    assert "apologize" in "".join(chunks).lower() 