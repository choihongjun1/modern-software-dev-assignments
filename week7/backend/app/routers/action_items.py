from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemPatch, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action_items"])

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


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,
    sort: str = Query("-created_at"),
) -> list[ActionItemRead]:
    _validate_pagination(skip, limit)
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))

    stmt = _apply_sort(stmt, ActionItem, sort)

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    _reject_blank(payload.description, "description")
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    if payload.description is not None:
        _reject_blank(payload.description, "description")
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    db.delete(item)
    db.flush()
    return Response(status_code=204)


