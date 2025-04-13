import asyncio
from unittest.mock import patch, MagicMock
from src.helpers.telegraph_helper import create_telegraph_page
from src.llms.VertexAI import VertexAI  # Adjust import based on your actual structure

async def main():
    # Test prompt
    prompt = "tell me about fifa world cup history"
    
    # Mock research data that would be returned by the LLM
    mock_research_data = {
        "title": "FIFA World Cup History",
        "introduction": "The FIFA World Cup is the most prestigious soccer tournament in the world...",
        "sections": [
            {"title": "Origins (1930-1938)", "content": "The first FIFA World Cup was held in 1930 in Uruguay..."},
            {"title": "Post-War Era (1950-1978)", "content": "After a 12-year hiatus due to World War II..."},
            {"title": "Modern Era (1982-Present)", "content": "The tournament expanded to 24 teams in 1982..."}
        ],
        "sources": [
            {"title": "FIFA Official History", "url": "https://www.fifa.com/worldcup/history"},
            {"title": "World Cup Archive", "url": "https://www.worldcuparchive.com"}
        ],
        "conclusion": "The FIFA World Cup continues to be the most watched sporting event globally...",
        "summary": "The FIFA World Cup began in 1930 and has evolved into the world's biggest sporting event."
    }
    
    # Test the full flow
    print("Testing Telegraph feature with prompt:", prompt)
    
    # Method 1: Using mocks to test without actual API calls
    with patch('src.llms.VertexAI.VertexAI.generate_research_response') as mock_generate:
        with patch('src.helpers.telegraph_helper.create_telegraph_page') as mock_telegraph:
            # Configure mocks
            mock_generate.return_value = {"research_data": mock_research_data, "summary": mock_research_data["summary"]}
            mock_telegraph.return_value = {"url": "https://telegra.ph/FIFA-World-Cup-History-01-01", "title": mock_research_data["title"]}
            
            # Create LLM instance
            llm = VertexAI()
            
            # Generate research response
            research_response = await llm.generate_research_response(prompt)
            
            # Create Telegraph page
            telegraph_result = await create_telegraph_page(research_response["research_data"])
            
            # Print results
            print("\nMock Test Results:")
            print(f"Telegraph URL: {telegraph_result['url']}")
            print(f"Title: {telegraph_result['title']}")
            print(f"Summary: {research_response['summary']}")
    
    # Method 2: Optional - Uncomment to test with actual API calls (requires API keys)
    """
    print("\nRunning actual API test...")
    
    # Create LLM instance
    llm = VertexAI()
    
    # Generate research response
    research_response = await llm.generate_research_response(prompt)
    
    # Create Telegraph page
    telegraph_result = await create_telegraph_page(research_response["research_data"])
    
    # Print results
    print("\nActual API Test Results:")
    print(f"Telegraph URL: {telegraph_result['url']}")
    print(f"Title: {telegraph_result['title']}")
    print(f"Summary: {research_response['summary']}")
    """

if __name__ == "__main__":
    asyncio.run(main()) 