from fastapi.testclient import TestClient


def test_users_me_returns_current_user(client: TestClient) -> None:
    response = client.get("/users/me", headers={"X-User-Id": "10", "X-User-Role": "user"})
    assert response.status_code == 200
    assert response.json() == {"id": 10, "role": "user"}


def test_users_me_without_header_returns_401(client: TestClient) -> None:
    response = client.get("/users/me")
    assert response.status_code == 401


def test_user_cannot_access_admin_stats(client: TestClient) -> None:
    response = client.get("/admin/stats", headers={"X-User-Id": "10", "X-User-Role": "user"})
    assert response.status_code == 403


def test_admin_can_get_stats(client: TestClient) -> None:
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task1", "priority": 1, "status": "todo"},
    )
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task2", "priority": 2, "status": "done"},
    )
    response = client.get("/admin/stats", headers={"X-User-Id": "1", "X-User-Role": "admin"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_tasks"] == 2
    assert payload["by_status"]["todo"] == 1
    assert payload["by_status"]["done"] == 1


def test_user_cannot_delete_other_users_task_via_tasks(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task1", "priority": 1, "status": "todo"},
    ).json()

    response = client.delete(
        f"/tasks/{created['id']}", headers={"X-User-Id": "11"}
    )
    assert response.status_code == 404


def test_admin_can_delete_any_task(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task1", "priority": 1, "status": "todo"},
    ).json()

    response = client.delete(
        f"/admin/tasks/{created['id']}",
        headers={"X-User-Id": "1", "X-User-Role": "admin"},
    )
    assert response.status_code == 204


def test_openapi_tags_grouped_by_router(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi = response.json()
    tags = set()
    for path_item in openapi.get("paths", {}).values():
        for operation in path_item.values():
            for tag in operation.get("tags", []):
                tags.add(tag)
    assert "tasks" in tags
    assert "users" in tags
    assert "admin" in tags
