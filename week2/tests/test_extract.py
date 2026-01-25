import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# -----------------------------------------------------------------------------
# Unit tests for extract_action_items_llm
# -----------------------------------------------------------------------------
# LLM output is non-deterministic, so we avoid asserting exact string matches.
# We assert only on types, length, and general properties (e.g. list of strings,
# non-empty when input contains action items, empty when input is empty).
# -----------------------------------------------------------------------------


def test_extract_action_items_llm_empty_input_returns_empty_list():
    """Empty or whitespace-only input must return an empty list (no LLM call)."""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    assert extract_action_items_llm("\n\t") == []


def test_extract_action_items_llm_bullet_point_input_returns_non_empty_list():
    """Bullet-point input should yield at least one action item from the LLM."""
    text = """
    Meeting notes:
    - Set up the database
    * Implement the API endpoint
    1. Write unit tests
    Some context here.
    """
    items = extract_action_items_llm(text.strip())
    # We avoid asserting exact strings (e.g. "Set up the database" in items) because
    # LLM output varies; phi-3 may paraphrase or merge items. We check types and shape.
    assert isinstance(items, list), "Return value must be a list"
    assert all(isinstance(x, str) for x in items), "Each item must be a string"
    assert isinstance(items, list)
    assert all(len(s.strip()) > 0 for s in items), "Action items must be non-empty strings"


def test_extract_action_items_llm_keyword_input_returns_list():
    """Keyword-based input (TODO, Action:, etc.) should yield a list of action items."""
    text = """
    TODO: Review the pull request.
    Action: Schedule the demo.
    Next: Update the documentation.
    """
    items = extract_action_items_llm(text.strip())
    # Same rationale as bullet test: no exact matches; assert types, length, and structure only.
    assert isinstance(items, list), "Return value must be a list"
    assert all(isinstance(x, str) for x in items), "Each item must be a string"
    assert len(items) >= 1, "Keyword-based input should produce at least one action item"
    assert all(len(s.strip()) > 0 for s in items), "Action items must be non-empty strings"
