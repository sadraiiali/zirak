import os
import sys
from typing import Dict, List, Generator, Union, Any, Optional
from abc import ABC, abstractmethod

class LLMBase(ABC):
    """Base class for Large Language Model interfaces."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the LLM interface.
        
        Args:
            config_path (str, optional): Path to configuration file
        """
        self.config_path = config_path
        self.models = {}
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the connection to the LLM service.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_available_models(self) -> List[str]:
        """
        List available models for this LLM service.
        
        Returns:
            List[str]: Names of available models
        """
        pass
    
    @abstractmethod
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
        Send a chat request to the LLM.
        
        Args:
            model_name (str): Name of the model to use
            prompt (str): The primary user prompt
            system_prompt (str): System instructions for the model
            conversation (List[Dict]): Optional conversation history with role/content format
            temperature (float): Controls randomness in generation (0.0-1.0)
            stream (bool): Whether to stream the response
            params (Dict[str, Any]): Additional parameters for the model
            
        Returns:
            Union[str, Generator[str, None, None]]: Model response as string or generator
        """
        pass
    
    def _load_configuration(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a file.
        
        Args:
            config_path (str): Path to configuration file
            
        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        try:
            import yaml
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except ImportError:
            print("Warning: PyYAML not installed. Using default configuration.")
            return {}
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return {}

class GeneralLLM(LLMBase):
    def is_extensive_research(self, prompt):
        """
        Determine if a prompt requires extensive research based on:
        - Length of prompt
        - Complexity (presence of multiple questions)
        - Explicit request for detailed research
        
        Args:
            prompt (str): The user prompt
            
        Returns:
            bool: True if extensive research is needed
        """
        # Check for explicit research requests
        research_keywords = [
            "research", "investigate", "detailed analysis", 
            "comprehensive", "in-depth", "thorough"
        ]
        
        if any(keyword in prompt.lower() for keyword in research_keywords):
            return True
            
        # Check for complexity based on question count
        question_count = prompt.count("?")
        if question_count >= 3:
            return True
            
        # Check for length - long prompts often need detailed responses
        if len(prompt) > 300:  # Arbitrary threshold
            return True
            
        return False
