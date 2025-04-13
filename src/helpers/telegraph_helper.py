import asyncio
from telegraph import Telegraph
from src.logger import get_logger

logger = get_logger(__name__)

class TelegraphHelper:
    def __init__(self, author_name="Zirak AI"):
        self.telegraph = Telegraph()
        self.telegraph.create_account(short_name=author_name)
        self.author_name = author_name
        logger.info("Telegraph account created")

    async def create_page(self, title, content):
        """
        Create a Telegraph page with the given title and content.
        
        Args:
            title (str): The title of the page
            content (str): HTML content for the page
            
        Returns:
            str: URL of the created page, or None if creation failed
        """
        try:
            # Telegraph API calls are synchronous, run in executor to avoid blocking
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.telegraph.create_page(
                    title=title,
                    html_content=content,
                    author_name=self.author_name
                )
            )
            
            url = f"https://telegra.ph/{response['path']}"
            logger.info(f"Created Telegraph page: {url}")
            return url
        except Exception as e:
            logger.error(f"Failed to create Telegraph page: {str(e)}")
            return None
            
    def format_content(self, research_data):
        """
        Format research data into HTML content suitable for Telegraph.
        
        Args:
            research_data (dict): Research data with sections, findings, etc.
            
        Returns:
            str: HTML formatted content
        """
        html = ""
        
        # Add introduction if available
        if "introduction" in research_data:
            html += f"<p>{research_data['introduction']}</p>"
            
        # Add main content sections
        if "sections" in research_data:
            for section in research_data["sections"]:
                html += f"<h3>{section['title']}</h3>"
                html += f"<p>{section['content']}</p>"
                
        # Add sources if available
        if "sources" in research_data:
            html += "<h3>Sources</h3><ul>"
            for source in research_data["sources"]:
                html += f"<li><a href='{source['url']}'>{source['title']}</a></li>"
            html += "</ul>"
            
        # Add conclusion if available
        if "conclusion" in research_data:
            html += f"<p><strong>Conclusion:</strong> {research_data['conclusion']}</p>"
            
        return html 

async def create_telegraph_page(research_data):
    """
    Create a Telegraph page from research data
    
    Args:
        research_data (dict): Research data including title, sections, etc.
        
    Returns:
        dict: Dictionary containing the URL and title of the created page
    """
    try:
        telegraph = Telegraph()
        # You can use a random short name or your bot's name
        telegraph.create_account(short_name='ResearchBot')
        
        # Construct HTML content from research data
        content = f"<p>{research_data['introduction']}</p>"
        
        # Add sections
        for section in research_data['sections']:
            content += f"<h3>{section['title']}</h3><p>{section['content']}</p>"
        
        # Add sources if available
        if 'sources' in research_data and research_data['sources']:
            content += "<h3>Sources</h3><ul>"
            for source in research_data['sources']:
                if 'url' in source:
                    content += f"<li><a href='{source['url']}'>{source['title']}</a></li>"
                else:
                    content += f"<li>{source['title']}</li>"
            content += "</ul>"
        
        # Add conclusion
        if 'conclusion' in research_data:
            content += f"<h3>Conclusion</h3><p>{research_data['conclusion']}</p>"
        
        # Create page
        response = telegraph.create_page(
            title=research_data['title'],
            html_content=content
        )
        
        return {
            'url': 'https://telegra.ph/{}'.format(response['path']),
            'title': research_data['title']
        }
        
    except Exception as e:
        logger.error(f"Error creating Telegraph page: {str(e)}")
        return {
            'url': None,
            'title': research_data.get('title', 'Research Results')
        } 