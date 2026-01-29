def test_create_project(client):
    r = client.post("/projects/", json={"name": "Alpha"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Alpha"
    assert "id" in data and "created_at" in data and "updated_at" in data

    r = client.get(f"/projects/{data['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "Alpha"


def test_associate_note_with_project(client):
    r = client.post("/projects/", json={"name": "Beta"})
    assert r.status_code == 201, r.text
    project = r.json()
    project_id = project["id"]

    r = client.post(
        "/notes/",
        json={"title": "Project note", "content": "Details here", "project_id": project_id},
    )
    assert r.status_code == 201, r.text
    note = r.json()
    assert note["title"] == "Project note"

    r = client.get(f"/projects/{project_id}/notes")
    assert r.status_code == 200, r.text
    notes = r.json()
    assert len(notes) == 1
    assert notes[0]["id"] == note["id"] and notes[0]["title"] == "Project note"


def test_retrieve_notes_for_project(client):
    r = client.post("/projects/", json={"name": "Gamma"})
    assert r.status_code == 201, r.text
    project_id = r.json()["id"]

    client.post("/notes/", json={"title": "A", "content": "First", "project_id": project_id})
    client.post("/notes/", json={"title": "B", "content": "Second", "project_id": project_id})
    client.post("/notes/", json={"title": "Orphan", "content": "No project"})

    r = client.get(f"/projects/{project_id}/notes")
    assert r.status_code == 200, r.text
    notes = r.json()
    assert len(notes) == 2
    titles = {n["title"] for n in notes}
    assert titles == {"A", "B"}
