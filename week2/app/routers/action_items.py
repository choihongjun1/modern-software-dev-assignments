from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from .. import db
from ..schemas import (
    ActionItemResponse,
    ActionItemSummary,
    ExtractActionItemsRequest,
    ExtractActionItemsResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

# ============================================================================
# Refactoring Notes
# ============================================================================
# This router was refactored to replace raw Dict[str, Any] request/response
# handling with explicit Pydantic models. Benefits include:
#
# 1. Type Safety: Pydantic validates request payloads automatically, catching
#    type errors and missing required fields before handler execution.
#
# 2. API Documentation: FastAPI automatically generates OpenAPI/Swagger docs
#    from Pydantic models, providing clear contracts for API consumers.
#
# 3. Code Clarity: Request/response structures are now explicit and self-
#    documenting, making the API easier to understand and maintain.
#
# 4. Validation: Field-level validation (e.g., min_length) is handled by
#    Pydantic, reducing manual validation code in handlers.
#
# 5. IDE Support: Type hints enable better autocomplete and static analysis.
# ============================================================================

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractActionItemsResponse)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    """Extract action items from text, optionally saving the text as a note.
    
    The request payload is now validated by Pydantic: the 'text' field is
    required, must be non-empty (min_length=1), and cannot be whitespace-only.
    The Pydantic validator also strips the text, so payload.text is already
    clean and ready to use. This replaces the manual validation and stripping
    that was previously done in the handler.
    
    This endpoint uses rule-based extraction (regex patterns and heuristics).
    """
    # Pydantic validator ensures text is non-empty and already stripped
    text = payload.text
    
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)
    
    # Build response using Pydantic model for type safety and validation
    return ExtractActionItemsResponse(
        note_id=note_id,
        items=[ActionItemSummary(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.post("/extract-llm", response_model=ExtractActionItemsResponse)
def extract_llm(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    """Extract action items from text using LLM, optionally saving the text as a note.
    
    This endpoint uses the same request/response schemas as /extract but employs
    an LLM-based extraction method (extract_action_items_llm) instead of rule-based
    heuristics. The LLM approach can better understand context and extract action
    items that may not match predefined patterns.
    
    The request payload is validated by Pydantic: the 'text' field is required,
    must be non-empty (min_length=1), and cannot be whitespace-only. The behavior
    is consistent with /extract, including support for save_note.
    """
    # Pydantic validator ensures text is non-empty and already stripped
    text = payload.text
    
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(text)

    # Use LLM-based extraction instead of rule-based extraction
    items = extract_action_items_llm(text)
    ids = db.insert_action_items(items, note_id=note_id)
    
    # Build response using Pydantic model for type safety and validation
    return ExtractActionItemsResponse(
        note_id=note_id,
        items=[ActionItemSummary(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: Optional[int] = Query(None, description="Filter by note ID")) -> list[ActionItemResponse]:
    """List all action items, optionally filtered by note_id.
    
    Query parameters are now explicitly defined using FastAPI's Query() for
    better documentation. The response uses a Pydantic model to ensure
    consistent structure across all action item responses.
    """
    rows = db.list_action_items(note_id=note_id)
    
    # Convert database rows to Pydantic models for consistent response structure
    # The bool() conversion for 'done' is preserved to handle SQLite's INTEGER
    # representation (0/1) correctly, maintaining the same behavior as before.
    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    """Mark an action item as done or undone.
    
    The request body is now a Pydantic model with a default value for 'done',
    making the API contract explicit. The default (True) matches the previous
    behavior where missing 'done' field defaulted to True.
    """
    # Pydantic model provides the default value, maintaining backward compatibility
    db.mark_action_item_done(action_item_id, payload.done)
    return MarkDoneResponse(id=action_item_id, done=payload.done)


