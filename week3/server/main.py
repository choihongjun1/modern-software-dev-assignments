import sys
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server

from server.tools import register_tools


def main():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    logging.info("Starting News MCP Server (STDIO mode)")

    server = Server(
        name="news-mcp-server",
        version="0.1.0",
        description="MCP server that provides news search tools using NewsAPI",
    )

    register_tools(server)

    logging.info("Registered MCP tools")

    stdio_server(server)


if __name__ == "__main__":
    main()
