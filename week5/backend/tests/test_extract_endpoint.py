def _create_note(client, title="T", content="Hello"):
    r = client.post("/notes/", json={"title": title, "content": content})
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["ok"] is True
    return body["data"]


def test_extract_preview_does_not_persist_action_items(client):
    note = _create_note(
        client,
        content="""
        Some note
        - TODO: write tests
        - Ship it!
        """.strip(),
    )

    r = client.post(f"/notes/{note['id']}/extract")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    data = body["data"]

    assert data["mode"] == "preview"
    assert "TODO: write tests" in data["extracted"]
    assert "Ship it!" in data["extracted"]
    assert data["created"] == []

    r = client.get("/action-items/")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["data"] == []



def test_extract_apply_persists_action_items(client):
    note = _create_note(
        client,
        content="""
        - TODO: write tests
        - Ship it!
        """.strip(),
    )

    r = client.post(f"/notes/{note['id']}/extract", params={"apply": "true"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    data = body["data"]

    assert data["mode"] == "apply"

    assert len(data["created"]) == 2

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()["data"]

    assert len(items) == 2
    assert {i["description"] for i in items} == {
        "TODO: write tests",
        "Ship it!",
    }
    assert all(i["completed"] is False for i in items)


def test_extract_apply_is_idempotent(client):
    note = _create_note(
        client,
        content="""
        - TODO: write tests
        - Ship it!
        """.strip(),
    )

    client.post(f"/notes/{note['id']}/extract", params={"apply": "true"})
    r = client.get("/action-items/")
    first = r.json()["data"]
    assert len(first) == 2

    client.post(f"/notes/{note['id']}/extract", params={"apply": "true"})
    r = client.get("/action-items/")
    second = r.json()["data"]
    assert len(second) == 2  # no duplicates


def test_extract_note_not_found(client):
    r = client.post("/notes/999999/extract")
    assert r.status_code == 404
    err = r.json()
    assert err["ok"] is False
    assert err["error"]["code"] == "NOT_FOUND"


def test_extract_no_actionable_content(client):
    note = _create_note(
        client,
        content="This note has nothing actionable.",
    )

    r = client.post(f"/notes/{note['id']}/extract")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["data"]["extracted"] == []

    r = client.post(f"/notes/{note['id']}/extract", params={"apply": "true"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["data"]["created"] == []

    r = client.get("/action-items/")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["data"] == []
