from typing import List
from fastapi import WebSocket

class BroadcastSender:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    @staticmethod
    async def send_to_one_only(websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        try:
            self.connections.remove(websocket)
        except ValueError as e:
            print(f"Starlette error handle: {e}")

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections