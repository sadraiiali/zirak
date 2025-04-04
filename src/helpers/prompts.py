import os
from pathlib import Path
from src.logger import get_logger

# Set up logger
logger = get_logger("prompts")

# Dictionary to store prompts in memory
PROMPTS = {}

def _load_all_prompts():
    """Load all prompts from the prompts directory into memory."""
    global PROMPTS
    prompts_dir = Path(__file__).parent.parent / "prompts"
    
    if not prompts_dir.exists() or not prompts_dir.is_dir():
        logger.error(f"Prompts directory not found: {prompts_dir}")
        return

    for prompt_file in prompts_dir.glob("*.txt"):
        name = prompt_file.stem
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                PROMPTS[name] = f.read()
            logger.debug(f"Loaded prompt: {name}")
        except Exception as e:
            logger.error(f"Error loading prompt '{name}': {e}")

# Load all prompts into memory when the module is initialized
_load_all_prompts()

def get_prompt(name):
    """
    Get a prompt from the in-memory dictionary.
    
    Args:
        name: Name of the prompt (without extension)
        
    Returns:
        The prompt text or None if not found.
    """
    if name in PROMPTS:
        return PROMPTS[name]
    else:
        logger.error(f"Prompt not found in memory: {name}")
        return None
