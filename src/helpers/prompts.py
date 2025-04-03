import os
from pathlib import Path
from src.logger import get_logger

# Set up logger
logger = get_logger("prompts")

def get_prompt(name):
    """
    Get a prompt from the prompts directory
    
    Args:
        name: Name of the prompt file (without extension)
        
    Returns:
        The prompt text or None if the file doesn't exist
    """
    # Get the absolute path to the prompts directory
    prompts_dir = Path(__file__).parent.parent / "prompts"
    prompt_path = prompts_dir / f"{name}.txt"
    
    try:
        if not prompt_path.exists():
            logger.error(f"Prompt file not found: {prompt_path}")
            return None
            
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        logger.debug(f"Loaded prompt: {name}")
        return content
    except Exception as e:
        logger.error(f"Error loading prompt '{name}': {e}")
        return None
