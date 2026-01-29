def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"

    r = client.delete(f"/action-items/{item['id']}")
    assert r.status_code == 204, r.text

    r = client.delete(f"/action-items/{item['id']}")
    assert r.status_code == 404


def test_action_items_sort_created_at_desc(client):
    ids = []
    for i in range(3):
        r = client.post("/action-items/", json={"description": f"Item {i} description here"})
        ids.append(r.json()["id"])
    r = client.get("/action-items/", params={"limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 3
    first_three_ids = [items[i]["id"] for i in range(3)]
    assert first_three_ids == sorted(ids, reverse=True)


def test_action_items_sort_invalid_field_returns_400(client):
    r = client.get("/action-items/", params={"sort": "invalid_field"})
    assert r.status_code == 400
    assert "invalid" in r.json().get("detail", "").lower() or "allowed" in r.json().get("detail", "").lower()
