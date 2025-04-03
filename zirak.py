import asyncio
import sys
import traceback
from src.mastodon.mastodon_client import MastodonClient
from src.notifications import notification_handler
from src.logger import get_logger

# Set up logger
logger = get_logger("main")

async def async_main():
    """Async version of main for handling notification polling"""
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
        
        logger.error("\nAuthentication failed. You can run './check_auth.py' to diagnose issues.")
        logger.error("If the access token is invalid, you may need to regenerate it in your Mastodon settings.")
        
        sys.exit(1)

def main():
    """Entry point that runs the async main function"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
