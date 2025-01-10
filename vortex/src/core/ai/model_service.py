"""
Vortex AI Model Service
======================

This module provides a unified interface for interacting with multiple locally hosted
Ollama models:

Models:
- llama3.2-vision: For visual analysis and interpretation
- hermes3: For general text generation and conversation
- mxbai-embed-large: For generating embeddings and semantic analysis

Usage:
------
```python
from vortex.src.core.ai.model_service import VortexAI

# Initialize the service
ai_service = VortexAI()

# Vision analysis
vision_result = await ai_service.analyze_image("path/to/image.jpg", "Describe this sacred geometry")

# Text generation
response = await ai_service.generate_text("Explain the mystical significance of the number 7")

# Generate embeddings
embeddings = await ai_service.get_embeddings("spiritual text to embed")

# Chat conversation
chat_response = await ai_service.chat([
    {"role": "system", "content": "You are a mystical guide"},
    {"role": "user", "content": "What is the meaning of the Kabbalistic Tree of Life?"}
])
```
"""

from typing import Optional, Dict, Any, List, Union
import base64
import asyncio
import httpx
import logging
from functools import lru_cache
import json
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)

class VortexAI:
    """Unified service for interacting with multiple Ollama AI models."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        vision_model: str = "llama3.2-vision",
        text_model: str = "hermes3",
        embedding_model: str = "mxbai-embed-large"
    ):
        """Initialize the VortexAI service.
        
        Args:
            base_url: Ollama API base URL
            vision_model: Model name for vision tasks
            text_model: Model name for text generation
            embedding_model: Model name for embeddings
        """
        self.base_url = base_url
        self.vision_model = vision_model
        self.text_model = text_model
        self.embedding_model = embedding_model
        self._client = httpx.AsyncClient(timeout=30.0)
        
    async def _check_model_availability(self, model_name: str) -> bool:
        """Check if a specific model is available locally.
        
        Args:
            model_name: Name of the Ollama model to check
            
        Returns:
            bool: True if model is available, False otherwise
        """
        try:
            response = await self._client.get(f"{self.base_url}/api/tags")
            models = response.json().get("models", [])
            return any(model["name"] == model_name for model in models)
        except Exception as e:
            logger.error(f"Failed to check model availability: {e}")
            return False
            
    async def ensure_models_available(self) -> None:
        """Ensure all required models are available, pulling them if necessary."""
        models = [self.vision_model, self.text_model, self.embedding_model]
        
        for model in models:
            if not await self._check_model_availability(model):
                logger.info(f"Pulling model: {model}")
                try:
                    await self._client.post(f"{self.base_url}/api/pull", json={"name": model})
                except Exception as e:
                    logger.error(f"Failed to pull model {model}: {e}")
                    raise RuntimeError(f"Could not pull required model: {model}")

    async def analyze_image(
        self,
        image_path: Union[str, Path],
        prompt: str,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Analyze an image using the vision model.
        
        Args:
            image_path: Path to the image file
            prompt: Instruction or question about the image
            temperature: Model temperature (0.0 to 1.0)
            
        Returns:
            Dict containing model response and metadata
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        try:
            with open(image_path, 'rb') as img:
                image_data = base64.b64encode(img.read()).decode('utf-8')
                
                payload = {
                    "model": self.vision_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                            "images": [image_data]
                        }
                    ],
                    "stream": False,
                    "temperature": temperature
                }
                
                response = await self._client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Failed to analyze image: {e}")
            raise

    async def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Generate text using the text model.
        
        Args:
            prompt: Input prompt for text generation
            temperature: Model temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            payload = {
                "model": self.text_model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            response = await self._client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            return response.json().get("response", "")
            
        except Exception as e:
            logger.error(f"Failed to generate text: {e}")
            raise

    async def get_embeddings(
        self,
        text: str,
        normalize: bool = True
    ) -> np.ndarray:
        """Generate embeddings for the given text.
        
        Args:
            text: Input text to embed
            normalize: Whether to L2-normalize the embeddings
            
        Returns:
            numpy.ndarray: Embedding vector
        """
        try:
            payload = {
                "model": self.embedding_model,
                "prompt": text,
                "stream": False
            }
            
            response = await self._client.post(
                f"{self.base_url}/api/embeddings",
                json=payload
            )
            response.raise_for_status()
            
            embeddings = np.array(response.json()["embedding"])
            
            if normalize:
                embeddings = embeddings / np.linalg.norm(embeddings)
                
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """Have a conversation using the text model.
        
        Args:
            messages: List of conversation messages in the format:
                     [{"role": "user", "content": "..."}, ...]
            temperature: Model temperature (0.0 to 1.0)
            
        Returns:
            Model's response text
        """
        try:
            payload = {
                "model": self.text_model,
                "messages": messages,
                "temperature": temperature,
                "stream": False
            }
            
            response = await self._client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json().get("response", "")
            
        except Exception as e:
            logger.error(f"Failed to get chat response: {e}")
            raise

    async def close(self):
        """Close the HTTP client session."""
        await self._client.aclose() 