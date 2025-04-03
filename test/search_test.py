import os
import sys
import time

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llms.VertexAI import VertexAI

def main():
    """Test Google Search grounding with VertexAI."""
    print("Testing VertexAI with Google Search grounding...")
    
    # Path to credentials
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
    
    # Select a model that supports grounding
    model_name = "gemini-2.5-pro-exp-03-25"  # This model should support grounding
    print(f"Using model: {model_name}")
    
    # Test query that benefits from Google Search
    prompt = "What are the latest developments in quantum computing as of 2024?"
    print(f"User: {prompt}")
    
    # Parameters for Google Search grounding
    params = {
        'use_google_search': True,
        'max_tokens': 1024,
        'top_p': 0.9,
    }
    
    # System prompt that encourages use of search
    system_prompt = "You are a helpful AI assistant with access to Google Search. Use search to provide current information."
    
    print("Assistant (with Google Search): ", end="", flush=True)
    
    try:
        # Try with the params approach
        for chunk in llm.chat(
            model_name,
            prompt,
            system_prompt=system_prompt,
            params=params
        ):
            print(chunk, end="", flush=True)
            time.sleep(0.01)  # Small delay for readability
    except Exception as e:
        print(f"\nError: {e}")
        print("\nFalling back to direct method call...")
        
        # Fall back to calling the grounding method directly
        for chunk in llm._chat_stream_with_grounding(
            model_name,
            prompt,
            system_prompt=system_prompt,
            conversation=None,
            temperature=0.8,
            params=params
        ):
            print(chunk, end="", flush=True)
            time.sleep(0.01)
    
    print("\n\nSearch test complete!")

if __name__ == "__main__":
    main()
