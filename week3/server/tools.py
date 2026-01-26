from typing import List, Optional, Dict, Any

from mcp.server import Server
from mcp.server.tools import Tool

from server.news_client import search_news, get_top_headlines, NewsAPIError


def register_tools(server: Server):
    """
    Register all MCP tools for this server.
    """

    # 🔹 Tool 1: search_news
    server.add_tool(
        Tool(
            name="search_news",
            description="Search for news articles by keyword.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword (e.g. 'AI', 'climate change')",
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code (default: 'en')",
                        "default": "en",
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of articles to return (default: 5)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
            handler=_handle_search_news,
        )
    )

    # 🔹 Tool 2: get_top_headlines
    server.add_tool(
        Tool(
            name="get_top_headlines",
            description="Get top news headlines for a given country.",
            parameters={
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Country code (e.g. 'us', 'kr')",
                        "default": "us",
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of headlines to return (default: 5)",
                        "default": 5,
                    },
                },
            },
            handler=_handle_get_top_headlines,
        )
    )


def _handle_search_news(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
        return search_news(
            query=args["query"],
            language=args.get("language", "en"),
            page_size=args.get("page_size", 5),
        )
    except NewsAPIError as e:
        return [{"error": str(e)}]


def _handle_get_top_headlines(args: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
        return get_top_headlines(
            country=args.get("country", "us"),
            page_size=args.get("page_size", 5),
        )
    except NewsAPIError as e:
        return [{"error": str(e)}]
