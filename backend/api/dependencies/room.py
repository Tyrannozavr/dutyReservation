import uuid
from typing import Annotated

from fastapi import Body, Path
from fastapi.params import Depends

from api.dependencies.database import SessionDep
from api.errors.room import RoomNotFound
from models.pydantic.room import RoomCreate, RoomUpdateSettings
from models.sqlmodels.auth import DutiesRoom
from services.room import RoomServices


def get_room_services(db: SessionDep) -> RoomServices:
    return RoomServices(db=db)


RoomServicesDep = Annotated[RoomServices, Depends(get_room_services)]
RoomParamsDep = Annotated[RoomCreate, Body()]


async def get_room_by_identifier(room_identifier: Annotated[uuid.UUID, Path()], room_services: RoomServicesDep) -> DutiesRoom:
    room = await room_services.get_room_by_identifier(identifier=room_identifier)
    if not room:
        raise RoomNotFound
    return room


DutiesRoomIdentifierDep = Annotated[DutiesRoom, Depends(get_room_by_identifier)]
DutiesRoomIdDp = Annotated[int, Path()]
DutiesRoomUpdateParams = Annotated[RoomUpdateSettings, Body()]



