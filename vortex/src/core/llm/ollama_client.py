"""
Ollama LLM client integration for local testing.
"""
from typing import Optional, Dict, Any
import requests
import json
import time

class ModelLoadError(Exception):
    """Raised when model loading fails."""
    pass

class GenerationError(Exception):
    """Raised when text generation fails."""
    pass

class OllamaClient:
    """Client for interacting with local Ollama models."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        base_url: str = "http://localhost:11434",
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize Ollama client.

        Args:
            model_name: Name of model to use. If None, uses llama3.1:8b.
            base_url: Ollama server URL.
            max_retries: Maximum number of retries for generation.
            retry_delay: Delay between retries in seconds.
        """
        self.model_name = model_name or "llama3.1:8b"
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Test connection
        self._test_connection()

    def _test_connection(self):
        """Test connection to Ollama server."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ModelLoadError(f"Ollama server not accessible: {response.status_code}")

            # Check if our model is available
            available_models = [model['name'] for model in response.json()['models']]
            if not any(self.model_name in model for model in available_models):
                print(f"Warning: Model '{self.model_name}' not found. Available models: {available_models}")

        except requests.exceptions.RequestException as e:
            raise ModelLoadError(f"Cannot connect to Ollama server at {self.base_url}: {str(e)}")

    def generate(
        self,
        prompt: str,
        max_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 50,
        num_return_sequences: int = 1,
        stop_sequences: Optional[list[str]] = None,
        **kwargs
    ) -> str:
        """Generate text using Ollama model with retries.

        Args:
            prompt: Input text to generate from.
            max_length: Maximum length of generated text.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            top_k: Top-k sampling parameter.
            num_return_sequences: Number of sequences to generate.
            stop_sequences: Sequences to stop generation at.
            **kwargs: Additional generation parameters.

        Returns:
            Generated text response.

        Raises:
            GenerationError: If generation fails after retries.
        """
        for attempt in range(self.max_retries):
            try:
                return self._generate_once(
                    prompt,
                    max_length,
                    temperature,
                    top_p,
                    top_k,
                    num_return_sequences,
                    stop_sequences,
                    **kwargs
                )
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise GenerationError(f"Generation failed after {self.max_retries} attempts: {str(e)}")
                time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff

    def _generate_once(
        self,
        prompt: str,
        max_length: int,
        temperature: float,
        top_p: float,
        top_k: int,
        num_return_sequences: int,
        stop_sequences: Optional[list[str]],
        **kwargs
    ) -> str:
        """Single generation attempt."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_length,
                "stop": stop_sequences or []
            }
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=60  # Long timeout for generation
        )

        if response.status_code != 200:
            raise GenerationError(f"Ollama API error: {response.status_code} - {response.text}")

        result = response.json()
        generated_text = result.get('response', '')

        # Clean up the response
        generated_text = generated_text.strip()

        return generated_text

    def __call__(self, prompt: str, **kwargs) -> str:
        """Convenience method to call generate."""
        return self.generate(prompt, **kwargs)
