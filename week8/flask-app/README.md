# Developer Control Center (Version 3)

## Project Overview

Developer Control Center is a task management web application. This version is a minimal, manually implemented Flask application: a single backend file, SQLite used directly (no ORM), and a simple HTML page with vanilla JavaScript. It is intended for local development only.

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (via the `sqlite3` standard library; no ORM)
- **Frontend:** HTML + Vanilla JavaScript (fetch API)

## Features

- Create, list, and delete tasks
- Task status support: `todo`, `in_progress`, `done`

## Prerequisites

- Python 3.10 or later
- pip

## Installation

Navigate to the Flask app directory:

```bash
cd week8/flask-app
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

Install Flask:

```bash
pip install flask
```

## Running the Application

Start the server:

```bash
python app.py
```

Open a browser and go to **http://127.0.0.1:5000**.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create a task |
| DELETE | `/api/tasks/<id>` | Delete a task by ID |

## Notes

- This version avoids ORMs and frontend frameworks to keep the stack minimal and to highlight low-level control over the database and UI.
- The SQLite database file is created and tables are initialized automatically when the app starts (if they do not already exist).
- This code was implemented with assistance from Cursor as an AI coding assistant.
