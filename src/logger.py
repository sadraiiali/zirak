import logging
import sys
import os
from pathlib import Path
from src.settings import settings

# Define log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

class Logger:
    """Centralized logger for the application"""
    
    def __init__(self, name, level=None, log_to_file=None, log_dir=None):
        """
        Initialize the logger
        
        Args:
            name: Name of the logger (usually module name)
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to log to files as well as console
            log_dir: Directory to store log files (if log_to_file is True)
        """
        self.logger = logging.getLogger(name)
        
        # Get log level from parameters, settings, or default to INFO
        config_level = getattr(settings.logging, "level", "INFO") if hasattr(settings, "logging") else "INFO"
        log_level_name = level or config_level
        log_level = LOG_LEVELS.get(log_level_name.upper(), logging.INFO)
        
        # Set the log level
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers
        self.logger.handlers = []
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        
        # Get log to file setting from parameters, settings, or default to False
        config_log_to_file = getattr(settings.logging, "to_file", False) if hasattr(settings, "logging") else False
        should_log_to_file = log_to_file if log_to_file is not None else config_log_to_file
        
        # Add file handler if requested
        if should_log_to_file:
            # Get log directory from parameters, settings, or default to "logs"
            config_log_dir = getattr(settings.logging, "log_dir", "logs") if hasattr(settings, "logging") else "logs"
            final_log_dir = log_dir or config_log_dir
            
            # Create log directory if it doesn't exist
            base_dir = Path(__file__).parent.parent
            log_path = os.path.join(base_dir, final_log_dir)
            os.makedirs(log_path, exist_ok=True)
            
            # Create file handler
            log_file = os.path.join(log_path, f"{name}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log a critical message"""
        self.logger.critical(message)
    
    def exception(self, message):
        """Log an exception with traceback"""
        self.logger.exception(message)


# Factory function to create loggers
def get_logger(name, level=None, log_to_file=None):
    """
    Get a configured logger
    
    Args:
        name: Logger name (usually module name)
        level: Override default log level
        log_to_file: Override default file logging setting
    
    Returns:
        Logger: Configured logger instance
    """
    # Defaults will be read from settings in the Logger class
    return Logger(name, level=level, log_to_file=log_to_file)
