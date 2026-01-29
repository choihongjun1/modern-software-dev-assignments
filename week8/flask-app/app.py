import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DB_PATH = Path(__file__).resolve().parent / "tasks.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'todo',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


def row_to_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"] or "",
        "status": row["status"],
        "created_at": row["created_at"],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, description, status, created_at FROM task ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    tasks = [row_to_task(row) for row in rows]
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True, silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required and cannot be empty"}), 400

    description = (data.get("description") or "").strip()
    status = (data.get("status") or "todo").strip()
    if status not in ("todo", "in_progress", "done"):
        status = "todo"

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO task (title, description, status) VALUES (?, ?, ?)",
        (title, description, status),
    )
    conn.commit()
    task_id = cursor.lastrowid
    row = conn.execute(
        "SELECT id, title, description, status, created_at FROM task WHERE id = ?",
        (task_id,),
    ).fetchone()
    conn.close()

    task = row_to_task(row)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cursor = conn.execute("DELETE FROM task WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "task not found"}), 404
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
