"""Tests for the AI service implementation."""

import pytest
import asyncio
from typing import AsyncGenerator
from src.core.ai_service import (
    AIService,
    ModelConfig,
    ModelProvider,
    AIServiceError,
    ModelNotAvailableError
)

@pytest.fixture
def ollama_config():
    """Fixture for Ollama model configuration."""
    return ModelConfig(
        provider=ModelProvider.OLLAMA,
        model_name="hermes3",
        api_base="http://localhost:11434"
    )

@pytest.fixture
def openai_config():
    """Fixture for OpenAI model configuration."""
    return ModelConfig(
        provider=ModelProvider.OPENAI,
        model_name="gpt-3.5-turbo",
        api_base="https://api.openai.com",
        api_key="test-key"
    )

@pytest.fixture
def ai_service(ollama_config, openai_config):
    """Fixture for AI service with both Ollama and OpenAI configs."""
    return AIService(
        default_config=ollama_config,
        fallback_configs=[openai_config]
    )

@pytest.mark.asyncio
async def test_generate_text_basic(ai_service):
    """Test basic text generation."""
    prompt = "Write a haiku about coding"
    response = await ai_service.generate_text(prompt)
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_generate_text_with_system(ai_service):
    """Test text generation with system message."""
    prompt = "What is the capital of France?"
    system = "You are a helpful geography teacher."
    response = await ai_service.generate_text(prompt, system=system)
    assert isinstance(response, str)
    assert "Paris" in response.lower()

@pytest.mark.asyncio
async def test_streaming_generation(ai_service):
    """Test streaming text generation."""
    prompt = "Count from 1 to 5"
    stream = await ai_service.generate_text(prompt, stream=True)
    assert isinstance(stream, AsyncGenerator)
    
    chunks = []
    async for chunk in stream:
        chunks.append(chunk)
        
    assert len(chunks) > 0
    combined = "".join(chunks)
    assert any(str(i) in combined for i in range(1, 6))

@pytest.mark.asyncio
async def test_fallback_behavior(ai_service, monkeypatch):
    """Test fallback to secondary model on primary failure."""
    
    # Make primary model fail
    async def mock_failed_generate(*args, **kwargs):
        raise AIServiceError("Primary model failed")
        
    monkeypatch.setattr(
        ai_service,
        "_generate_ollama",
        mock_failed_generate
    )
    
    # Mock successful OpenAI response
    async def mock_openai_generate(*args, **kwargs):
        return "Response from fallback model"
        
    monkeypatch.setattr(
        ai_service,
        "_generate_openai",
        mock_openai_generate
    )
    
    response = await ai_service.generate_text("Test prompt")
    assert response == "Response from fallback model"

@pytest.mark.asyncio
async def test_invalid_provider():
    """Test handling of unsupported model provider."""
    config = ModelConfig(
        provider=ModelProvider.ANTHROPIC,  # Not implemented yet
        model_name="claude",
        api_base="https://api.anthropic.com"
    )
    service = AIService(default_config=config)
    
    with pytest.raises(ModelNotAvailableError):
        await service.generate_text("Test prompt")

@pytest.mark.asyncio
async def test_temperature_control(ai_service):
    """Test temperature parameter affects response variability."""
    prompt = "Generate a random number between 1 and 10"
    
    # Get multiple responses with high temperature
    high_temp_responses = set()
    for _ in range(3):
        response = await ai_service.generate_text(prompt, temperature=0.9)
        high_temp_responses.add(response)
        
    # Get multiple responses with low temperature
    low_temp_responses = set()
    for _ in range(3):
        response = await ai_service.generate_text(prompt, temperature=0.1)
        low_temp_responses.add(response)
        
    # High temperature should give more varied responses
    assert len(high_temp_responses) >= len(low_temp_responses)

@pytest.mark.asyncio
async def test_service_cleanup(ai_service):
    """Test proper cleanup of HTTP client."""
    await ai_service.close()
    # Verify client is closed by attempting to use it
    with pytest.raises(Exception):
        await ai_service.generate_text("This should fail") 