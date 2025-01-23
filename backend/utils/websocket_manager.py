# backend/utils/websocket_manager.py
from fastapi import WebSocket
from typing import Dict, Set
import logging

class WebsocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.search_connections: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, connection_id: str):
        await websocket.accept()
        self.active_connections[connection_id] = websocket

    def disconnect(self, connection_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        for search_id in self.search_connections:
            if connection_id in self.search_connections[search_id]:
                self.search_connections[search_id].remove(connection_id)

    def register_search(self, search_id: str, connection_id: str):
        if search_id not in self.search_connections:
            self.search_connections[search_id] = set()
        self.search_connections[search_id].add(connection_id)

    async def broadcast_to_search(self, search_id: str, message: dict):
        if search_id in self.search_connections:
            for connection_id in self.search_connections[search_id]:
                await self.send_personal_message(message, connection_id)

    async def send_personal_message(self, message: dict, connection_id: str):
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_json(message)
            except Exception as e:
                logging.error(f"Error sending message to {connection_id}: {str(e)}")
                await self.disconnect(connection_id)
