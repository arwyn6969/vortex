"""
Vortex AI Service using Vercel AI SDK patterns
============================================

This module implements Vercel AI SDK patterns in Python for unified AI model interactions.
Provides streaming responses, provider flexibility, and improved error handling.
"""

import asyncio
import json
from typing import List, Dict, Any, AsyncGenerator, Optional, Union
import httpx
import logging
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

from .ai.mcp_transport import (
    MCPTransport,
    MCPRequest,
    MCPResponse,
    StdioTransport,
    HTTPTransport,
    WebSocketTransport,
    TransportType
)

logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    """Supported AI model providers."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"

@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    provider: ModelProvider
    model_name: str
    api_base: str
    api_key: Optional[str] = None
    transport_type: TransportType = TransportType.HTTP
    transport_options: Optional[Dict[str, Any]] = None
    
class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass

class ModelNotAvailableError(AIServiceError):
    """Raised when a requested model is not available."""
    pass

class AIService:
    """Implements Vercel AI SDK patterns for interacting with AI models."""
    
    def __init__(
        self,
        default_config: ModelConfig,
        fallback_configs: Optional[List[ModelConfig]] = None,
        timeout: float = 30.0
    ):
        """Initialize the AI service.
        
        Args:
            default_config: Primary model configuration
            fallback_configs: Backup model configurations
            timeout: Request timeout in seconds
        """
        self.default_config = default_config
        self.fallback_configs = fallback_configs or []
        self.timeout = timeout
        self._transports = {}
        
    def _create_transport(self, config: ModelConfig) -> MCPTransport:
        """Create appropriate transport for model config."""
        options = config.transport_options or {}
        
        if config.transport_type == TransportType.STDIO:
            return StdioTransport(options.get("process_cmd", ""))
        elif config.transport_type == TransportType.WEBSOCKET:
            return WebSocketTransport(options.get("ws_url", ""))
        else:  # Default to HTTP
            headers = {}
            if config.api_key:
                headers["Authorization"] = f"Bearer {config.api_key}"
            return HTTPTransport(config.api_base, headers)
            
    def _get_transport(self, config: ModelConfig) -> MCPTransport:
        """Get or create transport for model config."""
        key = (config.provider, config.model_name, config.transport_type)
        if key not in self._transports:
            self._transports[key] = self._create_transport(config)
        return self._transports[key]
        
    async def generate_text(
        self, 
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        stream: bool = False,
        model_config: Optional[ModelConfig] = None
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Generate text using the specified model.
        
        Implements the Vercel AI SDK generateText pattern.
        
        Args:
            prompt: The prompt to generate text from
            system: System message/instructions
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stream: Whether to stream the response
            model_config: Optional specific model config to use
            
        Returns:
            Either the complete text response or an async generator of text chunks
            
        Raises:
            AIServiceError: If text generation fails
        """
        config = model_config or self.default_config
        
        try:
            return await self._generate_with_config(
                config,
                prompt,
                system,
                max_tokens,
                temperature,
                stream
            )
        except Exception as e:
            logger.error(f"Text generation failed with {config.provider}: {e}")
            
            # Try fallback models if available
            for fallback in self.fallback_configs:
                try:
                    logger.info(f"Attempting fallback to {fallback.provider}")
                    return await self._generate_with_config(
                        fallback,
                        prompt,
                        system,
                        max_tokens,
                        temperature,
                        stream
                    )
                except Exception as e:
                    logger.error(f"Fallback to {fallback.provider} failed: {e}")
                    continue
                    
            raise AIServiceError("All generation attempts failed")
            
    async def _generate_with_config(
        self,
        config: ModelConfig,
        prompt: str,
        system: Optional[str],
        max_tokens: Optional[int],
        temperature: float,
        stream: bool
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Generate text using a specific model configuration."""
        
        transport = self._get_transport(config)
        
        # Prepare request payload based on provider
        if config.provider == ModelProvider.OLLAMA:
            payload = {
                "model": config.model_name,
                "prompt": prompt,
                "stream": stream
            }
            if system:
                payload["system"] = system
            if max_tokens:
                payload["max_tokens"] = max_tokens
            if temperature is not None:
                payload["temperature"] = temperature
                
        elif config.provider == ModelProvider.OPENAI:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": config.model_name,
                "messages": messages,
                "stream": stream
            }
            if max_tokens:
                payload["max_tokens"] = max_tokens
            if temperature is not None:
                payload["temperature"] = temperature
                
        elif config.provider == ModelProvider.ANTHROPIC:
            # Format prompt for Claude
            formatted_prompt = ""
            if system:
                formatted_prompt += f"\n\nSystem: {system}\n\n"
            formatted_prompt += f"Human: {prompt}\n\nAssistant:"
            
            payload = {
                "model": config.model_name,
                "prompt": formatted_prompt,
                "stream": stream,
                "max_tokens_to_sample": max_tokens or 4096,
                "temperature": temperature
            }
            
        else:
            raise ModelNotAvailableError(f"Provider {config.provider} not implemented")
            
        # Send request through transport
        request = MCPRequest(
            type="generate",
            payload=payload,
            metadata={"provider": config.provider.value}
        )
        
        if stream:
            return self._stream_response(transport, request)
        else:
            return await self._complete_response(transport, request)
            
    async def _stream_response(
        self,
        transport: MCPTransport,
        request: MCPRequest
    ) -> AsyncGenerator[str, None]:
        """Stream response chunks from transport."""
        async for response in transport.send_request(request):
            if response.type == "error":
                raise AIServiceError(response.payload.get("error", "Unknown error"))
            elif response.type == "text":
                yield response.payload.get("content", "")
                
    async def _complete_response(
        self,
        transport: MCPTransport,
        request: MCPRequest
    ) -> str:
        """Get complete response from transport."""
        chunks = []
        async for response in transport.send_request(request):
            if response.type == "error":
                raise AIServiceError(response.payload.get("error", "Unknown error"))
            elif response.type == "text":
                chunks.append(response.payload.get("content", ""))
        return "".join(chunks)
        
    async def close(self):
        """Close all transports."""
        for transport in self._transports.values():
            await transport.close()
        self._transports.clear() 