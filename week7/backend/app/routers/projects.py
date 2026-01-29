from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note, Project
from ..schemas import NoteRead, ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


def _reject_blank(value: str, field_name: str) -> None:
    if value.strip() == "":
        raise HTTPException(status_code=400, detail=f"Invalid input: '{field_name}' cannot be empty")


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    _reject_blank(payload.name, "name")
    project = Project(name=payload.name)
    db.add(project)
    db.flush()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.model_validate(project)


@router.get("/{project_id}/notes", response_model=list[NoteRead])
def list_project_notes(project_id: int, db: Session = Depends(get_db)) -> list[NoteRead]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    stmt = select(Note).where(Note.project_id == project_id).order_by(Note.created_at.desc())
    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]
