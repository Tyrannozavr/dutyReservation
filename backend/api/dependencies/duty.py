from typing import Annotated

from api.dependencies.database import SessionDep
from db.repositories.duty import DutyRepositories

from fastapi import Depends, HTTPException, Path

from db.repositories.room import RoomRepositories
from models.sqlmodels.auth import DutiesRoom


async def get_room_by_identifier(room_identifier: Annotated[str, Path()], db: SessionDep) -> DutiesRoom:
    duty_queries = DutyRepositories(db=db)
    room = await duty_queries.get_room_by_identifier(room_identifier)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


async def get_duty_queries(db: SessionDep) -> DutyRepositories:
    return DutyRepositories(db=db)

async def get_room_queries(db: SessionDep) -> RoomRepositories:
    return RoomRepositories(db=db)



DutiesRoomDp = Annotated[DutiesRoom, Depends()]
DutyIdDp = Annotated[int, Path()]
DutyRepositoriesDep = Annotated[DutyRepositories, Depends(get_duty_queries)]
RoomRepositoriesDep = Annotated[RoomRepositories, Depends(get_room_queries)]