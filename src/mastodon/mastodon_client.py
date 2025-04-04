import asyncio
from mastodon import Mastodon
from src.settings import settings
from src.logger import get_logger
import re

class MastodonClient:
    def __init__(self):
        # Set up logging
        self.logger = get_logger("mastodon_client")
        
        # Application credentials from secure environment
        self.client_id = settings.credentials.client_id.get_secret_value()
        self.client_secret = settings.credentials.client_secret.get_secret_value()
        self.access_token = settings.credentials.access_token.get_secret_value()
        
        # Instance URL from config
        self.api_base_url = settings.mastodon.instance_url
        self.alt_instances = settings.mastodon.alt_instances
        
        # Initialize the API client
        self.mastodon = self._initialize_client()
        
        # Notification polling
        self.polling_active = False
        self.polling_task = None
        self.latest_notification_id = None
        self.notification_callback = None
    
    def _initialize_client(self):
        """Initialize the Mastodon API client using credentials"""
        try:
            self.logger.info("Creating a new Mastodon client directly...")
            
            # Create a Mastodon client with the primary instance
            mastodon = self._create_client(self.api_base_url)
            
            # Try to authenticate with the default instance
            try:
                account = mastodon.account_verify_credentials()
                self.logger.info(f"Authentication successful with access token as @{account.username}")
                return mastodon
            except Exception as e:
                self.logger.error(f"Error with default instance: {e}")
                
                # Try alternate instances from config
                for alt_url in self.alt_instances:
                    self.logger.info(f"Trying alternate instance: {alt_url}")
                    try:
                        alt_mastodon = self._create_client(alt_url)
                        account = alt_mastodon.account_verify_credentials()
                        self.logger.info(f"Authentication successful on {alt_url} as @{account.username}")
                        return alt_mastodon
                    except Exception as e2:
                        self.logger.error(f"Error with {alt_url}: {e2}")
                
                # If we get here, all instances failed
                raise Exception("Failed to authenticate with any Mastodon instance")
            
        except Exception as e:
            self.logger.critical(f"Error creating Mastodon client: {e}")
            raise
    
    def _create_client(self, instance_url):
        """Create a Mastodon client for a specific instance using access token"""
        return Mastodon(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token,
            api_base_url=instance_url
        )
    
    def post_status(self, content, visibility="public", media_ids=None, spoiler_text=None):
        """Post a new status to Mastodon"""
        try:
            status = self.mastodon.status_post(
                status=content,
                media_ids=media_ids,
                visibility=visibility,
                spoiler_text=spoiler_text
            )
            self.logger.info(f"Posted status with ID: {status['id']}")
            return status
        except Exception as e:
            self.logger.error(f"Error posting status: {e}")
            return None
    
    def reply_to_mention(self, mention_status, content, visibility="public", media_ids=None, spoiler_text=None):
        """
        Reply to a mention from another user
        
        Args:
            mention_status: The status object that contains the mention
            content: The content of the reply (will be prefixed with @username)
            visibility: Visibility level ('public', 'unlisted', 'private', 'direct')
            media_ids: Optional list of media IDs to attach
            spoiler_text: Optional content warning
            
        Returns:
            The posted status object or None if there was an error
        """
        try:
            # Extract the account username to reply to
            account = mention_status.get('account', {})
            username = account.get('acct')
            
            if not username:
                self.logger.error("Could not determine username to reply to")
                return None

            # Prepend newline if content starts with a RTL character to fix direction
            rtl_pattern = re.compile('[\u0627-\u064a]|[\u0600-\u06FF]|[\u0590-\u05FF\uFB2A-\uFB4E]')
            if len(re.findall(rtl_pattern, content[0])) > (len(content[0])/2):
                content = f"\n{content}"
            
            # Format the reply to include the username
            formatted_reply = f"@{username} {content}"
            
            # Get the status ID to reply to
            in_reply_to_id = mention_status.get('id')
            
            if not in_reply_to_id:
                self.logger.error("Could not determine status ID to reply to")
                return None
                
            # Post the reply
            status = self.mastodon.status_post(
                status=formatted_reply,
                in_reply_to_id=in_reply_to_id,
                media_ids=media_ids,
                visibility=visibility,
                spoiler_text=spoiler_text
            )
            
            self.logger.info(f"Posted reply to @{username} with ID: {status['id']}")
            return status
            
        except Exception as e:
            self.logger.error(f"Error posting reply: {e}")
            return None
    
    def get_status(self, status_id):
        """
        Fetch a status/post by its ID
        
        Args:
            status_id: The ID of the status to fetch
            
        Returns:
            The status object or None if there was an error
        """
        try:
            status = self.mastodon.status(status_id)
            self.logger.debug(f"Fetched status with ID: {status_id}")
            return status
        except Exception as e:
            self.logger.error(f"Error fetching status {status_id}: {e}")
            return None
    
    def get_thread(self, status_id):
        """
        Fetch an entire thread/conversation containing a status
        
        Args:
            status_id: The ID of the status in the thread
            
        Returns:
            List of statuses in the thread or empty list if there was an error
        """
        try:
            context = self.mastodon.status_context(status_id)
            # The context contains 'ancestors' and 'descendants' lists
            ancestors = context.get('ancestors', [])
            descendants = context.get('descendants', [])
            
            # Get the status itself
            status = self.get_status(status_id)
            
            if status:
                # Construct the full thread in order
                thread = ancestors + [status] + descendants
                self.logger.info(f"Fetched thread with {len(thread)} posts")
                return thread
            else:
                return ancestors + descendants
                
        except Exception as e:
            self.logger.error(f"Error fetching thread for status {status_id}: {e}")
            return []
    
    def get_account(self, account_id):
        """
        Fetch account information by account ID
        
        Args:
            account_id: The ID of the account to fetch
            
        Returns:
            The account object or None if there was an error
        """
        try:
            account = self.mastodon.account(account_id)
            self.logger.debug(f"Fetched account: @{account.get('acct', 'unknown')}")
            return account
        except Exception as e:
            self.logger.error(f"Error fetching account {account_id}: {e}")
            return None
    
    def check_notifications(self, limit=None):
        """Fetch recent notifications"""
        try:
            # Use configured limit if not specified
            if limit is None:
                limit = settings.mastodon.notification_limit
                
            notifications = self.mastodon.notifications(limit=limit)
            self.logger.debug(f"Fetched {len(notifications)} notifications")
            return notifications
        except Exception as e:
            self.logger.error(f"Error fetching notifications: {e}")
            return []
    
    def handle_notification(self, notification):
        """Process a new notification (called from push notification handler)"""
        try:
            notification_type = notification.get('type')
            
            if notification_type == 'mention':
                self.logger.info(f"New mention from @{notification['account']['acct']}")
                # Process the mention
                self._handle_mention(notification)
            
            elif notification_type == 'reblog':
                self.logger.info(f"Your post was boosted by @{notification['account']['acct']}")
            
            elif notification_type == 'favourite':
                self.logger.info(f"Your post was favorited by @{notification['account']['acct']}")
            
            elif notification_type == 'follow':
                self.logger.info(f"New follower: @{notification['account']['acct']}")
            
            else:
                self.logger.info(f"Received notification of type: {notification_type}")
        
        except Exception as e:
            self.logger.error(f"Error handling notification: {e}")
    
    def _handle_mention(self, notification):
        """Handle a mention notification specifically"""
        # Extract the status and account information
        status = notification.get('status', {})
        content = status.get('content', '')
        from_account = notification.get('account', {}).get('acct')
        
        self.logger.info(f"Mention from @{from_account}: {content}")
        
        # Example of how to auto-reply to mentions
        # Uncomment and modify this code to implement auto-replies
        # if "help" in content.lower():
        #     reply_content = "Here's how you can use my services..."
        #     self.reply_to_mention(status, reply_content, visibility="direct")
        # elif "hello" in content.lower() or "hi" in content.lower():
        #     reply_content = "Hello there! How can I assist you today?"
        #     self.reply_to_mention(status, reply_content)
        # else:
        #     # Default response
        #     reply_content = "Thanks for reaching out! I've received your message."
        #     self.reply_to_mention(status, reply_content)
    
    async def start_notification_polling(self, notification_handler=None):
        """
        Start polling for new notifications using the interval from settings
        
        Args:
            notification_handler: Async function to call with (event_type, notification_data) 
                                  when a new notification is received
        """
        if self.polling_active:
            self.logger.warning("Notification polling is already active")
            return False
        
        # Store the callback function
        self.notification_callback = notification_handler
        
        # Get interval from settings
        interval = settings.mastodon.notification_interval
        
        self.polling_active = True
        
        # Initialize the latest notification ID
        try:
            notifications = self.check_notifications(limit=1)
            if notifications:
                self.latest_notification_id = notifications[0]['id']
                self.logger.info(f"Starting notification polling with latest ID: {self.latest_notification_id}")
            else:
                self.logger.info("No initial notifications found")
        except Exception as e:
            self.logger.error(f"Error initializing notification polling: {e}")
        
        # Start the polling as an asyncio task
        self.polling_task = asyncio.create_task(self._notification_polling_loop(interval))
        self.logger.info(f"Notification polling started with interval of {interval} seconds")
        return True
    
    async def _notification_polling_loop(self, interval):
        """
        Asyncio-based polling loop for notifications
        
        Args:
            interval: Time in seconds between polling attempts
        """
        while self.polling_active:
            try:
                # Get recent notifications
                notifications = self.check_notifications(limit=settings.mastodon.notification_limit)
                
                # Process new notifications (if any)
                new_notifications = self._get_new_notifications(notifications)
                if new_notifications:
                    self.logger.info(f"Found {len(new_notifications)} new notifications")
                    # Process each notification in order (oldest first)
                    for notification in reversed(new_notifications):
                        # Always handle internally
                        self.handle_notification(notification)
                        
                        # Call the callback function if provided
                        if self.notification_callback and callable(self.notification_callback):
                            event_type = notification.get('type', 'unknown')
                            notification_id = notification.get('id')
                            
                            # Create a bound method for this specific notification
                            # Using a proper function definition instead of lambda
                            def create_done_callback(notification_id):
                                self.logger.info(f"Notification processed")
                                def done_callback(id=notification_id):
                                    self.logger.debug(f"Notification {id} processed")
                                    return self.notification_done(id)
                                return done_callback
                            
                            try:
                                await self.notification_callback(event_type, notification, create_done_callback(notification_id), self)
                            except Exception as e:
                                self.logger.error(f"Error in notification callback: {e}")
                        
                        # Update latest ID if newer
                        if notification['id'] > self.latest_notification_id:
                            self.latest_notification_id = notification['id']
                
            except Exception as e:
                self.logger.error(f"Error during notification polling: {e}")
            
            # Wait for the next interval using asyncio
            await asyncio.sleep(interval)
    
    async def stop_notification_polling(self):
        """Stop the notification polling if it's active"""
        if not self.polling_active:
            self.logger.warning("Notification polling is not active")
            return False
        
        self.polling_active = False
        if self.polling_task and not self.polling_task.done():
            # Cancel the task and wait for it to complete
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                pass
            self.logger.info("Notification polling stopped")
        
        return True
    
    def _get_new_notifications(self, notifications):
        """Filter notifications to get only new ones since the last check"""
        if not self.latest_notification_id or not notifications:
            return notifications
        
        # Find notifications newer than the latest one we've seen
        new_notifications = []
        for notification in notifications:
            if notification['id'] > self.latest_notification_id:
                new_notifications.append(notification)
        
        return new_notifications
    
    def notification_done(self, notification_id):
        """Mark a notification as processed/done"""
        try:
            # Dismiss the notification on the server
            self.mastodon.notifications_dismiss(notification_id)
            self.logger.debug(f"Marked notification {notification_id} as done")
            return True
        except Exception as e:
            self.logger.error(f"Error marking notification {notification_id} as done: {e}")
            return False
