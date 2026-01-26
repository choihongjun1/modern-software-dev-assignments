def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

def test_mark_note_completed(client):
    response = client.post(
        "/notes",
        json={
            "title": "Test Title",
            "content": "test note"
        }
    )
    assert response.status_code == 201
    note_id = response.json()["id"]

    response = client.post(f"/notes/{note_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

