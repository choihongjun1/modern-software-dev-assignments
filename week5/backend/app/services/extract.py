import re
from typing import List


CHECKBOX_RE = re.compile(r"-\s*\[\s*\]\s*(.+)", re.IGNORECASE)
DASH_TODO_RE = re.compile(r"-\s*(todo:\s*.+)", re.IGNORECASE)
PLAIN_TODO_RE = re.compile(r"^\s*(todo:\s*.+)", re.IGNORECASE)
EXCLAMATION_RE = re.compile(r"-\s*(.+!)$")


def extract_action_items(text: str) -> List[str]:
    """
    Extract action item descriptions from free-form text.

    Supported patterns:
    - "- [ ] task description"
    - "- TODO: task description"
    - "TODO: task description"
    - "- task description!"   (ends with '!')
    """
    results: List[str] = []
    seen = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = (
            CHECKBOX_RE.match(line)
            or DASH_TODO_RE.match(line)
            or PLAIN_TODO_RE.match(line)
            or EXCLAMATION_RE.match(line)
        )

        if not match:
            continue

        item = match.group(1).strip()
        if not item:
            continue

        key = item.lower()
        if key not in seen:
            seen.add(key)
            results.append(item)

    return results
