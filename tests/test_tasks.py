from fastapi.testclient import TestClient


def test_create_task_success(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={
            "title": "Подготовить тесты",
            "description": "Написать интеграционные тесты для основных сценариев",
            "status": "todo",
            "priority": 4,
        },
    )
    assert response.status_code == 201
    assert response.json()["owner_id"] == 10
    assert response.json()["title"] == "Подготовить тесты"


def test_create_task_validation_error(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Hi", "priority": 3},
    )
    assert response.status_code == 422


def test_missing_user_id_returns_401(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Новая задача", "priority": 3, "status": "todo"},
    )
    assert response.status_code == 401


def test_user_sees_only_own_tasks(client: TestClient) -> None:
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Задача 1", "priority": 2, "status": "todo"},
    )
    client.post(
        "/tasks",
        headers={"X-User-Id": "11"},
        json={"title": "Задача 2", "priority": 4, "status": "todo"},
    )

    response = client.get("/tasks", headers={"X-User-Id": "10"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["owner_id"] == 10


def test_filter_tasks_by_status_and_priority(client: TestClient) -> None:
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "A", "priority": 1, "status": "todo"},
    )
    client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Bigger task", "priority": 5, "status": "in_progress"},
    )

    response = client.get(
        "/tasks?status=in_progress&min_priority=4",
        headers={"X-User-Id": "10"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "in_progress"


def test_update_task_status_success(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task", "priority": 3, "status": "todo"},
    ).json()

    response = client.patch(
        f"/tasks/{created['id']}/status",
        headers={"X-User-Id": "10"},
        json={"status": "done"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_get_other_user_task_returns_404(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task", "priority": 3, "status": "todo"},
    ).json()

    response = client.get(
        f"/tasks/{created['id']}",
        headers={"X-User-Id": "11"},
    )
    assert response.status_code == 404


def test_delete_task_success(client: TestClient) -> None:
    created = client.post(
        "/tasks",
        headers={"X-User-Id": "10"},
        json={"title": "Task", "priority": 3, "status": "todo"},
    ).json()

    response = client.delete(
        f"/tasks/{created['id']}", headers={"X-User-Id": "10"}
    )
    assert response.status_code == 204
