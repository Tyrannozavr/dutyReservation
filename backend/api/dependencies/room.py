import uuid
from typing import Annotated

from fastapi import Body, Path
from fastapi.params import Depends

from api.dependencies.database import SessionDep
from models.pydantic.room import RoomCreate, RoomUpdateSettings
from models.sqlmodels.auth import DutiesRoom
from services.room import RoomServices


def get_room_services(db: SessionDep) -> RoomServices:
    return RoomServices(db=db)


RoomServicesDep = Annotated[RoomServices, Depends(get_room_services)]
RoomParamsDep = Annotated[RoomCreate, Body()]


async def get_duties_room(room_identifier: Annotated[uuid.UUID, Path()], room_services: RoomServicesDep) -> DutiesRoom:
    return await room_services.get_room_by_identifier(identifier=room_identifier)


DutiesRoomIdentifierDp = Annotated[DutiesRoom, Depends(get_duties_room)]
DutiesRoomIdDp = Annotated[int, Path()]
DutiesRoomUpdateParams = Annotated[RoomUpdateSettings, Body()]
