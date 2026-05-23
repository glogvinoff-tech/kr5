from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from ..schemas import RoomUsersResponse

router = APIRouter()


class RoomManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    def connect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        room = self.rooms.setdefault(room_id, {})
        room[username] = websocket

    def disconnect(self, room_id: str, username: str, websocket: WebSocket) -> None:
        room = self.rooms.get(room_id, {})
        if username in room and room[username] is websocket:
            room.pop(username, None)
        if not room:
            self.rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, payload: dict) -> None:
        room = self.rooms.get(room_id, {})
        for ws in list(room.values()):
            try:
                await ws.send_json(payload)
            except RuntimeError:
                pass

    def get_users(self, room_id: str) -> List[str]:
        return list(self.rooms.get(room_id, {}).keys())


room_manager = RoomManager()


@router.get("/rooms/{room_id}/users", response_model=RoomUsersResponse)
def get_room_users(room_id: str) -> RoomUsersResponse:
    return RoomUsersResponse(room_id=room_id, users=room_manager.get_users(room_id))


@router.websocket("/ws/rooms/{room_id}")
async def websocket_room(room_id: str, websocket: WebSocket) -> None:
    username = websocket.query_params.get("username", "").strip()
    if not username:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    room_manager.connect(room_id, username, websocket)
    await room_manager.broadcast(room_id, {"type": "message", "text": f"{username} joined", "username": username})

    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                text = data.get("text", "")
                if not isinstance(text, str) or len(text) > 300:
                    await websocket.send_json({"type": "error", "detail": "Message is too long"})
                    continue
                await room_manager.broadcast(
                    room_id,
                    {"type": "message", "room_id": room_id, "username": username, "text": text},
                )
    except WebSocketDisconnect:
        room_manager.disconnect(room_id, username, websocket)
        await room_manager.broadcast(room_id, {"type": "message", "text": f"{username} left", "username": username})
