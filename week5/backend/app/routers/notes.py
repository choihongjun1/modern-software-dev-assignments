from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note, ActionItem
from ..schemas import NoteCreate, NoteRead
from ..services.extract import extract_action_items

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(db: Session = Depends(get_db)) -> list[NoteRead]:
    rows = db.execute(select(Note)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search/", response_model=list[NoteRead])
def search_notes(q: Optional[str] = None, db: Session = Depends(get_db)) -> list[NoteRead]:
    if not q:
        rows = db.execute(select(Note)).scalars().all()
    else:
        rows = (
            db.execute(
                select(Note).where(
                    (Note.title.contains(q)) | (Note.content.contains(q))
                )
            )
            .scalars()
            .all()
        )
    return [NoteRead.model_validate(row) for row in rows]


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.post("/{note_id}/extract")
def extract_note(
    note_id: int,
    apply: bool = Query(
        False,
        description="If true, persist extracted action items to the database",
    ),
    db: Session = Depends(get_db),
):
    """
    Extract action items from a note.

    - apply=false (default): preview only
    - apply=true: persist new ActionItems (idempotent)
    """
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    extracted = extract_action_items(note.content or "")

    if not apply:
        return {
            "note_id": note.id,
            "mode": "preview",
            "extracted": extracted,
            "created": [],
        }

    existing = {
        ai.description.lower()
        for ai in db.execute(select(ActionItem)).scalars().all()
    }

    created = []
    for desc in extracted:
        if desc.lower() in existing:
            continue

        item = ActionItem(
            description=desc,
            completed=False,
        )
        db.add(item)
        db.flush()  

        created.append(
            {
                "id": item.id,
                "description": item.description,
                "completed": item.completed,
            }
        )

    db.commit()

    return {
        "note_id": note.id,
        "mode": "apply",
        "extracted": extracted,
        "created": created,
    }
