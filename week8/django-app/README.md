# Developer Control Center (Version 2)

## Project Overview

Developer Control Center is a task management web application. This version provides a REST API backend for creating, viewing, updating, and deleting tasks. It is intended for local development and demonstration.

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite

## Features

- Full CRUD operations for tasks
- Task status management: `todo`, `in_progress`, `done`

## Prerequisites

- Python 3.10 or later (or as required by your course)
- pip (Python package installer)
- A virtual environment is optional but recommended

## Installation

From the repository root, navigate to the Django app directory:

```bash
cd week8/django-app
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

Install dependencies:

```bash
pip install django djangorestframework
```

## Database Setup

Apply migrations to create the SQLite database and tables:

```bash
python manage.py migrate
```

## Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The API is available at **http://127.0.0.1:8000/api/tasks/**.

## API Endpoints

All task endpoints are under `/api/tasks/`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<id>/` | Retrieve a task |
| PUT | `/api/tasks/<id>/` | Update a task (full) |
| PATCH | `/api/tasks/<id>/` | Update a task (partial) |
| DELETE | `/api/tasks/<id>/` | Delete a task |

## Notes

- This version uses a traditional backend-driven architecture with Django and Django REST Framework.
- Django REST Framework provides a browsable API: you can open `/api/tasks/` in a browser to list and manage tasks via the built-in UI.
- No authentication is implemented; the app is for local/demo use only.
- This code was implemented with assistance from Cursor as an AI coding assistant.
