#!/usr/bin/env python3
"""
Quick test script to debug LLM integration.
"""
import sys
import os

# Add the vortex src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vortex', 'src'))

from guides.llm_dialogue import LLMDialogueGenerator, DialogueContext
from core.user_profiling.profile_matrix import ProfileDimension

def test_llm():
    print("🤖 Testing LLM Integration...")

    # Create a simple dialogue generator
    generator = LLMDialogueGenerator()

    # Create a test context
    context = DialogueContext(
        guide_name="Thoth",
        guide_archetype="wisdom_teacher",
        cultural_system="Egyptian",
        attributes={"wisdom", "knowledge", "writing", "magic"},
        profile={
            ProfileDimension.CONSCIOUSNESS_DEPTH: 0.8,
            ProfileDimension.WISDOM: 0.7,
            ProfileDimension.EMPATHY: 0.6
        },
        interaction_history=[],
        guidance_style={"analytical": 0.8, "mystical": 0.7}
    )

    # Test welcome message
    print("\n📝 Testing welcome message...")
    try:
        welcome = generator.generate_welcome(context)
        print(f"Welcome response: {welcome}")
    except Exception as e:
        print(f"Welcome failed: {e}")

    # Test response generation
    print("\n💬 Testing response generation...")
    try:
        response = generator.generate_response(context, "Hello, wise Thoth!")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Response failed: {e}")

if __name__ == "__main__":
    test_llm()
