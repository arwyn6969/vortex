# Vortex AI Setup Guide

This guide explains how to set up and use the AI models in the Vortex of Enlightenment game.

## Prerequisites

1. Install Ollama:
```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Model Setup

The game uses three main models:

1. **llama3.2-vision**: For visual analysis and interpretation
2. **hermes3**: For general text generation and spiritual guidance
3. **mxbai-embed-large**: For generating embeddings and semantic analysis

Pull all required models:
```bash
ollama pull llama3.2-vision
ollama pull hermes3
ollama pull mxbai-embed-large
```

## Usage Examples

### Basic Usage

```python
from vortex.src.core.ai.model_service import VortexAI
import asyncio

async def main():
    # Initialize the AI service
    ai = VortexAI()
    
    # Ensure all models are available
    await ai.ensure_models_available()
    
    try:
        # Vision Analysis
        vision_result = await ai.analyze_image(
            "path/to/sacred_geometry.jpg",
            "Describe the spiritual significance of this pattern"
        )
        print("Vision Analysis:", vision_result)
        
        # Text Generation
        text_response = await ai.generate_text(
            "Explain the mystical meaning of the number 7",
            temperature=0.7
        )
        print("Generated Text:", text_response)
        
        # Get Embeddings
        embeddings = await ai.get_embeddings(
            "This is a spiritual text about consciousness"
        )
        print("Embeddings shape:", embeddings.shape)
        
        # Chat Conversation
        chat_response = await ai.chat([
            {"role": "system", "content": "You are a mystical guide"},
            {"role": "user", "content": "What is the Tree of Life?"}
        ])
        print("Chat Response:", chat_response)
        
    finally:
        # Clean up
        await ai.close()

# Run the example
asyncio.run(main())
```

### Advanced Usage

#### Custom Temperature Settings

```python
# More deterministic responses
response = await ai.generate_text(
    "Explain karma",
    temperature=0.3  # Lower temperature for more focused responses
)

# More creative responses
response = await ai.generate_text(
    "Create a mystical meditation",
    temperature=0.9  # Higher temperature for more creative responses
)
```

#### Batch Processing

```python
async def process_images(image_paths: List[str], prompt: str):
    ai = VortexAI()
    try:
        tasks = [ai.analyze_image(path, prompt) for path in image_paths]
        results = await asyncio.gather(*tasks)
        return results
    finally:
        await ai.close()
```

#### Error Handling

```python
try:
    response = await ai.generate_text("Query")
except Exception as e:
    logger.error(f"AI generation failed: {e}")
    # Implement fallback behavior
```

## Model Specifications

### llama3.2-vision
- Purpose: Visual analysis and interpretation
- Input: Images + text prompts
- Output: Detailed textual analysis
- Best for: Sacred geometry analysis, artistic interpretation

### hermes3
- Purpose: Text generation and conversation
- Input: Text prompts or chat messages
- Output: Natural language responses
- Best for: Spiritual guidance, mystical explanations

### mxbai-embed-large
- Purpose: Text embeddings
- Input: Text strings
- Output: High-dimensional vectors
- Best for: Semantic search, content similarity

## Performance Considerations

1. **Memory Usage**:
   - llama3.2-vision: ~8GB RAM
   - hermes3: ~4GB RAM
   - mxbai-embed-large: ~2GB RAM

2. **Response Times**:
   - Vision analysis: 2-5 seconds
   - Text generation: 1-3 seconds
   - Embeddings: <1 second

3. **Optimization Tips**:
   - Use appropriate temperature settings
   - Implement caching for repeated queries
   - Close AI service when not in use
   - Consider batch processing for multiple requests

## Troubleshooting

Common issues and solutions:

1. **Model Not Found**:
   ```bash
   ollama pull [model_name]  # Re-pull the model
   ```

2. **Out of Memory**:
   - Close other applications
   - Reduce batch sizes
   - Process images sequentially

3. **Slow Responses**:
   - Check system resources
   - Reduce image sizes
   - Implement request queuing

4. **Connection Errors**:
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   
   # Restart Ollama
   sudo systemctl restart ollama  # Linux
   brew services restart ollama   # macOS
   ```

## Security Considerations

1. **API Access**:
   - Ollama runs locally by default
   - No external API keys needed
   - Consider firewall rules if needed

2. **Data Privacy**:
   - All processing happens locally
   - No data sent to external services
   - Implement access controls as needed

## Maintenance

1. **Updating Models**:
   ```bash
   ollama pull llama3.2-vision:latest
   ollama pull hermes3:latest
   ollama pull mxbai-embed-large:latest
   ```

2. **Cleaning Up**:
   ```bash
   # Remove unused models
   ollama rm [model_name]
   
   # List installed models
   ollama list
   ```

## Support

For issues or questions:
1. Check the Ollama documentation: https://ollama.ai/docs
2. Review the game's issue tracker
3. Contact the development team 