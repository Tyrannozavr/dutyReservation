import uuid

from fastapi import BackgroundTasks
from fastapi.websockets import WebSocket
from collections import defaultdict
from api.dependencies.duty import DutyServicesDep
from api.dependencies.room import DutiesRoomIdentifierDep

def default_factory_for_web_socket():
    return []

class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(default_factory_for_web_socket)

    async def connect(self, websocket: WebSocket, identifier: uuid):
        await websocket.accept()
        self.active_connections[identifier].append(websocket)

    def disconnect(self, websocket: WebSocket, identifier: uuid):
        self.active_connections[identifier].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_group_message(self, identifier: uuid, message: str):
        for connection in self.active_connections[identifier]:
            await connection.send_text(message)


duty_connection_manager = ConnectionManager()

async def refresh_websocket_duties_task(
        background_tasks: BackgroundTasks,
        duty_services: DutyServicesDep,
        room: DutiesRoomIdentifierDep,
):
    """Refreshes duties data in websocket"""
    duties_json = await duty_services.get_all_duties_with_users_in_the_room_json(room_id=room.id)
    background_tasks.add_task(duty_connection_manager.send_group_message, room.identifier, duties_json)


