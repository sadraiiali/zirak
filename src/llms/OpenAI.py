import os
import sys
from typing import Dict, List, Generator, Union, Optional, Any

from .General import LLMBase

class OpenAI(LLMBase):
    """Implementation of LLMBase for OpenAI."""
    
    def __init__(self, 
                 config_path: str = 'openai_models.yml',
                 api_key: Optional[str] = None):
        """
        Initialize the OpenAI interface.
        
        Args:
            config_path (str, optional): Path to model configuration file
            api_key (str, optional): OpenAI API key
        """
        super().__init__(config_path)
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        # These will be imported during initialization
        self.openai = None
        self.ChatCompletion = None
        
    def initialize(self) -> bool:
        """
        Initialize the connection to OpenAI.
        
        Returns:
            bool: True if initialization is successful, False otherwise
        """
        try:
            # Load environment variables
            try:
                from dotenv import load_dotenv
                load_dotenv()  # Load variables from .env file
            except ImportError:
                print("Warning: python-dotenv not installed. Environment variables must be set manually.")
            
            # Import OpenAI SDK
            try:
                import openai
                self.openai = openai
            except ImportError:
                print("Please install the required library: pip install openai")
                return False
            
            # Set API key
            if not self.api_key:
                self.api_key = os.getenv('OPENAI_API_KEY')
                
            if not self.api_key:
                print("Error: OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass as parameter.")
                return False
                
            self.openai.api_key = self.api_key
            
            # Load models configuration
            if self.config_path:
                try:
                    self.models = self._load_configuration(self.config_path)
                    print(f"Loaded {len(self.models)} models from configuration file")
                except Exception as e:
                    print(f"Error loading model configuration: {e}")
            
            # Use default models if none were loaded
            if not self.models:
                print("Creating default model configuration")
                self.models = {
                    "gpt-3.5-turbo": {
                        "description": "Fast and efficient for most tasks",
                        "max_tokens": 4096
                    },
                    "gpt-4o": {
                        "description": "Advanced model with higher reasoning capabilities",
                        "max_tokens": 8192
                    },
                    "gpt-4o-mini": {
                        "description": "Smaller, more efficient version of GPT-4o",
                        "max_tokens": 4096
                    }
                }
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"Error initializing OpenAI: {e}")
            return False
    
    def list_available_models(self) -> List[str]:
        """
        Returns a list of available model names from the loaded configuration.
        
        Returns:
            List[str]: Names of available models
        """
        return list(self.models.keys())
    
    def chat(
        self,
        model_name: str,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        conversation: List[Dict[str, str]] = None,
        temperature: float = 0.8,
        stream: bool = True,
        params: Dict[str, Any] = None
    ) -> Union[str, Generator[str, None, None]]:
        """
        Chat with an OpenAI model.
        
        Args:
            model_name (str): Name of the model to use
            prompt (str): The primary user prompt
            system_prompt (str): System instructions for the model
            conversation (List[Dict]): Optional conversation history with role/content format
            temperature (float): Controls randomness in generation (0.0-1.0)
            stream (bool): Whether to stream the response
            params (Dict[str, Any]): Additional parameters for the model, can include:
                - max_tokens (int): Maximum number of tokens to generate
                - top_p (float): Controls diversity via nucleus sampling
                - frequency_penalty (float): Decreases repetition of token sequences
                - presence_penalty (float): Increases likelihood of new topics
                - stop (List[str]): Stop generation at these sequences
                - n (int): Number of completions to generate
                - response_format (Dict): Format to structure responses
            
        Returns:
            Union[str, Generator[str, None, None]]: Model response
            
        Raises:
            ValueError: If the specified model_name is not found
        """
        if not self.initialized:
            success = self.initialize()
            if not success:
                raise RuntimeError("Failed to initialize OpenAI")
        
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Available models: {self.list_available_models()}")
        
        # Extract parameters or use defaults
        params = params or {}
        max_tokens = params.get('max_tokens', self.models[model_name].get("max_tokens", 2048))
        top_p = params.get('top_p', 0.9)
        frequency_penalty = params.get('frequency_penalty', 0.0)
        presence_penalty = params.get('presence_penalty', 0.0)
        stop = params.get('stop', None)
        n = params.get('n', 1)
        response_format = params.get('response_format', None)
        
        # Format messages for OpenAI
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history if provided
        if conversation:
            messages.extend(conversation)
        else:
            # Just add the user prompt if no conversation
            messages.append({"role": "user", "content": prompt})
        
        try:
            # Create the completion parameters
            completion_params = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stream": stream,
                "n": n
            }
            
            # Add optional parameters
            if stop:
                completion_params["stop"] = stop
            if response_format:
                completion_params["response_format"] = response_format
            
            if stream:
                # Return a generator for streaming responses
                return self._chat_stream(completion_params)
            else:
                # Return the full response at once
                response = self.openai.chat.completions.create(**completion_params)
                return response.choices[0].message.content
                
        except Exception as e:
            if stream:
                def error_generator():
                    yield f"Error: {str(e)}"
                return error_generator()
            else:
                return f"Error: {str(e)}"
    
    def _chat_stream(self, completion_params: Dict[str, Any]) -> Generator[str, None, None]:
        """
        Stream chat responses from OpenAI.
        
        Args:
            completion_params (Dict[str, Any]): Parameters for the chat completion
            
        Yields:
            str: Text chunks from the model response
        """
        try:
            response_stream = self.openai.chat.completions.create(**completion_params)
            
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Stream Error: {str(e)}"

# Example usage demo
if __name__ == "__main__":
    # Create and initialize OpenAI interface
    openai_client = OpenAI()
    if not openai_client.initialize():
        print("Failed to initialize OpenAI")
        sys.exit(1)
    
    # Show available models
    print("Available models:")
    for model in openai_client.list_available_models():
        print(f" - {model}")
    
    # Select first available model
    available_models = openai_client.list_available_models()
    if not available_models:
        print("No models available!")
        sys.exit(1)
        
    model_name = available_models[0]
    
    # Example prompt
    prompt = "Explain quantum computing in simple terms"
    
    print(f"\nChatting with model: {model_name}")
    print(f"Prompt: {prompt}")
    print("\nResponse:")
    
    # Stream the response
    for chunk in openai_client.chat(model_name, prompt):
        print(chunk, end="", flush=True)
    
    print("\n\nDone!")
