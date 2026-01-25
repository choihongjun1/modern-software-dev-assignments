from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import CreateNoteRequest, NoteResponse

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
# 4. Validation: Field-level validation (e.g., min_length, whitespace checking)
#    is handled by Pydantic, reducing manual validation code in handlers.
#
# 5. IDE Support: Type hints enable better autocomplete and static analysis.
# ============================================================================

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=201)
def create_note(payload: CreateNoteRequest) -> NoteResponse:
    """Create a new note with the provided content.
    
    The request payload is now validated by Pydantic: the 'content' field is
    required, must be non-empty (min_length=1), and cannot be whitespace-only.
    The Pydantic validator also strips the content, so payload.content is
    already clean and ready to use. This replaces the manual validation and
    stripping that was previously done in the handler.
    
    Returns the created note with its generated ID and timestamp.
    """
    # Pydantic validator ensures content is non-empty and already stripped
    note_id = db.insert_note(payload.content)
    note = db.get_note(note_id)
    
    # Build response using Pydantic model for type safety and validation
    # Note: In practice, note should never be None here since we just inserted it,
    # but we maintain the original behavior of direct dict access.
    return NoteResponse(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """Retrieve a single note by its ID.
    
    The response uses a Pydantic model to ensure consistent structure.
    Returns 404 if the note is not found, maintaining the original behavior.
    """
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    
    # Convert database row to Pydantic model for consistent response structure
    return NoteResponse(
        id=row["id"],
        content=row["content"],
        created_at=row["created_at"],
    )


