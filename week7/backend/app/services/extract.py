import re

def extract_action_items(text: str) -> list[str]:

    def _strip_leading_markers(s: str) -> str:
        # Remove leading bullets/checkboxes/numbering while preserving capitalization.
        s = s.strip()
        s = re.sub(r"^\s*(?:[-*•]+|\[[ xX]\])\s+", "", s)
        s = re.sub(r"^\s*\(?\d{1,3}\)?[.)]\s+", "", s)
        s = re.sub(r"^\s*[a-zA-Z][.)]\s+", "", s)
        return s.strip()

    def _is_question(s: str) -> bool:
        s_stripped = s.strip()
        if s_stripped.endswith("?"):
            return True
        return bool(re.match(r"^\s*(who|what|when|where|why|how|can|could|should|would|do|does|did|is|are|was|were|will)\b",
                             s_stripped,
                             flags=re.IGNORECASE))

    def _is_too_vague(s: str) -> bool:
        # Avoid very short/vague fragments.
        if len(s.strip()) < 12:
            return True
        word_count = len(re.findall(r"\b[\w'-]+\b", s))
        if word_count < 3:
            return True
        if re.fullmatch(r"(?i)\s*(todo|tbd|asap|follow up|next steps|action item)\s*[:\-]?\s*", s.strip()):
            return True
        return False

    def _looks_informational(s: str) -> bool:
        # Heuristic: statements that look like status/info rather than a request/plan.
        return bool(
            re.match(
                r"^\s*(note|fyi|info|heads up|status|update)\b",
                s,
                flags=re.IGNORECASE,
            )
        )

    # Prefix patterns (explicit labels)
    prefix_re = re.compile(
        r"^\s*(?:todo|action|action item|follow up|follow-up|next steps)\s*[:\-]\s*(.+)$",
        flags=re.IGNORECASE,
    )

    # Sentence starters like "we should", "we need to", "please", "let's"
    starter_re = re.compile(
        r"^\s*(?:we\s+(?:should|need\s+to|have\s+to|must)\b|please\b|let['’]s\b)\s+(.+)$",
        flags=re.IGNORECASE,
    )

    # Imperative verbs at the beginning of a line
    imperative_verbs = [
        "update",
        "fix",
        "send",
        "review",
        "create",
        "add",
        "remove",
        "refactor",
        "investigate",
        "check",
        "follow",
        "follow up",
        "schedule",
        "confirm",
        "notify",
        "document",
        "test",
        "deploy",
        "reply",
        "call",
        "email",
        "meet",
    ]
    imperative_re = re.compile(
        r"^\s*(?:" + "|".join(re.escape(v) for v in sorted(imperative_verbs, key=len, reverse=True)) + r")\b",
        flags=re.IGNORECASE,
    )

    # Split into lines; also handle multiple sentences per line conservatively.
    raw_lines = [ln for ln in text.splitlines() if ln.strip()]
    candidates: list[str] = []

    for raw in raw_lines:
        line = raw.strip()
        cleaned = _strip_leading_markers(line)
        if not cleaned:
            continue

        # If it contains multiple sentences, extract those that individually look actionable.
        parts = re.split(r"(?<=[.!?])\s+", cleaned)
        if len(parts) == 1:
            parts = [cleaned]

        for part in parts:
            part = part.strip()
            if not part:
                continue

            m = prefix_re.match(part)
            actionable = False

            if m:
                part = m.group(1).strip()
                part = _strip_leading_markers(part)
                actionable = True  

            if starter_re.match(part):
                actionable = True
            elif imperative_re.match(part):
                actionable = True
            elif part.endswith("!") and len(part) >= 12:
                actionable = True

            if not actionable:
                continue


            if _is_question(part):
                continue

            if _looks_informational(part):
                continue

            # Avoid fragments that are basically just an opener.
            part = part.strip().strip("–-").strip()
            if _is_too_vague(part):
                continue

            # Trim trailing punctuation noise while keeping normal punctuation.
            part = part.strip()
            part = re.sub(r"\s+", " ", part)
            part = part.rstrip()
            candidates.append(part)

    # Deduplicate while preserving order and original capitalization.
    seen: set[str] = set()
    results: list[str] = []
    for item in candidates:
        key = re.sub(r"\s+", " ", item).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        results.append(item)

    return results


