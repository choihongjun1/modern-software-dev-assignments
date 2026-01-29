def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204, r.text

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 404


def test_notes_pagination_limit(client):
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
    r = client.get("/notes/", params={"limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_notes_pagination_skip(client):
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
    r_first = client.get("/notes/", params={"limit": 2, "skip": 0})
    r_second = client.get("/notes/", params={"limit": 2, "skip": 2})
    assert r_first.status_code == 200 and r_second.status_code == 200
    first_ids = {n["id"] for n in r_first.json()}
    second_ids = {n["id"] for n in r_second.json()}
    assert first_ids != second_ids
    assert len(first_ids) == 2 and len(second_ids) == 2


def test_notes_sort_created_at_desc(client):
    ids = []
    for i in range(3):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
        ids.append(r.json()["id"])
    r = client.get("/notes/", params={"limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 3
    first_three_ids = [items[i]["id"] for i in range(3)]
    assert first_three_ids == sorted(ids, reverse=True)


def test_notes_sort_created_at_asc(client):
    ids = []
    for i in range(3):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
        ids.append(r.json()["id"])
    r = client.get("/notes/", params={"limit": 10, "sort": "created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 3
    first_three_ids = [items[i]["id"] for i in range(3)]
    assert first_three_ids == sorted(ids)


def test_notes_sort_invalid_field_returns_400(client):
    r = client.get("/notes/", params={"sort": "invalid_field"})
    assert r.status_code == 400
    assert "invalid" in r.json().get("detail", "").lower() or "allowed" in r.json().get("detail", "").lower()
