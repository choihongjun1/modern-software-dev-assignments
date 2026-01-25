from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Request Schemas
# ============================================================================
# These models define the expected structure of incoming request payloads.
# Using Pydantic provides automatic validation, type checking, and clear
# API documentation via FastAPI's OpenAPI/Swagger integration.
# ============================================================================


class ExtractActionItemsRequest(BaseModel):
    """Request schema for extracting action items from text.
    
    Attributes:
        text: The input text to extract action items from. Required and must be non-empty
              after stripping whitespace (whitespace-only strings are rejected).
        save_note: Optional flag to save the text as a note in the database.
    """
    text: str = Field(..., min_length=1, description="Text content to extract action items from")
    save_note: Optional[bool] = Field(default=False, description="Whether to save the text as a note")
    
    @field_validator("text")
    @classmethod
    def validate_text_not_empty_after_strip(cls, v: str) -> str:
        """Ensure text is non-empty after stripping whitespace and return stripped value.
        
        This maintains the original behavior where whitespace-only strings
        are rejected. The validator also strips the text, so the endpoint
        receives a clean value without needing to call .strip() again.
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("text must not be empty or whitespace-only")
        return stripped


class MarkDoneRequest(BaseModel):
    """Request schema for marking an action item as done/undone.
    
    Attributes:
        done: Boolean flag indicating whether the action item is done. Defaults to True.
    """
    done: bool = Field(default=True, description="Whether the action item is marked as done")


class CreateNoteRequest(BaseModel):
    """Request schema for creating a new note.
    
    Attributes:
        content: The note content. Required and must be non-empty after stripping
                 whitespace (whitespace-only strings are rejected).
    """
    content: str = Field(..., min_length=1, description="Note content text")
    
    @field_validator("content")
    @classmethod
    def validate_content_not_empty_after_strip(cls, v: str) -> str:
        """Ensure content is non-empty after stripping whitespace and return stripped value.
        
        This maintains the original behavior where whitespace-only strings
        are rejected. The validator also strips the content, so the endpoint
        receives a clean value without needing to call .strip() again.
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("content must not be empty or whitespace-only")
        return stripped


# ============================================================================
# Response Schemas
# ============================================================================
# These models define the structure of API responses, ensuring consistency
# and providing clear contracts for API consumers. Response models also
# enable automatic OpenAPI documentation generation.
# ============================================================================


class ActionItemResponse(BaseModel):
    """Response schema for a single action item.
    
    This represents an action item in API responses, including its ID,
    associated note (if any), text content, completion status, and timestamp.
    """
    id: int = Field(..., description="Unique identifier for the action item")
    text: str = Field(..., description="The action item text content")
    note_id: Optional[int] = Field(None, description="ID of the associated note, if any")
    done: bool = Field(..., description="Whether the action item is completed")
    created_at: str = Field(..., description="ISO timestamp when the action item was created")


class ActionItemSummary(BaseModel):
    """Simplified action item schema for extract endpoint responses.
    
    This is a lighter-weight representation used in the extract endpoint
    response, containing only the ID and text of extracted items.
    """
    id: int = Field(..., description="Unique identifier for the action item")
    text: str = Field(..., description="The action item text content")


class ExtractActionItemsResponse(BaseModel):
    """Response schema for the extract action items endpoint.
    
    Returns the extracted action items along with an optional note ID
    if the text was saved as a note.
    """
    note_id: Optional[int] = Field(None, description="ID of the saved note, if save_note was True")
    items: list[ActionItemSummary] = Field(..., description="List of extracted action items")


class MarkDoneResponse(BaseModel):
    """Response schema for marking an action item as done/undone.
    
    Returns the action item ID and its updated done status.
    """
    id: int = Field(..., description="The action item ID that was updated")
    done: bool = Field(..., description="The updated done status")


class NoteResponse(BaseModel):
    """Response schema for a note.
    
    This represents a note in API responses, including its ID, content,
    and creation timestamp.
    """
    id: int = Field(..., description="Unique identifier for the note")
    content: str = Field(..., description="The note content text")
    created_at: str = Field(..., description="ISO timestamp when the note was created")
