"""
Example script demonstrating the new guide interaction system.
"""

import asyncio
import json
from src.core.ai_service import AIService, ModelConfig, ModelProvider
from src.guides.dialogue import (
    DialogueManager,
    DialogueContext,
    GuidePersona,
    GuidanceStyle
)

async def main():
    """Run the guide interaction example."""
    
    # Initialize AI service
    config = ModelConfig(
        provider=ModelProvider.OLLAMA,
        model_name="hermes3",
        api_base="http://localhost:11434"
    )
    ai_service = AIService(default_config=config)
    
    # Create a guide persona
    thoth = GuidePersona(
        name="Thoth",
        tradition="Egyptian",
        style=GuidanceStyle.WISE,
        description="Ancient Egyptian god of wisdom and knowledge",
        key_traits=["wise", "scholarly", "mystical", "precise"]
    )
    
    # Create dialogue context
    context = DialogueContext(
        guide=thoth,
        user_profile={
            "wisdom": 0.7,
            "intuition": 0.6,
            "knowledge": 0.8
        },
        conversation_history=[],
        current_location="Library of Ancient Wisdom",
        current_quest="Seeking the Emerald Tablets"
    )
    
    # Initialize dialogue manager
    dialogue_manager = DialogueManager(ai_service)
    
    try:
        # Get welcome message
        print("\nInitiating conversation with Thoth...\n")
        welcome = await dialogue_manager.generate_welcome(context)
        print(f"Thoth: {welcome}\n")
        
        # Demonstrate regular response
        user_message = "What wisdom can you share about the nature of knowledge?"
        print(f"User: {user_message}\n")
        
        response = await dialogue_manager.generate_response(context, user_message)
        print(f"Thoth: {response}\n")
        
        # Update conversation history
        context.conversation_history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response}
        ])
        
        # Demonstrate streaming response
        user_message = "How can I decode the wisdom in the Emerald Tablets?"
        print(f"User: {user_message}\n")
        print("Thoth: ", end="", flush=True)
        
        async for chunk in await dialogue_manager.generate_response(
            context,
            user_message,
            stream=True
        ):
            print(chunk, end="", flush=True)
        print("\n")
        
        # Get quest guidance
        print("Seeking guidance on current quest...")
        guidance = await dialogue_manager.generate_quest_guidance(
            context,
            "Find and understand the Emerald Tablets of Thoth",
            0.3
        )
        print(f"\nThoth's Quest Guidance: {guidance}\n")
        
        # Get location insight
        print("Seeking insight about current location...")
        insight = await dialogue_manager.generate_location_insight(
            context,
            "The Library of Ancient Wisdom, filled with scrolls and mystical artifacts",
            ["Emerald Tablet fragments", "Astrolabe of Time", "Mirror of Truth"]
        )
        print(f"\nThoth's Location Insight: {insight}\n")
        
    finally:
        await ai_service.close()

if __name__ == "__main__":
    asyncio.run(main()) 