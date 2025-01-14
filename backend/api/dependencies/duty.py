from typing import Annotated

from api.dependencies.database import SessionDep
from db.queries.duty import DutyQueries

from fastapi import Depends, HTTPException, Path

from db.queries.room import RoomQueries
from models.sqlmodels.duty import DutiesRoom


async def get_room_by_identifier(room_identifier: Annotated[str, Path()], db: SessionDep) -> DutiesRoom:
    duty_queries = DutyQueries(db=db)
    room = await duty_queries.get_room_by_identifier(room_identifier)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


async def get_duty_queries(db: SessionDep) -> DutyQueries:
    return DutyQueries(db=db)

async def get_room_queries(db: SessionDep) -> RoomQueries:
    return RoomQueries(db=db)



DutiesRoomDp = Annotated[DutiesRoom, Depends()]
DutyIdDp = Annotated[int, Path()]
DutyQueriesDep = Annotated[DutyQueries, Depends(get_duty_queries)]
RoomQueriesDep = Annotated[RoomQueries, Depends(get_room_queries)]