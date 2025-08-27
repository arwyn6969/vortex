#!/usr/bin/env python3
"""
Simple test for Ollama client.
"""
import requests
import json

def test_ollama_direct():
    print("🔗 Testing Ollama API directly...")

    # Test basic connectivity
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama is running! Available models: {[m['name'] for m in models.get('models', [])]}")
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("Make sure Ollama is running with: ollama serve")
        return

    # Test text generation
    print("\n🤖 Testing text generation...")
    payload = {
        "model": "llama3.1:8b",
        "prompt": "Say hello as Thoth, the Egyptian god of wisdom.",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.95,
            "num_predict": 100
        }
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '')
            print(f"✅ Generated response: {generated_text[:200]}...")
        else:
            print(f"❌ Generation failed: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Generation request failed: {e}")

if __name__ == "__main__":
    test_ollama_direct()
