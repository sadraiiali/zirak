import sys
import asyncio
from cleo.commands.command import Command
from cleo.helpers import option
from src.logger import get_logger
import traceback

logger = get_logger("run_bot")

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



class RunBotCommand(Command):
    name = "bot"
    description = "Start the Zirak bot with notification polling"
    options = [
        option(
            "debug",
            "d",
            description="Enable debug mode with additional output",
            flag=True
        ),
    ]
    
    def handle(self):
        """Start the bot with notification polling"""
        self.line("<info>Starting Zirak bot...</info>")
        try:
            # Import run_bot function here to avoid loading dependencies
            # until the command is actually executed
            asyncio.run(run_bot())
            return 0
        except Exception as e:
            self.line(f"<error>Error: {e}</error>")
            return 1

# For backward compatibility
def main():
    command = RunBotCommand()
    return command.run([])

if __name__ == "__main__":
    sys.exit(main())
