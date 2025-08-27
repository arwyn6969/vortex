"""
Deepseek-R1 LLM client integration.
"""
from typing import Optional, Dict, Any
import os
import time
from functools import lru_cache
# Make transformers and torch optional to avoid import errors at import time
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM = None
    AutoTokenizer = None

try:
    import torch
except ImportError:
    class _DummyCuda:
        @staticmethod
        def is_available():
            return False

    class _DummyTorch:
        cuda = _DummyCuda()

    torch = _DummyTorch()

class ModelLoadError(Exception):
    """Raised when model loading fails."""
    pass

class GenerationError(Exception):
    """Raised when text generation fails."""
    pass

class DeepseekClient:
    """Client for interacting with Deepseek-R1 70B model."""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        model_config: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """Initialize Deepseek-R1 model and tokenizer.
        
        Args:
            model_name: Name/path of model to load. If None, uses default.
            model_config: Additional model configuration.
            max_retries: Maximum number of retries for generation.
            retry_delay: Delay between retries in seconds.
        """
        self.model_name = model_name or os.getenv("DEEPSEEK_MODEL", "deepseek-ai/deepseek-r1-70b")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        try:
            # Stringify the model_config for caching to avoid unhashable dict error
            config_str = repr(model_config or {})
            self._load_model(config_str)
        except Exception as e:
            raise ModelLoadError(f"Failed to load model: {str(e)}")
    
    @lru_cache(maxsize=1)
    def _load_model(self, config_str: str) -> None:
        """Load model and tokenizer with caching.
        
        Args:
            config_str: Stringified config for cache key.
        """
        config = eval(config_str) if config_str else {}
        
        # 70B model specific configurations
        model_config = {
            "device_map": "auto",
            "trust_remote_code": True,
            "use_flash_attention_2": True,  # Enable flash attention for better memory efficiency
            "max_memory": {0: "24GiB"},  # Adjust based on available GPU memory
            **config
        }
        # Set torch_dtype if supported, avoid errors when torch is dummy
        try:
            dtype = torch.bfloat16 if (self.device == "cuda" and hasattr(torch, 'bfloat16')) else torch.float32
            model_config["torch_dtype"] = dtype
        except Exception:
            # Torch does not support dtype attributes in dummy mode
            pass
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            use_fast=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            **model_config
        )
        
    def generate(
        self,
        prompt: str,
        max_length: int = 2048,  # Increased for 70B model
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 50,
        num_return_sequences: int = 1,
        stop_sequences: Optional[list[str]] = None,
        **kwargs
    ) -> str:
        """Generate text using Deepseek-R1 model with retries.
        
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
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # 70B optimized generation config
        generation_config = {
            "max_length": max_length,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "num_return_sequences": num_return_sequences,
            "pad_token_id": self.tokenizer.eos_token_id,
            "do_sample": True,
            "use_cache": True,
            "repetition_penalty": 1.1,  # Slight penalty for repetition
            **kwargs
        }
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs, **generation_config)
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response[len(prompt):].strip()
        
        if stop_sequences:
            for stop_seq in stop_sequences:
                if stop_seq in response:
                    response = response[:response.index(stop_seq)]
        
        return response.strip()
    
    def __call__(self, prompt: str, **kwargs) -> str:
        """Convenience method to call generate."""
        return self.generate(prompt, **kwargs) 