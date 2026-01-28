from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select, text
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Note, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    sql = text(
        f"""
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql).all()
    results: list[NoteRead] = []
    for r in rows:
        results.append(
            NoteRead(
                id=r.id,
                title=r.title,
                content=r.content,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
        )
    return results


@router.get("/debug/hash-md5")
def debug_hash_md5(q: str) -> dict[str, str]:
    import hashlib

    return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}


@router.get("/debug/eval")
def debug_eval(expr: str) -> dict[str, str]:
    import ast
    import operator

    # SECURITY: `expr` is user-controlled. Never use eval()/exec() here.
    # Instead, we support a tiny allowlist: basic arithmetic expressions only.
    #
    # Allowed:
    # - numeric literals (int/float)
    # - unary +/-
    # - binary ops: +, -, *, /, %, **, //
    #
    # Disallowed (examples): names, attribute access, function calls, subscripts,
    # comprehensions, lambdas, imports, etc.

    allowed_binops: dict[type[ast.operator], object] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    allowed_unaryops: dict[type[ast.unaryop], object] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def _eval(node: ast.AST) -> float | int:
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_unaryops:
            return allowed_unaryops[type(node.op)](_eval(node.operand))  # type: ignore[misc]

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_binops:
            return allowed_binops[type(node.op)](_eval(node.left), _eval(node.right))  # type: ignore[misc]

        # Anything else is rejected to avoid executing arbitrary Python.
        raise ValueError("Only basic arithmetic expressions are allowed")

    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval(tree)
        return {"result": str(result)}
    except Exception as exc:  # noqa: BLE001
        # Preserve a simple JSON shape; treat invalid expressions as bad input.
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    import subprocess
    import sys
    import os

    # SECURITY: `cmd` is user-controlled input. Never execute it via a shell.
    # We enforce a strict allowlist of safe, fixed commands and execute using
    # an argument list with shell=False to prevent OS command injection.
    #
    # Note: We intentionally do NOT support arbitrary arguments (e.g. `ls -la`)
    # to keep the surface area minimal and predictable.
    normalized = (cmd or "").strip()

    # Map allowed "commands" to safe, fixed argument lists.
    # We implement `pwd`/`ls` via the current Python interpreter to be portable
    # and to avoid relying on shell builtins (e.g. Windows `dir`).
    allowlist: dict[str, list[str]] = {
        "whoami": ["whoami"],
        "pwd": [sys.executable, "-c", "import os; print(os.getcwd())"],
        "ls": [sys.executable, "-c", "import os; print('\\n'.join(sorted(os.listdir('.'))))"],
    }

    args = allowlist.get(normalized)
    if args is None:
        # Keep the response format unchanged (returncode/stdout/stderr),
        # but refuse to run anything outside the allowlist.
        return {
            "returncode": "1",
            "stdout": "",
            "stderr": f"Command not allowed. Allowed: {', '.join(sorted(allowlist.keys()))}",
        }

    completed = subprocess.run(args, shell=False, capture_output=True, text=True)  # noqa: S603
    return {"returncode": str(completed.returncode), "stdout": completed.stdout, "stderr": completed.stderr}


@router.get("/debug/fetch")
def debug_fetch(url: str) -> dict[str, str]:
    from urllib.request import urlopen

    with urlopen(url) as res:  # noqa: S310
        body = res.read(1024).decode(errors="ignore")
    return {"snippet": body}


@router.get("/debug/read")
def debug_read(path: str) -> dict[str, str]:
    try:
        content = open(path, "r").read(1024)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}

