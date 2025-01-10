from typing import Optional, Dict, Any
import requests
import logging
from functools import lru_cache
import json

logger = logging.getLogger(__name__)

class VisionLLMService:
    """Service for interacting with locally hosted Llama 3.2 Vision model via Ollama."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3.2-vision"
        
    def _check_ollama_health(self) -> bool:
        """Check if Ollama service is running and healthy."""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
            
    @lru_cache(maxsize=100)
    def analyze_image(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """Analyze an image using the vision model.
        
        Args:
            image_path: Path to the image file
            prompt: Instruction or question about the image
            
        Returns:
            Dict containing model response and metadata
        """
        if not self._check_ollama_health():
            raise RuntimeError("Ollama service is not available")
            
        try:
            with open(image_path, 'rb') as img:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "image": img.read(),
                    "stream": False
                }
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
        except (IOError, requests.RequestException) as e:
            logger.error(f"Failed to analyze image: {e}")
            raise
            
    def get_visual_guidance(self, image_path: str, context: str) -> str:
        """Get spiritual/mystical guidance based on visual input.
        
        Args:
            image_path: Path to the image file
            context: Additional context about the spiritual question or situation
            
        Returns:
            Guidance text from the model
        """
        prompt = f"""As a spiritual guide, analyze this image in the context of: {context}
                    Provide mystical insights and guidance while maintaining the game's atmosphere."""
        
        try:
            response = self.analyze_image(image_path, prompt)
            return response.get("response", "")
        except Exception as e:
            logger.error(f"Failed to get visual guidance: {e}")
            return "I am unable to provide guidance at this moment. Please try again later." 