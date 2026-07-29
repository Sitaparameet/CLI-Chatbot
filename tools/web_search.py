import os
from langchain_core.tools import tool
from tavily import TavilyClient
from tools.tool_logger import log_tool


@tool
@log_tool
def web_search(query: str) -> str:
    """Search the web using Tavily.

    Use this tool when the user needs:
    - Current or latest information
    - Recent news or events
    - Current weather-related events
    - Detailed research
    - Information about technology or current trends
    - External facts or sources
    - A researched report or document
    """
    query = query.strip()
    if not query:
        return "Error: Search query cannot be empty."

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY is not configured."

    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=3,
        )
        results = response.get("results", [])

        if not results:
            return "No recent search results found."

        formatted_results = [
            f"Title: {item.get('title', 'No title')}\n"
            f"Content: {item.get('content', 'No content')}\n"
            f"URL: {item.get('url', 'No URL')}"
            for item in results
        ]
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Web search failed: {e}"