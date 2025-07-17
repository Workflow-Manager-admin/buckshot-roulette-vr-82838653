from fastapi import WebSocket, WebSocketDisconnect
from fastapi import FastAPI
from typing import Dict, List, Any

class ConnectionManager:
    """Manages WebSocket connections for game events and chat."""
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    # PUBLIC_INTERFACE
    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)

    # PUBLIC_INTERFACE
    def disconnect(self, websocket: WebSocket, channel: str):
        self.active_connections[channel].remove(websocket)

    # PUBLIC_INTERFACE
    async def broadcast(self, channel: str, message: Any):
        if channel in self.active_connections:
            for ws in self.active_connections[channel]:
                await ws.send_json(message)

manager = ConnectionManager()

# PUBLIC_INTERFACE
def register_ws_routes(app: FastAPI):
    """Register WebSocket routes for game and chat events."""

    @app.websocket("/ws/game")
    async def ws_game_endpoint(websocket: WebSocket):
        """WebSocket for real-time lobby and game state sync."""
        channel = "game"
        await manager.connect(websocket, channel)
        try:
            while True:
                data = await websocket.receive_json()
                # Here: parse and forward game state or action
                await manager.broadcast(channel, {"from": "server", "event": data})
        except WebSocketDisconnect:
            manager.disconnect(websocket, channel)

    @app.websocket("/ws/chat")
    async def ws_chat_endpoint(websocket: WebSocket):
        """WebSocket for in-game or lobby chat."""
        channel = "chat"
        await manager.connect(websocket, channel)
        try:
            while True:
                msg = await websocket.receive_json()
                await manager.broadcast(channel, {"from": "server", "message": msg})
        except WebSocketDisconnect:
            manager.disconnect(websocket, channel)
