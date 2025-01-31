from typing import Annotated

from fastapi import BackgroundTasks, Depends

from api.dependencies.duty import DutyServicesDep
from api.dependencies.room import DutiesRoomIdentifierDep
from services.Websockets import refresh_websocket_duties_task


async def get_refresh_duties_task(background_tasks: BackgroundTasks,
                                  duty_services: DutyServicesDep,
                                  room: DutiesRoomIdentifierDep):
    async def wrapped():
        return await refresh_websocket_duties_task(
            background_tasks=background_tasks,
            duty_services=duty_services,
            room=room
        )
    return wrapped


DutyRefreshWebSocketTask = Annotated[callable, Depends(get_refresh_duties_task)]