from typing import Annotated, Callable, TypeVar, Coroutine, Any

from fastapi import BackgroundTasks, Depends

from api.dependencies.duty import DutyServicesDep, DutyIdDp
from api.dependencies.room import DutiesRoomIdentifierDep, DutiesRoomIdDp, RoomServicesDep
from services.Websockets import refresh_websocket_duties_task


async def get_refresh_duties_task_by_room_identifier(background_tasks: BackgroundTasks,
                                                     duty_services: DutyServicesDep,
                                                     room: DutiesRoomIdentifierDep) -> Callable[
    [], Coroutine[Any, Any, Any]]:
    """Allows to use refresh websocket duties task directly in parameter of a function with automatically
    put dependencies"""

    async def wrapped():
        return await refresh_websocket_duties_task(
            background_tasks=background_tasks,
            duty_services=duty_services,
            room=room
        )

    return wrapped


async def get_refresh_duties_task_by_room_id(background_tasks: BackgroundTasks,
                                             duty_services: DutyServicesDep,
                                             room_services: RoomServicesDep,
                                             room_id: DutiesRoomIdDp) -> Callable[[], Coroutine[Any, Any, Any]]:
    """Allows to use refresh websocket duties task directly in parameter of a function with automatically
    put dependencies"""
    room = await room_services.get_room_by_id(room_id=room_id)

    async def wrapped():
        return await refresh_websocket_duties_task(
            background_tasks=background_tasks,
            duty_services=duty_services,
            room=room
        )

    return wrapped


async def get_refresh_duties_task_by_duty_id(background_tasks: BackgroundTasks,
                                             duty_services: DutyServicesDep,
                                             room_services: RoomServicesDep,
                                             duty_id: DutyIdDp) -> Callable[[], Coroutine[Any, Any, Any]]:
    """Allows to use refresh websocket duties task directly in parameter of a function with automatically
    put dependencies"""
    duty = await duty_services.get_duty(duty_id=duty_id)
    room = await room_services.get_room_by_id(room_id=duty.room_id)

    async def wrapped():
        return await refresh_websocket_duties_task(
            background_tasks=background_tasks,
            duty_services=duty_services,
            room=room
        )
    return wrapped


class DutyRefreshWebSocketTask:
    by_room_identifier: Annotated[Callable, Depends(get_refresh_duties_task_by_room_identifier)] =\
        Annotated[Callable, Depends(get_refresh_duties_task_by_room_identifier)]
    by_room_id: Annotated[Callable, Depends(get_refresh_duties_task_by_room_id)] =\
        Annotated[Callable, Depends(get_refresh_duties_task_by_room_id)]
    by_duty_id:  Annotated[Callable, Depends(get_refresh_duties_task_by_duty_id)] =\
        Annotated[Callable, Depends(get_refresh_duties_task_by_duty_id)]
