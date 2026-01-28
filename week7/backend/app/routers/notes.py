from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

MAX_LIMIT = 200


def _validate_pagination(skip: int, limit: int) -> None:
    if skip < 0:
        raise HTTPException(status_code=400, detail="Invalid pagination: skip must be >= 0")
    if limit < 1 or limit > MAX_LIMIT:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid pagination: limit must be between 1 and {MAX_LIMIT}",
        )


def _apply_sort(stmt, model, sort: str):
    allowed_fields = set(model.__table__.columns.keys())
    if not sort or not sort.strip():
        raise HTTPException(status_code=400, detail="Invalid sort: sort must be a non-empty string")

    sort_str = sort.strip()
    sort_field = sort_str.lstrip("-")
    if not sort_field:
        raise HTTPException(status_code=400, detail="Invalid sort: missing sort field")

    if sort_field not in allowed_fields:
        allowed = ", ".join(sorted(allowed_fields))
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field '{sort_field}'. Allowed fields: {allowed}",
        )

    order_fn = desc if sort_str.startswith("-") else asc
    return stmt.order_by(order_fn(getattr(model, sort_field)))


def _reject_blank(value: str, field_name: str) -> None:
    if value.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid input: '{field_name}' cannot be empty")


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    _validate_pagination(skip, limit)
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    stmt = _apply_sort(stmt, Note, sort)

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    _reject_blank(payload.title, "title")
    _reject_blank(payload.content, "content")
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
        _reject_blank(payload.title, "title")
        note.title = payload.title
    if payload.content is not None:
        _reject_blank(payload.content, "content")
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


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Response:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
    return Response(status_code=204)


