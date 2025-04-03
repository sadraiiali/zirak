import os
import sys
import time
from typing import Dict, List

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llms.VertexAI import VertexAI

def main():
    """Test the VertexAI class with a simple conversation."""
    print("Testing VertexAI...")
    
    # Create VertexAI instance
    # Point to the credentials file in the project root
    credentials_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "data",
        "google-auth.json"
    )
    
    # Initialize VertexAI
    print(f"Using credentials from: {credentials_path}")
    llm = VertexAI(credentials_path=credentials_path)
    
    if not llm.initialize():
        print("Failed to initialize VertexAI")
        return
    
    # List available models
    models = llm.list_available_models()
    print(f"Available models: {models}")
    
    # Select a model (using the first available model by default)
    model_name = models[0] if models else "gemini-1.5-flash-001"
    print(f"Using model: {model_name}")
    
    # Define system prompt
    system_prompt = "You are a knowledgeable and helpful AI assistant that provides concise answers."
    
    # Simple conversation test
    print("\n=== Single prompt test ===")
    prompt = "What's the capital of France?"
    print(f"User: {prompt}")
    
    # Display streaming response
    print("Assistant: ", end="", flush=True)
    for chunk in llm.chat(model_name, prompt, system_prompt=system_prompt):
        print(chunk, end="", flush=True)
        time.sleep(0.01)  # Small delay to simulate real-time display
    print("\n")
    
    # Multi-turn conversation test
    print("\n=== Multi-turn conversation test ===")
    
    # Start with an empty conversation
    conversation = []
    
    # First turn
    prompt = "What's the capital of France?"
    print(f"User: {prompt}")
    
    # Get non-streaming response for first turn
    response = llm.chat(model_name, prompt, system_prompt=system_prompt, stream=False)
    print(f"Assistant: {response}\n")
    
    # Add to conversation history
    conversation.append({"role": "user", "content": prompt})
    conversation.append({"role": "assistant", "content": response})
    
    # Second turn
    prompt = "What's interesting to see there?"
    print(f"User: {prompt}")
    
    # Display streaming response for second turn
    print("Assistant: ", end="", flush=True)
    for chunk in llm.chat(
        model_name, 
        prompt, 
        system_prompt=system_prompt,
        conversation=conversation
    ):
        print(chunk, end="", flush=True)
        time.sleep(0.01)  # Small delay to simulate real-time display
    print("\n")
    
    # Test with Google Search grounding
    print("\n=== Google Search grounding test ===")
    prompt = "What are the latest developments in quantum computing as of 2024?"
    print(f"User: {prompt}")
    
    # Additional parameters including Google Search grounding
    params = {
        'use_google_search': True,
        'max_tokens': 1024,
        'top_p': 0.9,
        'seed': 42  # For deterministic generation
    }
    
    print("Assistant (with Google Search): ", end="", flush=True)
    for chunk in llm.chat(
        model_name,
        prompt,
        system_prompt="You are a helpful AI assistant with access to Google Search. Use search to provide current information.",
        params=params
    ):
        print(chunk, end="", flush=True)
        time.sleep(0.01)  # Small delay to simulate real-time display
    print("\n")
    
    # Test with safety settings adjustment
    print("\n=== Custom safety settings test ===")
    prompt = "Discuss potential ethical concerns in AI development"
    print(f"User: {prompt}")
    
    # Custom safety settings - more permissive
    from google.genai import types
    custom_safety_settings = [
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH", 
            threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT", 
            threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT", 
            threshold="BLOCK_ONLY_HIGH"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT", 
            threshold="BLOCK_ONLY_HIGH"
        ),
    ]
    
    params = {
        'safety_settings': custom_safety_settings,
        'temperature': 0.7
    }
    
    print("Assistant (with custom safety): ", end="", flush=True)
    for chunk in llm.chat(
        model_name,
        prompt,
        system_prompt=system_prompt,
        params=params
    ):
        print(chunk, end="", flush=True)
        time.sleep(0.01)
    print("\n")
    
    print("VertexAI test complete!")

if __name__ == "__main__":
    main()
