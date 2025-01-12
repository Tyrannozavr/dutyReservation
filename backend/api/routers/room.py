import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Path
from pydantic import BaseModel

from api.dependencies.auth import AuthorizedUserType
from api.dependencies.database import SessionDep
from api.dependencies.duty import DutiesRoomDp
from api.errors.duty import UserHasNoPermission
from db.queries.duty import duty_queries
from db.queries.room import room_queries
from models.sqlmodels.duty import Duty

router = APIRouter(tags=["room"])

class DateParam(BaseModel):
    month: int
    year: int

@router.get("/")
async def get_rooms_by_user(
    user: AuthorizedUserType,
    db: SessionDep,
) -> list[Duty]:
    room = await room_queries.get_all_user_rooms(user_id=user.id, db=db)
    return room

@router.post("/")
async def create_room(
    user: AuthorizedUserType,
    db: SessionDep,
    room: Annotated[Duty, Body()],
    date: DateParam
) -> Duty:
    room = await room_queries.create_room(room=room, db=db, owner_id=user.id, month=date.month, year=date.year)
    return room


@router.delete("/{room_identifier}")
async def delete_room(
    user: AuthorizedUserType,
    db: SessionDep,
    room: DutiesRoomDp,
) -> dict[str, str]:
    if room.owner_id != user.id:
        raise UserHasNoPermission
    await room_queries.delete_room(room_id=room.id, db=db)
    return {"status": "success"}














