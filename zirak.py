import sys
import os
import glob
import importlib.util
from cleo.application import Application
from src.logger import get_logger

# Set up logger
logger = get_logger("main")

def load_commands(application):
    """Dynamically load all commands from the src/commands directory"""
    commands_dir = os.path.join(os.path.dirname(__file__), 'src', 'commands')
    command_files = glob.glob(os.path.join(commands_dir, "*.py"))
    
    for command_file in command_files:
        if os.path.basename(command_file) == '__init__.py':
            continue
            
        module_name = os.path.basename(command_file).replace('.py', '')
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, command_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Look for Command classes in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            # Check if it's a Command class but not the base Command class
            if (isinstance(attr, type) and 
                'Command' in attr_name and 
                attr.__module__ == module.__name__):
                try:
                    application.add(attr())
                    logger.debug(f"Loaded command: {attr_name}")
                except Exception as e:
                    logger.error(f"Failed to load command {attr_name}: {e}")

def main():
    """Entry point that handles CLI commands and running the bot"""
    # Initialize Cleo application
    application = Application(name="zirak", version="1.0.0")
    
    # Load commands from src/commands directory
    load_commands(application)
    
    # Check for the "run" command pattern
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        if len(sys.argv) == 2:
            # No task specified, show help for run command
            sys.argv = [sys.argv[0], "run"]
        else:
            # Extract the task and any additional arguments
            task = sys.argv[2]
            # Keep the original command structure for the run command to process
    
    # Run the Cleo application
    exit_code = application.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
