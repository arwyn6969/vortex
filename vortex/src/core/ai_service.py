from enum import Enum
from typing import Optional, List, Any, AsyncGenerator
import asyncio

class AIServiceError(Exception):
    """Raised for AI service errors."""
    pass

class ModelNotAvailableError(Exception):
    """Raised when a requested model provider is not available."""
    pass

class ModelProvider(Enum):
    """Supported model providers."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class ModelConfig:
    """Configuration for model providers."""
    def __init__(
        self,
        provider: ModelProvider,
        model_name: str,
        api_base: str,
        api_key: Optional[str] = None
    ):
        self.provider = provider
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key

class AIService:
    """Stub AI service for generating text."""
    def __init__(
        self,
        default_config: ModelConfig,
        fallback_configs: Optional[List[ModelConfig]] = None
    ):
        self.default_config = default_config
        self.fallback_configs = fallback_configs or []
    
    async def generate_text(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        stream: bool = False,
        **kwargs
    ) -> Any:
        # Simulate model not available
        if self.default_config.provider == ModelProvider.ANTHROPIC:
            raise ModelNotAvailableError("Provider not supported")
        if stream:
            async def _gen():
                yield "chunk"
            return _gen()
        return "stub response"

    async def close(self):
        """Stub close method."""
        pass 