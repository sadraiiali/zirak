from src.logger import get_logger
from src.llms.VertexAI import VertexAI
from src.helpers.prompts import get_prompt
import os
import html2text

# Set up logger
logger = get_logger("notifications")

# HTML to text converter for cleaning Mastodon content
html_converter = html2text.HTML2Text()
html_converter.ignore_links = False
html_converter.ignore_images = True

# Initialize VertexAI (create it once for the module)
credentials_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "data",
    "google-auth.json"
)
vertex_ai = VertexAI(credentials_path=credentials_path)

if not vertex_ai.initialize():
    logger.error("Failed to initialize VertexAI")
else:
    models = vertex_ai.list_available_models()
    if models:
        default_model = models[0]
        logger.info(f"VertexAI initialized with model: {default_model}")
    else:
        default_model = "gemini-1.5-flash-001"
        logger.info(f"No models found, using default: {default_model}")

def clean_html_content(html_content):
    """Remove HTML tags from content and convert to plain text"""
    if not html_content:
        return ""
    return html_converter.handle(html_content).strip()

def format_thread_for_llm(thread):
    """Format a Mastodon thread for input to the LLM"""
    formatted_thread = "The following is a conversation thread from Mastodon:\n\n"
    
    for i, post in enumerate(thread):
        post_account = post.get('account', {})
        post_username = post_account.get('acct', 'unknown')
        post_content = clean_html_content(post.get('content', ''))
        
        formatted_thread += f"@{post_username}: {post_content}\n\n"
    
    return formatted_thread

def get_ai_response(thread, username):
    """Get a response from VertexAI for the given thread"""
    try:
        # Format the thread content into a prompt
        thread_content = format_thread_for_llm(thread)
        
        # Load prompts from files
        system_prompt = get_prompt("mastodon_system_prompt")
        user_prompt_template = get_prompt("mastodon_user_prompt")
        
        # Format the user prompt with the thread content and username
        user_prompt = user_prompt_template.format(
            username=username,
            thread_content=thread_content
        )
        
        # Get response from VertexAI (non-streaming for simplicity)
        response = vertex_ai.chat(
            default_model, 
            user_prompt, 
            system_prompt=system_prompt,
            stream=False
        )
        
        # Trim the response if it's too long for Mastodon
        if len(response) > 500:
            logger.warning(f"AI response too long ({len(response)} chars), trimming to 500 chars")
            response = response[:497] + "..."
            
        return response
        
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "I'm sorry, I'm having trouble processing your request right now."

# Define a notification callback function
async def notification_handler(event_type, notification_data, done_callback, client=None):
    """
    Example callback function for processing notifications
    
    Args:
        event_type: Type of notification (mention, follow, favourite, reblog, etc.)
        notification_data: Full notification data from Mastodon
        done_callback: Function to call to mark notification as processed
        client: Instance of MastodonClient to use for API calls
    """
    account = notification_data.get('account', {})
    username = account.get('acct', 'unknown')
    
    try:
        if event_type == 'mention':
            status = notification_data.get('status', {})
            content = status.get('content', '')
            status_id = status.get('id')
            logger.info(f"CALLBACK: New mention from @{username}: {content[:50]}...")
            
            # Trace the thread from the mention to the top post
            if client and status_id:
                # Get the full thread
                thread = client.get_thread(status_id)
                
                if thread:
                    logger.info(f"Found a thread with {len(thread)} posts")
                    
                    # Print all posts in the thread from top to bottom
                    logger.info("======= THREAD BEGIN =======")
                    for i, post in enumerate(thread):
                        post_account = post.get('account', {})
                        post_username = post_account.get('acct', 'unknown')
                        post_content = clean_html_content(post.get('content', ''))
                        
                        logger.info(f"[{i+1}/{len(thread)}] @{post_username}: {post_content[:200]}")
                        if len(post_content) > 200:
                            logger.info("... (content truncated)")
                    logger.info("======= THREAD END =======")
                
                    # Get reply from VertexAI
                    reply_content = get_ai_response(thread, username)
                    logger.info(f"AI generated reply: {reply_content}")
                else:
                    # Fallback if we couldn't get the thread
                    reply_content = "Hi! I noticed your mention, but I couldn't retrieve the full conversation context."
                
                # Reply using the generated content
                client.reply_to_mention(status, reply_content)
                logger.info(f"CALLBACK: Replied to @{username}")
            else:
                logger.error("Missing client or status_id, couldn't process mention properly")

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
