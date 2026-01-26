# Week 3 — Custom MCP Server: News API Integration

This project implements a local STDIO-based Model Context Protocol (MCP) server in Python that wraps the NewsAPI service. The server exposes two MCP tools for searching news articles and retrieving top headlines, enabling AI assistants like Claude Desktop to access real-time news data.

## Overview

The News MCP Server provides programmatic access to news articles through the NewsAPI service. It implements a standard MCP server using STDIO transport, making it compatible with MCP clients such as Claude Desktop. The server handles API authentication, error handling, and rate limiting while exposing clean, typed tool interfaces.

**Key Features:**
- Search news articles by keyword with language and pagination support
- Retrieve top headlines by country
- Robust error handling for network failures and API errors
- Logging to stderr (following MCP STDIO best practices)
- Type-safe tool parameters with defaults

## Prerequisites

Before setting up the MCP server, ensure you have the following installed:

1. **Python 3.10 or higher** (3.12 recommended)
   - Verify installation: `python --version`

2. **Conda** (Anaconda or Miniconda)
   - Download from: [Anaconda Individual Edition](https://www.anaconda.com/download)
   - Verify installation: `conda --version`

3. **Poetry** (Python package manager)
   - Install via: `curl -sSL https://install.python-poetry.org | python -`
   - On Windows (PowerShell): `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -`
   - Verify installation: `poetry --version`

4. **NewsAPI Account and API Key**
   - Sign up at: [newsapi.org](https://newsapi.org/)
   - Obtain your free API key from the dashboard
   - Note: Free tier has rate limits (100 requests/day for development)

5. **Claude Desktop** (for testing the MCP server)
   - Download from: [claude.ai/download](https://claude.ai/download)
   - Required for local STDIO MCP server integration

## Environment Setup

### Step 1: Activate Conda Environment

Create and activate the Conda environment if not already done:

```bash
conda create -n cs146s python=3.12 -y
conda activate cs146s
```

### Step 2: Install Project Dependencies

From the repository root directory:

```bash
poetry install --no-interaction
```

This installs base dependencies including `httpx` and `python-dotenv`.

### Step 3: Install MCP SDK

Install the MCP Python SDK package:

```bash
pip install mcp
```

Or using Poetry (if adding to project dependencies):

```bash
poetry add mcp
```

### Step 4: Configure Environment Variables

Navigate to the `week3/` directory and create a `.env` file:

```bash
cd week3
```

Create `.env` with your NewsAPI key:

```env
NEWSAPI_KEY=your_api_key_here
```

**Important:** 
- Replace `your_api_key_here` with your actual NewsAPI key
- The `.env` file is gitignored and should not be committed
- Never share your API key publicly

### Step 5: Verify Installation

Test that the server can be imported:

```bash
python -c "from mcp.server import Server; print('MCP SDK installed successfully')"
```

## Running the MCP Server Locally (STDIO)

The MCP server runs as a STDIO-based server, communicating with clients via standard input/output streams. This is the standard mode for local MCP servers integrated with Claude Desktop.

### Start the Server

From the `week3/` directory, with the Conda environment activated:

```bash
python server/main.py
```

**Expected Behavior:**
- The server starts and logs initialization messages to stderr
- It waits for MCP protocol messages on stdin
- No output appears on stdout (following MCP STDIO best practices)
- Logs appear on stderr with timestamps and log levels

**Example stderr output:**
```
2025-01-26 10:30:00 [INFO] Starting News MCP Server (STDIO mode)
2025-01-26 10:30:00 [INFO] Registered MCP tools
```

### Testing the Server

The server is designed to be run by an MCP client (like Claude Desktop), not directly. However, you can verify it starts without errors:

1. Start the server: `python server/main.py`
2. The server should start and wait for input (no errors)
3. Press `Ctrl+C` to stop the server

For interactive testing, use the MCP Inspector tool or configure Claude Desktop (see next section).

## Configuring the MCP Client (Claude Desktop)

This section provides detailed instructions for configuring Claude Desktop on Windows to use the local STDIO MCP server.

### Step 1: Locate Claude Desktop Configuration File

On Windows, the Claude Desktop configuration file is located at:

```
C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
```

**Note:** If the file doesn't exist, create it. The `Claude` directory may need to be created first.

### Step 2: Edit the Configuration File

Open `claude_desktop_config.json` in a text editor and add the MCP server configuration:

```json
{
  "mcpServers": {
    "news-mcp-server": {
      "command": "python",
      "args": [
        "C:\\cs146s\\modern-software-dev-assignments\\week3\\server\\main.py"
      ],
      "env": {
        "NEWSAPI_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Important Configuration Details:**

1. **`command`**: Use `"python"` (ensure Python is in your PATH) or use the full path to your Python executable:
   ```json
   "command": "C:\\Users\\<YourUsername>\\anaconda3\\envs\\cs146s\\python.exe"
   ```

2. **`args`**: Provide the full absolute path to `main.py`. Use forward slashes or escaped backslashes:
   ```json
   "args": [
     "C:/cs146s/modern-software-dev-assignments/week3/server/main.py"
   ]
   ```

3. **`env`**: Set environment variables. You can either:
   - Set `NEWSAPI_KEY` here (as shown above), or
   - Rely on the `.env` file in `week3/` directory (if using `python-dotenv`)

**Alternative Configuration (Using .env file):**

If you prefer to use the `.env` file instead of setting the environment variable in the config:

```json
{
  "mcpServers": {
    "news-mcp-server": {
      "command": "python",
      "args": [
        "C:\\cs146s\\modern-software-dev-assignments\\week3\\server\\main.py"
      ]
    }
  }
}
```

Ensure the `.env` file exists in `week3/` with `NEWSAPI_KEY=your_key`.

### Step 3: Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen Claude Desktop
3. The MCP server should be automatically started when Claude Desktop launches

### Step 4: Verify Connection

1. Open Claude Desktop
2. Start a new conversation
3. The MCP tools should be available. You can ask Claude:
   - "Search for news about AI"
   - "Get top headlines for the US"
   - "What MCP tools are available?"

If the server fails to start, check:
- Python path is correct in the configuration
- The `main.py` path is correct and accessible
- The `NEWSAPI_KEY` is set (either in config or `.env`)
- Claude Desktop's error logs (check the application console or logs directory)

### Troubleshooting Claude Desktop Configuration

**Issue: Server not starting**
- Verify the Python executable path is correct
- Check that all paths use forward slashes or properly escaped backslashes
- Ensure the Conda environment is activated or use the full path to the Python executable

**Issue: "Module not found" errors**
- Ensure `mcp` package is installed: `pip install mcp`
- Verify you're using the correct Python environment (the one with MCP installed)

**Issue: API key errors**
- Verify `NEWSAPI_KEY` is set in the config's `env` section or in `.env`
- Check that the API key is valid and not expired

## Tool Reference

The server exposes two MCP tools for interacting with the NewsAPI service.

### search_news

Search for news articles by keyword with optional language and pagination controls.

**Tool Name:** `search_news`

**Description:** Search for news articles by keyword.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | `string` | Yes | - | Search keyword (e.g., 'AI', 'climate change', 'technology') |
| `language` | `string` | No | `"en"` | Language code (ISO 639-1 format, e.g., 'en', 'es', 'fr') |
| `page_size` | `integer` | No | `5` | Number of articles to return (1-100, default: 5) |

**Example Input:**

```json
{
  "query": "artificial intelligence",
  "language": "en",
  "page_size": 3
}
```

**Example Output:**

```json
[
  {
    "title": "AI Breakthrough in Medical Diagnosis",
    "source": "Tech News",
    "url": "https://example.com/article1",
    "published_at": "2025-01-26T10:00:00Z"
  },
  {
    "title": "New AI Model Surpasses Human Performance",
    "source": "Science Daily",
    "url": "https://example.com/article2",
    "published_at": "2025-01-26T09:30:00Z"
  },
  {
    "title": "Ethical Concerns in AI Development",
    "source": "The Guardian",
    "url": "https://example.com/article3",
    "published_at": "2025-01-26T08:15:00Z"
  }
]
```

**Expected Behaviors:**

- **Success Case:** Returns a list of article objects, each containing `title`, `source`, `url`, and `published_at` fields. The list is ordered by relevance (as determined by NewsAPI).
- **Empty Results:** Returns an empty list `[]` if no articles match the query.
- **Error Cases:**
  - Missing `query` parameter: MCP protocol validation error (tool not called)
  - Invalid `language` code: NewsAPI may return an error; server returns `[{"error": "News API error: 400"}]`
  - Network timeout: Returns `[{"error": "News API request timed out"}]`
  - API key missing/invalid: Returns `[{"error": "NEWSAPI_KEY is not set"}]` or `[{"error": "News API error: 401"}]`
  - Rate limit exceeded: Returns `[{"error": "News API error: 429"}]`

**Notes:**
- The `query` parameter supports multi-word searches (e.g., "climate change", "machine learning")
- Language codes follow ISO 639-1 standard (two-letter codes)
- `page_size` is capped by NewsAPI's maximum (typically 100 articles per request)
- Results are limited by NewsAPI's free tier restrictions

### get_top_headlines

Retrieve top news headlines for a specified country.

**Tool Name:** `get_top_headlines`

**Description:** Get top news headlines for a given country.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `country` | `string` | No | `"us"` | Country code (ISO 3166-1 alpha-2 format, e.g., 'us', 'kr', 'gb', 'jp') |
| `page_size` | `integer` | No | `5` | Number of headlines to return (1-100, default: 5) |

**Example Input:**

```json
{
  "country": "us",
  "page_size": 5
}
```

**Example Output:**

```json
[
  {
    "title": "Breaking: Major Policy Announcement",
    "source": "CNN",
    "url": "https://example.com/headline1",
    "published_at": "2025-01-26T11:00:00Z"
  },
  {
    "title": "Economic Report Shows Growth",
    "source": "Reuters",
    "url": "https://example.com/headline2",
    "published_at": "2025-01-26T10:45:00Z"
  },
  {
    "title": "Sports Championship Results",
    "source": "ESPN",
    "url": "https://example.com/headline3",
    "published_at": "2025-01-26T10:30:00Z"
  },
  {
    "title": "Technology Innovation Announcement",
    "source": "TechCrunch",
    "url": "https://example.com/headline4",
    "published_at": "2025-01-26T10:15:00Z"
  },
  {
    "title": "Health Advisory Update",
    "source": "BBC News",
    "url": "https://example.com/headline5",
    "published_at": "2025-01-26T10:00:00Z"
  }
]
```

**Expected Behaviors:**

- **Success Case:** Returns a list of headline objects with the same structure as `search_news` (title, source, url, published_at). Headlines are ordered by NewsAPI's ranking algorithm.
- **Empty Results:** Returns an empty list `[]` if no headlines are available for the specified country.
- **Error Cases:**
  - Invalid `country` code: NewsAPI may return an error; server returns `[{"error": "News API error: 400"}]`
  - Network timeout: Returns `[{"error": "News API request timed out"}]`
  - API key missing/invalid: Returns `[{"error": "NEWSAPI_KEY is not set"}]` or `[{"error": "News API error: 401"}]`
  - Rate limit exceeded: Returns `[{"error": "News API error: 429"}]`

**Notes:**
- Country codes follow ISO 3166-1 alpha-2 standard (two-letter codes)
- Common country codes: `us` (United States), `gb` (United Kingdom), `kr` (South Korea), `jp` (Japan), `de` (Germany), `fr` (France)
- Headlines are typically the most recent and popular stories for the country
- `page_size` is capped by NewsAPI's maximum (typically 100 headlines per request)

## Example Usage

### Using Claude Desktop

Once the MCP server is configured in Claude Desktop, you can interact with it through natural language:

**Example 1: Search for News**
```
User: "Search for news about climate change"
Claude: [Calls search_news with query="climate change"]
       Returns articles about climate change
```

**Example 2: Get Top Headlines**
```
User: "What are the top headlines in South Korea?"
Claude: [Calls get_top_headlines with country="kr"]
       Returns top headlines for South Korea
```

**Example 3: Search with Parameters**
```
User: "Find 10 recent articles about AI in Spanish"
Claude: [Calls search_news with query="AI", language="es", page_size=10]
       Returns 10 Spanish-language articles about AI
```

### Direct Tool Invocation (for testing)

If testing the server programmatically, tool calls follow the MCP protocol format:

**Search News:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "search_news",
    "arguments": {
      "query": "artificial intelligence",
      "language": "en",
      "page_size": 5
    }
  }
}
```

**Get Top Headlines:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_top_headlines",
    "arguments": {
      "country": "us",
      "page_size": 5
    }
  }
}
```

## Error Handling and Rate Limiting Notes

### Error Handling

The server implements comprehensive error handling for common failure scenarios:

1. **Missing API Key:**
   - **Detection:** Checks for `NEWSAPI_KEY` environment variable
   - **Response:** Returns `[{"error": "NEWSAPI_KEY is not set"}]`
   - **User Action:** Set the API key in `.env` or Claude Desktop config

2. **Network Timeouts:**
   - **Detection:** Catches `httpx.TimeoutException` (10-second timeout)
   - **Response:** Returns `[{"error": "News API request timed out"}]`
   - **User Action:** Check internet connection or retry the request

3. **HTTP Errors:**
   - **Detection:** Catches `httpx.HTTPStatusError` for non-2xx responses
   - **Response:** Returns `[{"error": "News API error: <status_code>"}]`
   - **Common Status Codes:**
     - `400`: Bad request (invalid parameters)
     - `401`: Unauthorized (invalid API key)
     - `429`: Too many requests (rate limit exceeded)
     - `500`: Internal server error (NewsAPI issue)

4. **Empty Results:**
   - **Detection:** NewsAPI returns no articles
   - **Response:** Returns empty list `[]`
   - **User Action:** Try different search terms or check if news is available

5. **Invalid Parameters:**
   - **Detection:** MCP protocol validates required parameters before tool invocation
   - **Response:** MCP protocol error (tool not called)
   - **User Action:** Ensure required parameters are provided

### Rate Limiting

**NewsAPI Free Tier Limits:**
- **Development Key:** 100 requests per day
- **Business Key:** Higher limits (varies by plan)

**Rate Limit Handling:**
- The server does not implement automatic retry or backoff
- When rate limit is exceeded (HTTP 429), the server returns an error message
- **User Action:** Wait until the rate limit resets (typically 24 hours) or upgrade to a paid plan

**Best Practices:**
- Cache results when possible to reduce API calls
- Use appropriate `page_size` values (don't request 100 articles if you only need 5)
- Monitor your API usage in the NewsAPI dashboard
- Consider implementing request queuing or exponential backoff for production use

### Logging

The server logs all operations to stderr (following MCP STDIO best practices):

- **INFO level:** Server startup, tool registration
- **Error details:** Captured in tool error responses (not logged separately to avoid duplicate information)

Logs follow the format:
```
%(asctime)s [%(levelname)s] %(message)s
```

Example:
```
2025-01-26 10:30:00 [INFO] Starting News MCP Server (STDIO mode)
2025-01-26 10:30:00 [INFO] Registered MCP tools
```

## Project Structure

```
week3/
├── server/
│   ├── main.py           # MCP STDIO server entrypoint
│   ├── tools.py          # MCP tool definitions and handlers
│   └── news_client.py    # NewsAPI client logic and error handling
├── .env                  # Environment variables (NEWSAPI_KEY) - not committed
├── .gitignore           # Excludes .env and other sensitive files
└── README.md            # This file
```

## Additional Notes

- **API Key Security:** Never commit your `.env` file or API keys to version control. The `.gitignore` file excludes `.env` by default.
- **Development vs Production:** This server is designed for local development. For production deployment, consider implementing additional security measures, request validation, and monitoring.
- **MCP Protocol:** The server follows the MCP specification for STDIO transport. All communication uses JSON-RPC-like messages over stdin/stdout.
- **Testing:** Use Claude Desktop or the MCP Inspector tool for interactive testing. Unit tests can be added to test the `news_client.py` functions independently.

## References

- [MCP Server Quickstart](https://modelcontextprotocol.io/quickstart/server)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [Claude Desktop Documentation](https://claude.ai/docs/mcp)
