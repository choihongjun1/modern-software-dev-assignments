from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_action_items_sentence_starters():
    text = """
    We should update the README.
    Please send the report by EOD.
    Let's review the PR tomorrow.
    """.strip()
    items = extract_action_items(text)
    assert "We should update the README." in items
    assert "Please send the report by EOD." in items
    assert "Let's review the PR tomorrow." in items
    assert "We should update the README.?" not in items


def test_extract_action_items_imperative_verbs():
    text = """
    Update dependencies in the backend.
    Send the invoice to accounting.
    Review the new onboarding doc.
    """.strip()
    items = extract_action_items(text)
    assert "Update dependencies in the backend." in items
    assert "Send the invoice to accounting." in items
    assert "Review the new onboarding doc." in items


def test_extract_action_items_avoids_questions_and_informational_prefixes():
    text = """
    Can you update the docs?
    Should we send the email now?
    FYI: the deploy finished successfully.
    Note: the meeting is at 3pm.
    Please update the docs.
    """.strip()
    items = extract_action_items(text)
    assert "Please update the docs." in items
    assert "Can you update the docs?" not in items
    assert "Should we send the email now?" not in items
    assert "FYI: the deploy finished successfully." not in items
    assert "Note: the meeting is at 3pm." not in items


def test_extract_action_items_deduplicates_equivalent_items():
    text = """
    - Please send the report by EOD.
    Please send the report by EOD.
    please send the report by EOD.
    """.strip()
    items = extract_action_items(text)
    assert "Please send the report by EOD." in items
    assert len(items) == 1

