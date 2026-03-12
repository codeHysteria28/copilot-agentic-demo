"""Tests for the /tasks endpoints."""

import pytest
import httpx


# -- POST /tasks --


async def test_create_task(client: httpx.AsyncClient) -> None:
    """Creating a task returns 201 with all expected fields."""
    response = await client.post(
        "/tasks", json={"title": "Buy milk", "description": "2% please"}
    )

    body = response.json()
    assert response.status_code == 201
    assert body["title"] == "Buy milk"
    assert body["description"] == "2% please"
    assert body["status"] == "todo"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


async def test_create_task_defaults(client: httpx.AsyncClient) -> None:
    """Omitting optional fields uses correct defaults."""
    response = await client.post("/tasks", json={"title": "Minimal"})

    body = response.json()
    assert response.status_code == 201
    assert body["description"] == ""
    assert body["status"] == "todo"


async def test_create_task_with_status(client: httpx.AsyncClient) -> None:
    """Creating a task with an explicit status works."""
    response = await client.post(
        "/tasks", json={"title": "Started", "status": "in_progress"}
    )

    assert response.status_code == 201
    assert response.json()["status"] == "in_progress"


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        ({"title": ""}, "empty title"),
        ({"description": "no title"}, "missing title"),
        ({"title": "Bad", "status": "invalid"}, "invalid status"),
    ],
    ids=["empty_title", "missing_title", "invalid_status"],
)
async def test_create_task_invalid_payload(
    client: httpx.AsyncClient,
    payload: dict[str, str],
    reason: str,
) -> None:
    """Invalid create payloads are rejected with 422."""
    response = await client.post("/tasks", json=payload)

    assert response.status_code == 422


# -- GET /tasks --


async def test_list_tasks_empty(client: httpx.AsyncClient) -> None:
    """Listing tasks when none exist returns an empty list."""
    response = await client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


async def test_list_tasks(client: httpx.AsyncClient) -> None:
    """Listing tasks returns all created tasks."""
    await client.post("/tasks", json={"title": "A"})
    await client.post("/tasks", json={"title": "B"})

    response = await client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_list_tasks_filter_by_status(
    client: httpx.AsyncClient,
) -> None:
    """Filtering by status returns only matching tasks."""
    await client.post("/tasks", json={"title": "Todo task", "status": "todo"})
    await client.post("/tasks", json={"title": "Done task", "status": "done"})
    await client.post(
        "/tasks", json={"title": "WIP task", "status": "in_progress"}
    )

    response = await client.get("/tasks", params={"status_filter": "done"})

    tasks = response.json()
    assert response.status_code == 200
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Done task"


# -- GET /tasks/{id} --


async def test_get_task(client: httpx.AsyncClient) -> None:
    """Getting a task by ID returns the correct task."""
    create_resp = await client.post("/tasks", json={"title": "Find me"})
    task_id: str = create_resp.json()["id"]

    response = await client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


# -- PATCH /tasks/{id} --


async def test_update_task_title(client: httpx.AsyncClient) -> None:
    """Patching a task's title updates only the title."""
    create_resp = await client.post("/tasks", json={"title": "Old"})
    task_id: str = create_resp.json()["id"]

    response = await client.patch(f"/tasks/{task_id}", json={"title": "New"})

    body = response.json()
    assert response.status_code == 200
    assert body["title"] == "New"
    assert body["status"] == "todo"


async def test_update_task_status(client: httpx.AsyncClient) -> None:
    """Patching a task's status works."""
    create_resp = await client.post("/tasks", json={"title": "Do it"})
    task_id: str = create_resp.json()["id"]

    response = await client.patch(
        f"/tasks/{task_id}", json={"status": "done"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "done"


async def test_update_task_updates_timestamp(
    client: httpx.AsyncClient,
) -> None:
    """Patching a task bumps updated_at."""
    create_resp = await client.post("/tasks", json={"title": "Timely"})
    original = create_resp.json()

    patch_resp = await client.patch(
        f"/tasks/{original['id']}", json={"description": "now with desc"}
    )

    assert patch_resp.json()["updated_at"] >= original["updated_at"]


# -- DELETE /tasks/{id} --


async def test_delete_task(client: httpx.AsyncClient) -> None:
    """Deleting a task returns 204 and removes it."""
    create_resp = await client.post("/tasks", json={"title": "Delete me"})
    task_id: str = create_resp.json()["id"]

    del_resp = await client.delete(f"/tasks/{task_id}")

    assert del_resp.status_code == 204
    get_resp = await client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


# -- 404 for missing resources --


@pytest.mark.parametrize(
    ("method", "url", "json_body"),
    [
        ("GET", "/tasks/nonexistent", None),
        ("PATCH", "/tasks/nonexistent", {"title": "Nope"}),
        ("DELETE", "/tasks/nonexistent", None),
    ],
    ids=["get", "patch", "delete"],
)
async def test_nonexistent_task_returns_404(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    json_body: dict[str, str] | None,
) -> None:
    """Operations on a nonexistent task return 404."""
    response = await client.request(method, url, json=json_body)

    assert response.status_code == 404
    assert "detail" in response.json()
