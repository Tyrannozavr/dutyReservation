from typing import Annotated

from api.dependencies.database import SessionDep
from db.queries.duty import DutyQueries

from fastapi import Depends, HTTPException, Path

from models.sqlmodels.duty import DutiesRoom


async def get_room_by_identifier(room_identifier: Annotated[str, Path()], db: SessionDep) -> DutiesRoom:
    duty_queries = DutyQueries(db=db)
    room = await duty_queries.get_room_by_identifier(room_identifier)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room



DutiesRoomDp = Annotated[DutiesRoom, Depends()]
DutyIdDp = Annotated[int, Path()]