from src.logger import get_logger
from src.llms.VertexAI import VertexAI
from src.helpers.prompts import get_prompt
import os
import html2text
from src.helpers.telegraph_helper import TelegraphHelper

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
    "google-auth.json",
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
        post_account = post.get("account", {})
        post_username = post_account.get("acct", "unknown")
        post_content = clean_html_content(post.get("content", ""))

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
            username=username, thread_content=thread_content
        )

        # Get response from VertexAI (non-streaming for simplicity)
        response = vertex_ai.chat(
            default_model, user_prompt, system_prompt=system_prompt, stream=False
        )

        # Trim the response if it's too long for Mastodon
        if len(response) > 500:
            logger.warning(
                f"AI response too long ({len(response)} chars), trimming to 500 chars"
            )
            response = response[:497] + "..."

        return response

    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "I'm sorry, I'm having trouble processing your request right now."


class NotificationHandler:
    def __init__(self, mastodon_client, llm_client):
        self.mastodon_client = mastodon_client
        self.llm_client = llm_client
        self.telegraph_helper = TelegraphHelper()

    async def process_mention(self, notification):
        logger.debug(f"Processing mention notification from @{notification['account']['acct']}")
        status = notification.get("status", {})
        status_id = status.get("id")
        logger.info(f"CALLBACK: New mention from @{notification['account']['acct']}: {status.get('content', '')[:50]}...")

        # Trace the thread from the mention to the top post
        if self.mastodon_client and status_id:
            logger.debug(f"Retrieving thread for status_id: {status_id}")
            # Get the full thread
            thread = self.mastodon_client.get_thread(status_id)

            if thread:
                logger.info(f"Found a thread with {len(thread)} posts")
                logger.debug(
                    f"Thread details: {len(thread)} posts with status_id {status_id}"
                )

                # Print all posts in the thread from top to bottom
                logger.info("======= THREAD BEGIN =======")
                for i, post in enumerate(thread):
                    post_account = post.get("account", {})
                    post_username = post_account.get("acct", "unknown")
                    post_content = clean_html_content(post.get("content", ""))

                    logger.info(
                        f"[{i+1}/{len(thread)}] @{post_username}: {post_content[:200]}"
                    )
                    if len(post_content) > 200:
                        logger.info("... (content truncated)")
                logger.info("======= THREAD END =======")

                # Get reply from VertexAI
                logger.debug(
                    f"Generating AI response for thread with {len(thread)} posts"
                )
                reply_content = get_ai_response(thread, notification['account']['acct'])
                logger.info(f"AI generated reply: {reply_content}")
            else:
                # Fallback if we couldn't get the thread
                logger.debug("Failed to retrieve thread, using fallback response")
                reply_content = "Hi! I noticed your mention, but I couldn't retrieve the full conversation context."

            # Check if this requires extensive research
            needs_extensive_research = self.llm_client.is_extensive_research(reply_content)
            
            if needs_extensive_research:
                # Generate detailed research response
                detailed_response = await self.llm_client.generate_research_response(
                    reply_content, 
                    thread
                )
                
                # Format for Telegraph
                research_data = detailed_response.get("research_data", {})
                title = f"Research: {research_data.get('title', 'Requested Information')}"
                html_content = self.telegraph_helper.format_content(research_data)
                
                # Create Telegraph page
                telegraph_url = await self.telegraph_helper.create_page(title, html_content)
                
                if telegraph_url:
                    # Create a brief response with the link for Mastodon
                    brief_response = f"I've completed the research you requested. The full details are available here: {telegraph_url}"
                    
                    if "summary" in research_data:
                        brief_response = f"{research_data['summary']}\n\nFull details: {telegraph_url}"
                else:
                    # Fallback if Telegraph creation fails
                    brief_response = "I've completed your research request, but couldn't create an external page. Here's a summary:\n\n"
                    brief_response += detailed_response.get("summary", "Unable to provide summary.")
                    
                # Post the response to Mastodon
                await self.mastodon_client.post_status(
                    brief_response,
                    in_reply_to_id=status['id'],
                    visibility=status['visibility']
                )
            else:
                # Reply using the generated content
                logger.debug(f"Sending reply to @{notification['account']['acct']} for status_id: {status_id}")
                await self.mastodon_client.reply_to_mention(status, reply_content)
                logger.info(f"CALLBACK: Replied to @{notification['account']['acct']}")
        else:
            logger.error(
                "Missing client or status_id, couldn't process mention properly"
            )

        # Mark the notification as done after handling it
        logger.debug(f"Marking mention notification from @{notification['account']['acct']} as done")
        await self.mastodon_client.mark_notification_as_done(notification)

    async def process_follow(self, notification):
        logger.debug(f"Processing follow notification from @{notification['account']['acct']}")
        logger.info(f"CALLBACK: New follower: @{notification['account']['acct']}!")
        # Maybe send them a welcome message

        # Mark as done after processing
        logger.debug(f"Marking follow notification from @{notification['account']['acct']} as done")
        await self.mastodon_client.mark_notification_as_done(notification)

    async def process_favourite(self, notification):
        logger.debug(f"Processing favourite notification from @{notification['account']['acct']}")
        logger.info(f"CALLBACK: @{notification['account']['acct']} favorited your post!!")
        # Auto-dismiss favorites
        logger.debug(f"Marking favourite notification from @{notification['account']['acct']} as done")
        await self.mastodon_client.mark_notification_as_done(notification)

    async def process_reblog(self, notification):
        logger.debug(f"Processing reblog notification from @{notification['account']['acct']}")
        logger.info(f"CALLBACK: @{notification['account']['acct']} boosted your post")
        # Auto-dismiss boosts
        logger.debug(f"Marking reblog notification from @{notification['account']['acct']} as done")
        await self.mastodon_client.mark_notification_as_done(notification)

    async def process_unknown(self, notification):
        # For other notification types, mark as done
        logger.debug(
            f"Processing unknown notification type: {notification['type']} from @{notification['account']['acct']}"
        )
        logger.info(
            f"CALLBACK: Received {notification['type']} notification, marking as done"
        )
        logger.debug(f"Marking {notification['type']} notification from @{notification['account']['acct']} as done")
        await self.mastodon_client.mark_notification_as_done(notification)

    async def process_notification(self, notification):
        try:
            await self.process_mention(notification)
        except Exception as e:
            logger.error(f"Error in notification handler: {e}")
            logger.debug(f"Exception details: {str(e)}")
