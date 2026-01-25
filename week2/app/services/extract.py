from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str) -> list[str]:
    """
    Extract action items from text using Ollama with phi-3 model.
    
    This function uses a local LLM to identify action items in the provided text.
    It requests the model to return only a JSON array of strings, and handles
    various edge cases including empty input and malformed model responses.
    
    Args:
        text: The input text containing notes or meeting minutes to extract action items from.
        
    Returns:
        A list of action item strings. Returns an empty list if:
        - The input text is empty
        - The model output cannot be parsed as valid JSON
        - The parsed JSON is not a list of strings
    """
    # Return empty list for empty input
    if not text or not text.strip():
        return []
    
    # System prompt instructs the model to output only JSON array of strings
    system_prompt = """You are a helpful assistant that extracts action items from notes or meeting minutes.

Your task is to identify action items (tasks, todos, things that need to be done) from the provided text.

Output requirements:
- Output ONLY a JSON array of strings
- Each string should be a single action item
- Do not include any explanations, markdown formatting, or additional text
- The output must be valid JSON that can be parsed directly
- Example format: ["Action item 1", "Action item 2", "Action item 3"]"""

    user_prompt = f"""Extract all action items from the following text. Return ONLY a JSON array of strings, nothing else:

{text}"""

    try:
        # Call Ollama with phi-3 model
        response = chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": 0.3},  # Lower temperature for more consistent JSON output
        )
        
        # Get the raw response content
        output_text = response.message.content.strip()
        
        # Try to extract JSON from markdown code blocks if present
        # Some models wrap JSON in ```json ... ``` blocks
        json_match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", output_text, re.DOTALL)
        if json_match:
            output_text = json_match.group(1).strip()
        
        # Try to find JSON array pattern even if not in code blocks
        # Look for content that starts with [ and ends with ]
        if not output_text.startswith("["):
            json_match = re.search(r"\[.*?\]", output_text, re.DOTALL)
            if json_match:
                output_text = json_match.group(0).strip()
        
        # Parse the JSON response
        parsed = json.loads(output_text)
        
        # Validate that the parsed result is a list
        if not isinstance(parsed, list):
            return []
        
        # Filter to ensure all items are strings and non-empty
        action_items = [str(item).strip() for item in parsed if item]
        return [item for item in action_items if item]  # Remove empty strings
        
    except (json.JSONDecodeError, AttributeError, KeyError, TypeError) as e:
        # Handle malformed model output gracefully
        # JSONDecodeError: invalid JSON
        # AttributeError: response structure unexpected
        # KeyError: missing expected keys in response
        # TypeError: unexpected data types
        return []
