from tests.conftest import register_and_token


async def test_register_and_login(client):
    created = await client.post("/api/v1/auth/register", json={"email":"ada@example.com","password":"safe-password","full_name":"Ada Lovelace"})
    assert created.status_code == 201
    login = await client.post("/api/v1/auth/login", json={"email":"ada@example.com","password":"safe-password"})
    assert login.status_code == 200 and login.json()["access_token"]


async def test_project_crud_and_owner_permission(client):
    owner = await register_and_token(client)
    created = await client.post("/api/v1/projects", headers=owner, json={"name":"Platform","description":"Core work"})
    assert created.status_code == 201
    project_id = created.json()["id"]
    assert (await client.patch(f"/api/v1/projects/{project_id}", headers=owner, json={"name":"Platform v2"})).json()["name"] == "Platform v2"
    outsider = await register_and_token(client, "other@example.com", "Other")
    assert (await client.delete(f"/api/v1/projects/{project_id}", headers=outsider)).status_code == 403
    assert (await client.delete(f"/api/v1/projects/{project_id}", headers=owner)).status_code == 204


async def test_ticket_crud_filters_and_history(client):
    headers = await register_and_token(client)
    project = await client.post("/api/v1/projects", headers=headers, json={"name":"Roadmap"})
    project_id = project.json()["id"]
    ticket = await client.post(f"/api/v1/projects/{project_id}/tickets", headers=headers, json={"title":"Build API","priority":"high"})
    assert ticket.status_code == 201
    ticket_id = ticket.json()["id"]
    updated = await client.patch(f"/api/v1/tickets/{ticket_id}", headers=headers, json={"status":"in_progress","priority":"urgent"})
    assert updated.json()["status"] == "in_progress"
    history = await client.get(f"/api/v1/tickets/{ticket_id}/history", headers=headers)
    assert {record["field_changed"] for record in history.json()} == {"status", "priority"}
    filtered = await client.get(f"/api/v1/projects/{project_id}/tickets?status=in_progress", headers=headers)
    assert len(filtered.json()) == 1
    assert (await client.delete(f"/api/v1/tickets/{ticket_id}", headers=headers)).status_code == 204


async def test_protected_endpoint_requires_token(client):
    assert (await client.get("/api/v1/projects")).status_code == 401
