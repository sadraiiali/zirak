import asyncio
import sys
import traceback
import os
import glob
import importlib.util
from cleo.application import Application
from src.logger import get_logger

# Set up logger
logger = get_logger("main")

async def run_bot():
    """Run the bot with notification polling"""
    # Import here to avoid triggering initialization when just showing help
    from src.mastodon.mastodon_client import MastodonClient
    from src.notifications import notification_handler
    
    logger.info("Hello from zirak!")
    
    try:
        # Initialize the Mastodon client
        logger.info("Initializing Mastodon client...")
        client = MastodonClient()
        
        # Test the connection by fetching account info
        account = client.mastodon.account_verify_credentials()
        logger.info(f"Connected as: @{account.username}")
        
        # # Example: Post a status
        # logger.info("Posting a test status...")
        # status = client.post_status("Hello world from zirak_ai!")
        
        # if status:
        #     logger.info(f"Successfully posted status: {status['url']}")
        # else:
        #     logger.warning("Failed to post status")
        
        # Example: Check notifications
        logger.info("Checking notifications...")
        notifications = client.check_notifications()
        
        # Show a summary of notifications
        if notifications:
            mention_count = sum(1 for n in notifications if n['type'] == 'mention')
            favorite_count = sum(1 for n in notifications if n['type'] == 'favourite')
            reblog_count = sum(1 for n in notifications if n['type'] == 'reblog')
            
            logger.info(f"You have: {mention_count} mentions, {favorite_count} favorites, {reblog_count} reblogs")
        
        # Start notification polling with our custom handler
        logger.info("Starting notification polling...")
        await client.start_notification_polling(notification_handler=notification_handler)
        
        # Keep the main task running to allow the polling to work
        logger.info("Polling active. Press Ctrl+C to stop.")
        try:
            # Run indefinitely until interrupted
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nStopping notification polling...")
            await client.stop_notification_polling()
            logger.info("Polling stopped.")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        traceback.print_exc()
        
        logger.error("\nAuthentication failed. You can run 'zirak check-auth' to diagnose issues.")
        logger.error("If the access token is invalid, you may need to regenerate it in your Mastodon settings.")
        
        sys.exit(1)

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
    
    # Run the Cleo application
    exit_code = application.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
