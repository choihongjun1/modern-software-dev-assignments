# Action Item Extractor

A FastAPI-based web application that extracts actionable items from free-form text notes. The application supports both rule-based extraction (using regex patterns and heuristics) and LLM-based extraction (using Ollama with local models). Extracted action items can be saved to a SQLite database, associated with notes, and marked as complete.

## Overview

This application provides a simple interface for converting unstructured meeting notes, task lists, or other text into organized action items. It features:

- **Rule-based extraction**: Fast, deterministic extraction using pattern matching (bullet points, keywords like "TODO:", checkboxes)
- **LLM-based extraction**: Context-aware extraction using local language models via Ollama
- **Note management**: Save and retrieve notes with associated action items
- **Action item tracking**: Mark items as done/undone and filter by note

The frontend is a minimal HTML/JavaScript interface served directly by FastAPI, requiring no build tools or separate frontend server.

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # SQLite database operations
│   ├── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── action_items.py  # Action item endpoints
│   │   └── notes.py         # Note endpoints
│   └── services/
│       └── extract.py       # Extraction logic (rule-based and LLM)
├── frontend/
│   └── index.html          # Web UI
├── tests/
│   └── test_extract.py     # Unit tests for extraction functions
└── data/                   # SQLite database (created at runtime)
```

## Setup and Installation

### Prerequisites

- Python 3.10 or higher (3.12 recommended)
- Anaconda or Miniconda
- Poetry (Python package manager)

### Step 1: Create Conda Environment

Create and activate a new Conda environment:

```bash
conda create -n cs146s python=3.12 -y
conda activate cs146s
```

### Step 2: Install Poetry

If Poetry is not already installed:

```bash
curl -sSL https://install.python-poetry.org | python -
```

On Windows (PowerShell):

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Step 3: Install Dependencies

From the repository root directory:

```bash
poetry install --no-interaction
```

This installs all project dependencies including:
- FastAPI and Uvicorn (web framework and ASGI server)
- Pydantic (data validation)
- Ollama (for LLM-based extraction)
- pytest (testing framework)

### Step 4: Install and Configure Ollama (for LLM extraction)

The LLM-based extraction feature requires Ollama with a local model. Install Ollama:

- **macOS**: `brew install --cask ollama`
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`
- **Windows**: Download from [ollama.com/download](https://ollama.com/download)

Pull the required model (phi3:mini is used by default):

```bash
ollama pull phi3:mini
```

Start the Ollama service:

```bash
ollama serve
```

Keep this terminal running while using the LLM extraction feature.

## Running the Application

### Start the FastAPI Server

From the repository root, with the Conda environment activated:

```bash
poetry run uvicorn week2.app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

### Access the Application

- **Web UI**: Open http://127.0.0.1:8000/ in your browser
- **API Documentation**: Open http://127.0.0.1:8000/docs for interactive Swagger UI
- **Alternative API Docs**: http://127.0.0.1:8000/redoc

### Database

The SQLite database is automatically created at `week2/data/app.db` on first run. The database schema includes:

- **notes**: Stores note content with auto-generated IDs and timestamps
- **action_items**: Stores extracted action items, optionally linked to notes via `note_id`

## API Endpoints

### Action Items

#### `POST /action-items/extract`

Extract action items from text using rule-based heuristics.

**Request Body:**
```json
{
  "text": "Meeting notes:\n- [ ] Set up database\n* Implement API",
  "save_note": false
}
```

**Response:**
```json
{
  "note_id": null,
  "items": [
    {"id": 1, "text": "Set up database"},
    {"id": 2, "text": "Implement API"}
  ]
}
```

**Features:**
- Detects bullet points (`-`, `*`, `•`, numbered lists)
- Recognizes keywords (`TODO:`, `Action:`, `Next:`)
- Identifies checkboxes (`[ ]`, `[todo]`)
- Falls back to imperative sentence detection
- Optionally saves the input text as a note when `save_note: true`

#### `POST /action-items/extract-llm`

Extract action items using LLM-based extraction (requires Ollama).

**Request/Response:** Same as `/extract` endpoint.

**Features:**
- Uses Ollama with `phi3:mini` model
- Better context understanding than rule-based extraction
- Handles malformed JSON responses gracefully
- Returns empty list if model output cannot be parsed

#### `GET /action-items`

List all action items, optionally filtered by note ID.

**Query Parameters:**
- `note_id` (optional): Filter action items by note ID

**Response:**
```json
[
  {
    "id": 1,
    "note_id": 5,
    "text": "Set up database",
    "done": false,
    "created_at": "2025-01-26 10:30:00"
  }
]
```

#### `POST /action-items/{action_item_id}/done`

Mark an action item as done or undone.

**Request Body:**
```json
{
  "done": true
}
```

**Response:**
```json
{
  "id": 1,
  "done": true
}
```

### Notes

#### `POST /notes`

Create a new note.

**Request Body:**
```json
{
  "content": "Meeting notes from sprint planning"
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Meeting notes from sprint planning",
  "created_at": "2025-01-26 10:30:00"
}
```

#### `GET /notes`

List all notes, ordered by ID descending (newest first).

**Response:**
```json
[
  {
    "id": 2,
    "content": "Latest note",
    "created_at": "2025-01-26 11:00:00"
  },
  {
    "id": 1,
    "content": "Earlier note",
    "created_at": "2025-01-26 10:30:00"
  }
]
```

#### `GET /notes/{note_id}`

Retrieve a single note by ID.

**Response:**
```json
{
  "id": 1,
  "content": "Meeting notes from sprint planning",
  "created_at": "2025-01-26 10:30:00"
}
```

**Error:** Returns 404 if note not found.

## Running Tests

The test suite uses pytest and includes tests for both rule-based and LLM-based extraction.

### Run All Tests

From the repository root, with the Conda environment activated:

```bash
cd week2
PYTHONPATH=. poetry run pytest tests/ -v
```

Or from the project root:

```bash
PYTHONPATH=week2 poetry run pytest week2/tests/ -v
```

### Test Structure

- **`test_extract_bullets_and_checkboxes`**: Tests rule-based extraction with various input formats
- **`test_extract_action_items_llm_empty_input_returns_empty_list`**: Verifies LLM extraction handles empty input
- **`test_extract_action_items_llm_bullet_point_input_returns_non_empty_list`**: Tests LLM extraction with bullet points
- **`test_extract_action_items_llm_keyword_input_returns_list`**: Tests LLM extraction with keyword prefixes

### Note on LLM Tests

LLM-based tests avoid asserting exact string matches due to non-deterministic model output. Instead, they verify:
- Return type is a list of strings
- List is non-empty when input contains action items
- All items are non-empty strings

**Important:** LLM tests require Ollama to be running with the `phi3:mini` model available. If tests fail with "model not found", ensure Ollama is running and the model is pulled.

## Implementation Notes

### Extraction Methods

**Rule-based (`extract_action_items`):**
- Uses regex patterns to detect bullet points and numbered lists
- Checks for keyword prefixes (`todo:`, `action:`, `next:`)
- Identifies checkbox markers (`[ ]`, `[todo]`)
- Falls back to sentence splitting and imperative detection
- Deduplicates results while preserving order

**LLM-based (`extract_action_items_llm`):**
- Uses Ollama's `phi3:mini` model for extraction
- Requests JSON array output from the model
- Handles malformed responses by extracting JSON from markdown code blocks
- Validates and filters results to ensure list of strings
- Returns empty list on any parsing errors

### API Design

The API uses Pydantic models for request/response validation:
- **Type safety**: Automatic validation of request payloads
- **Documentation**: FastAPI generates OpenAPI/Swagger docs from models
- **Error handling**: Clear validation errors for invalid inputs
- **Field validation**: Text fields are validated for non-empty content (after stripping)

### Database

- SQLite database stored in `week2/data/app.db`
- Tables created automatically on first run via `init_db()`
- Foreign key relationship: `action_items.note_id` → `notes.id`
- Database operations use context managers for connection handling

### Frontend

- Minimal HTML/JavaScript interface (no build tools required)
- Served directly by FastAPI at the root path (`/`)
- Static files mounted at `/static` for future assets
- All API calls use `fetch()` with JSON payloads

## Troubleshooting

### Ollama Connection Issues

If LLM extraction fails:
1. Verify Ollama is running: `ollama list` should show available models
2. Ensure `phi3:mini` is pulled: `ollama pull phi3:mini`
3. Check Ollama service is accessible (default: http://localhost:11434)

### Database Errors

If database operations fail:
1. Check that `week2/data/` directory exists and is writable
2. Verify SQLite is working: `sqlite3 week2/data/app.db "SELECT 1;"`
3. Delete `app.db` to reset the database (data will be lost)

### Import Errors

If you see import errors when running tests:
- Ensure you're using `PYTHONPATH=.` or `PYTHONPATH=week2` when running pytest
- Verify the Conda environment is activated
- Check that dependencies are installed: `poetry show`

## License

This project is part of CS146S course assignments at Stanford University.
