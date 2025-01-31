from fastapi import BackgroundTasks
from fastapi.websockets import WebSocket

from api.dependencies.duty import DutyServicesDep
from api.dependencies.room import DutiesRoomIdentifierDep


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_group_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


duty_connection_manager = ConnectionManager()

async def refresh_websocket_duties(
        background_tasks: BackgroundTasks,
        duty_services: DutyServicesDep,
        room: DutiesRoomIdentifierDep,
):
    duties_json = await duty_services.get_all_duties_with_users_in_the_room_json(room_id=room.id)
    background_tasks.add_task(duty_connection_manager.send_group_message, duties_json)