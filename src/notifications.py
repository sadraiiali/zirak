from src.logger import get_logger

# Set up logger
logger = get_logger("notifications")

# Define a notification callback function
async def notification_handler(event_type, notification_data, done_callback):
    """
    Example callback function for processing notifications
    
    Args:
        event_type: Type of notification (mention, follow, favourite, reblog, etc.)
        notification_data: Full notification data from Mastodon
        done_callback: Function to call to mark notification as processed
    """
    account = notification_data.get('account', {})
    username = account.get('acct', 'unknown')
    
    try:
        if event_type == 'mention':
            status = notification_data.get('status', {})
            content = status.get('content', '')
            logger.info(f"CALLBACK: New mention from @{username}: {content[:50]}...")
            
            # Example of how you could respond to specific keywords
            if 'help' in content.lower():
                logger.info("CALLBACK: Help request detected, preparing response...")
                # You could trigger a response here
                
            else:
                # For other mentions, we might want to keep them for manual review
                logger.info("CALLBACK: Keeping mention notification for review")

            # Mark the notification as done after handling it
            done_callback()

        elif event_type == 'follow':
            logger.info(f"CALLBACK: New follower: @{username}!")
            # Maybe send them a welcome message
            
            # Mark as done after processing
            done_callback()
        
        elif event_type == 'favourite':
            logger.info(f"CALLBACK: @{username} favorited your post!!")
            # Auto-dismiss favorites
            done_callback()
        
        elif event_type == 'reblog':
            logger.info(f"CALLBACK: @{username} boosted your post")
            # Auto-dismiss boosts
            done_callback()
        
        else:
            # For other notification types, mark as done
            logger.info(f"CALLBACK: Received {event_type} notification, marking as done")
            done_callback()
            
    except Exception as e:
        logger.error(f"Error in notification handler: {e}")
