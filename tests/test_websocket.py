import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect


def test_websocket_connection_and_message_broadcast(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        join_event = websocket.receive_json()
        assert join_event["type"] == "message"

        with client.websocket_connect("/ws/rooms/python?username=bob") as websocket2:
            assert websocket.receive_json()["username"] == "bob"
            assert websocket2.receive_json()["username"] == "bob"

            message = {"type": "message", "text": "Всем привет"}
            websocket.send_json(message)

            received1 = websocket.receive_json()
            received2 = websocket2.receive_json()

            assert received1["type"] == "message"
            assert received2["type"] == "message"
            assert received1["text"] == "Всем привет"
            assert received2["text"] == "Всем привет"


def test_websocket_message_isolation_by_room(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket1:
        websocket1.receive_json()
        with client.websocket_connect("/ws/rooms/fastapi?username=bob") as websocket2:
            websocket2.receive_json()
            websocket1.send_json({"type": "message", "text": "Hello room"})
            received = websocket1.receive_json()
            assert received["text"] == "Hello room"
            try:
                other = websocket2.receive_json(timeout=0.1)
            except Exception:
                other = None
            assert other is None or other.get("text") != "Hello room"


def test_websocket_long_message_returns_error(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()
        long_text = "x" * 301
        websocket.send_json({"type": "message", "text": long_text})
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert response["detail"] == "Message is too long"


def test_websocket_disconnect_removes_user(client: TestClient) -> None:
    with client.websocket_connect("/ws/rooms/python?username=alice") as websocket:
        websocket.receive_json()
        response = client.get("/rooms/python/users")
        assert response.status_code == 200
        assert response.json()["users"] == ["alice"]
    response_after = client.get("/rooms/python/users")
    assert response_after.status_code == 200
    assert response_after.json()["users"] == []


def test_websocket_rejects_empty_username(client: TestClient) -> None:
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/rooms/python?username=   ") as websocket:
            pass
