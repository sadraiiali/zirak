import os
import sys
from typing import Dict, List, Generator, Union, Optional, Any

from .General import LLMBase

class VertexAI(LLMBase):
    """Implementation of LLMBase for Google Vertex AI."""
    
    def __init__(self, 
                 config_path: str = 'vertex_ai_models.yml',
                 credentials_path: str = 'google-auth.json',
                 project_id: Optional[str] = None,
                 location: str = 'us-central1'):
        """
        Initialize the Vertex AI interface.
        
        Args:
            config_path (str, optional): Path to model configuration file
            credentials_path (str): Path to Google Cloud credentials
            project_id (str, optional): Google Cloud project ID
            location (str): Google Cloud region
        """
        super().__init__(config_path)
        self.credentials_path = credentials_path
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = location or os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        
        # These will be imported during initialization
        self.vertexai = None
        self.GenerativeModel = None
        self.generative_models = None
        self.credentials = None
        self.SAFETY_SETTINGS = None
        
    def initialize(self) -> bool:
        """
        Initialize the connection to Vertex AI.
        
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
            
            # Import Vertex AI SDK
            try:
                import vertexai
                from vertexai.generative_models import GenerativeModel, FinishReason
                import vertexai.preview.generative_models as generative_models
                from google.oauth2 import service_account
                from google.api_core import exceptions as google_api_exceptions
                
                # Add import for genai client for advanced features
                from google import genai
                from google.genai import types
                
                self.vertexai = vertexai
                self.GenerativeModel = GenerativeModel
                self.FinishReason = FinishReason
                self.generative_models = generative_models
                self.google_api_exceptions = google_api_exceptions
                self.genai = genai
                self.genai_types = types
            except ImportError:
                print("Please install the required libraries: pip install google-cloud-aiplatform google-auth google-generativeai")
                return False
            
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
                    "gemini-1.5-flash-001": {
                        "description": "Fast, efficient model for most tasks",
                        "max_tokens": 2048
                    },
                    "gemini-1.5-pro": {
                        "description": "Advanced model with higher reasoning capabilities",
                        "max_tokens": 8192
                    },
                    "gemini-2.5-pro-exp-03-25": {
                        "description": "Experimental model with advanced features",
                        "max_tokens": 8192
                    }
                }
            
            # Initialize credentials
            self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
            
            # Get project ID from credentials if not provided
            if not self.project_id:
                self.project_id = self.credentials.project_id
            
            if not self.project_id:
                print("Error: Unable to determine Google Cloud project ID")
                return False
            
            # Initialize Vertex AI
            print(f"Initializing Vertex AI with project: {self.project_id}, location: {self.location}")
            self.vertexai.init(project=self.project_id, location=self.location, credentials=self.credentials)
            
            # Initialize genai client
            self.genai_client = self.genai.Client(
                vertexai=True,
                project=self.project_id,
                location=self.location,
                credentials=self.credentials
            )
            
            # Setup safety settings
            self.SAFETY_SETTINGS = {
                self.generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: self.generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                self.generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: self.generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                self.generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: self.generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                self.generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: self.generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
            
            # Default genai safety settings
            self.GENAI_SAFETY_SETTINGS = [
                self.genai_types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH", 
                    threshold="BLOCK_MEDIUM_AND_ABOVE"
                ),
                self.genai_types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT", 
                    threshold="BLOCK_MEDIUM_AND_ABOVE"
                ),
                self.genai_types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT", 
                    threshold="BLOCK_MEDIUM_AND_ABOVE"
                ),
                self.genai_types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT", 
                    threshold="BLOCK_MEDIUM_AND_ABOVE"
                ),
            ]
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"Error initializing Vertex AI: {e}")
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
        Chat with a Vertex AI model.
        
        Args:
            model_name (str): Name of the model to use
            prompt (str): The primary user prompt
            system_prompt (str): System instructions for the model
            conversation (List[Dict]): Optional conversation history with role/content format
            temperature (float): Controls randomness in generation (0.0-1.0)
            stream (bool): Whether to stream the response
            params (Dict[str, Any]): Additional parameters for the model, can include:
                - use_google_search (bool): Whether to enable Google Search grounding
                - max_tokens (int): Maximum number of tokens to generate
                - top_p (float): Controls diversity via nucleus sampling
                - top_k (int): Controls diversity via top-k sampling
                - safety_settings (list): Custom safety settings
                - seed (int): Seed for deterministic generation
                - candidate_count (int): Number of candidates to generate
                - stop_sequences (List[str]): Stop generation at these sequences
            
        Returns:
            Union[str, Generator[str, None, None]]: Model response
            
        Raises:
            ValueError: If the specified model_name is not found
        """
        if not self.initialized:
            success = self.initialize()
            if not success:
                raise RuntimeError("Failed to initialize Vertex AI")
        
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Available models: {self.list_available_models()}")
        
        # Extract parameters or use defaults
        params = params or {}
        
        # Determine which implementation to use based on params
        use_google_search = params.get('use_google_search', False)
        
        if use_google_search:
            # Use genai client implementation that supports grounding
            if stream:
                return self._chat_stream_with_grounding(model_name, prompt, system_prompt, conversation, temperature, params)
            else:
                # Collect all chunks from the streaming response
                response = ""
                for chunk in self._chat_stream_with_grounding(model_name, prompt, system_prompt, conversation, temperature, params):
                    response += chunk
                return response
        else:
            # Use standard implementation
            if stream:
                return self._chat_stream(model_name, prompt, system_prompt, conversation, temperature, params)
            else:
                # Collect all chunks from the streaming response
                response = ""
                for chunk in self._chat_stream(model_name, prompt, system_prompt, conversation, temperature, params):
                    response += chunk
                return response
    
    def _chat_stream(
        self,
        model_name: str,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        conversation: List[Dict[str, str]] = None,
        temperature: float = 0.8,
        params: Dict[str, Any] = None
    ) -> Generator[str, None, None]:
        """
        Chat with a Vertex AI model using streaming responses.
        
        Args:
            model_name (str): Name of the model to use
            prompt (str): The primary user prompt
            system_prompt (str): System instructions for the model
            conversation (List[Dict]): Optional conversation history
            temperature (float): Controls randomness (0.0-1.0)
            params (Dict[str, Any]): Additional parameters for the model
            
        Yields:
            str: Text chunks from the model response
        """
        # Extract parameters or use defaults
        params = params or {}
        max_tokens = params.get('max_tokens', self.models[model_name].get("max_tokens", 2048))
        top_p = params.get('top_p', 0.9)
        top_k = params.get('top_k', None)
        
        # Set up generation config
        generation_config = {
            "max_output_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
        }
        
        # Add top_k if provided
        if top_k is not None:
            generation_config["top_k"] = top_k
        
        # Add seed if provided for deterministic output
        if 'seed' in params:
            generation_config["seed"] = params['seed']
        
        try:
            # Load the model
            model = self.GenerativeModel(model_name)
            
            # Format the conversation for Vertex AI
            formatted_messages = []
            
            # If using a new conversation
            if conversation is None:
                # Add system prompt if provided
                if system_prompt:
                    formatted_messages.append({
                        "role": "user",
                        "parts": [{"text": f"System: {system_prompt}"}]
                    })
                
                # Add user prompt
                formatted_messages.append({
                    "role": "user",
                    "parts": [{"text": prompt}]
                })
            else:
                # Add system prompt if provided
                if system_prompt:
                    formatted_messages.append({
                        "role": "user", 
                        "parts": [{"text": f"System: {system_prompt}"}]
                    })
                
                # Add conversation history
                for message in conversation:
                    role = message["role"]
                    # Map to Vertex AI roles (user stays as "user", assistant becomes "model")
                    vertex_role = "model" if role == "assistant" else "user"
                    
                    formatted_messages.append({
                        "role": vertex_role,
                        "parts": [{"text": message["content"]}]
                    })
            
            # Use custom safety settings if provided
            safety_settings = params.get('safety_settings', self.SAFETY_SETTINGS)
            
            # Generate streaming response
            responses = model.generate_content(
                formatted_messages,
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )
            
            # Process and yield each response chunk
            for response_chunk in responses:
                # Check for prompt feedback (like blocking)
                if response_chunk.prompt_feedback and response_chunk.prompt_feedback.block_reason:
                    yield f"Stream Error: Blocked due to safety - {response_chunk.prompt_feedback.block_reason.name}"
                    return

                # Check for empty chunks
                if not response_chunk.candidates:
                    continue
                    
                candidate = response_chunk.candidates[0]
                
                # Check for safety-related finish reason
                if candidate.finish_reason == self.FinishReason.SAFETY:
                    safety_info = " Blocked categories: " + ", ".join([r.category.name for r in candidate.safety_ratings if r.blocked]) if candidate.safety_ratings else ""
                    yield f"\nResponse stopped due to safety concerns.{safety_info}"
                    return
                    
                # Extract and yield text from the chunk
                if candidate.content and candidate.content.parts:
                    chunk_text = "".join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
                    yield chunk_text
        
        except self.google_api_exceptions.InvalidArgument as e:
            yield f"\nAPI Error: Invalid Argument - {e}"
        except self.google_api_exceptions.PermissionDenied as e:
            yield f"\nAPI Error: Permission Denied - {e}"
        except self.google_api_exceptions.ResourceExhausted as e:
            yield f"\nAPI Error: Resource Exhausted - {e}"
        except ValueError as e:
            yield f"\nValue Error: {e}"
        except Exception as e:
            yield f"\nUnexpected Error: {e}"

    def _chat_stream_with_grounding(
        self,
        model_name: str,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        conversation: List[Dict[str, str]] = None,
        temperature: float = 0.8,
        params: Dict[str, Any] = None
    ) -> Generator[str, None, None]:
        """
        Chat with a Vertex AI model using streaming responses with Google Search grounding.
        
        Args:
            model_name (str): Name of the model to use
            prompt (str): The primary user prompt
            system_prompt (str): System instructions for the model
            conversation (List[Dict]): Optional conversation history
            temperature (float): Controls randomness (0.0-1.0)
            params (Dict[str, Any]): Additional parameters for the model
            
        Yields:
            str: Text chunks from the model response
        """
        # Extract parameters or use defaults
        params = params or {}
        max_tokens = params.get('max_tokens', self.models[model_name].get("max_tokens", 2048))
        top_p = params.get('top_p', 0.9)
        top_k = params.get('top_k', None)
        
        try:
            # Prepare contents for genai client
            contents = []
            
            # Add system prompt if provided
            if system_prompt:
                contents.append(self.genai_types.Content(
                    role="user",
                    parts=[{"text": f"System: {system_prompt}"}]
                ))
            
            # If conversation is provided
            if conversation:
                for message in conversation:
                    role = message["role"]
                    # Map to genai roles (user stays as "user", assistant becomes "model")
                    genai_role = "model" if role == "assistant" else "user"
                    
                    contents.append(self.genai_types.Content(
                        role=genai_role,
                        parts=[{"text": message["content"]}]
                    ))
            else:
                # Just add the user prompt if no conversation
                contents.append(self.genai_types.Content(
                    role="user",
                    parts=[{"text": prompt}]
                ))
            
            # Setup tools - always include Google Search if this method is called
            tools = [
                self.genai_types.Tool(google_search=self.genai_types.GoogleSearch()),
            ]
            
            # Setup safety settings
            safety_settings = params.get('safety_settings', self.GENAI_SAFETY_SETTINGS)
            
            # Create generation config
            generation_config = self.genai_types.GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
                response_modalities=["TEXT"],
                safety_settings=safety_settings,
                tools=tools,
            )
            
            # Add seed if provided
            if 'seed' in params:
                generation_config.seed = params['seed']
            
            # Generate content with google search grounding
            response_stream = self.genai_client.models.generate_content_stream(
                model=model_name,
                contents=contents,
                config=generation_config,
            )
            
            # Process and yield each response chunk
            for chunk in response_stream:
                if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                    continue
                    
                yield chunk.text
                
        except Exception as e:
            yield f"\nError with grounding: {str(e)}"

# Example usage demo
if __name__ == "__main__":
    # Create and initialize Vertex AI interface
    vertex = VertexAI()
    if not vertex.initialize():
        print("Failed to initialize Vertex AI")
        sys.exit(1)
    
    # Show available models
    print("Available models:")
    for model in vertex.list_available_models():
        print(f" - {model}")
    
    # Select first available model
    available_models = vertex.list_available_models()
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
    for chunk in vertex.chat(model_name, prompt):
        print(chunk, end="", flush=True)
    
    print("\n\nDone!")
