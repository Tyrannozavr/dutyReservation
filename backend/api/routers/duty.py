import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Path

from api.dependencies.auth import AuthorizedUserType
from api.dependencies.database import SessionDep
from api.dependencies.duty import DutiesRoomDp, DutyIdDp
from api.errors.duty import UserHasNoPermission
from db.repositories.duty import DutyRepositories

router = APIRouter(prefix="/{room_identifier}")


@router.get("/")
async def get_all_duties_in_room(room: DutiesRoomDp, db: SessionDep):
    duty_queries = DutyRepositories(db=db)
    duties_list = await duty_queries.get_all_duties_in_room(room_id=room.id, db=db)
    return duties_list


@router.post("/")
async def reserve_duty(
        user: AuthorizedUserType,
        db: SessionDep,
        date: Annotated[datetime.date, Body()],
        room: DutiesRoomDp
):
    duty_queries = DutyRepositories(db=db)
    duty = await duty_queries.create_duty(user_id=user.id, room_id=room.id, date=date)
    return duty


@router.put("/{duty_id}")
async def change_duty(
        duty_id: Annotated[int, Path()],
        user: AuthorizedUserType,
        date: Annotated[datetime.date, Body()],
        db: SessionDep,
):
    duty_queries = DutyRepositories(db=db)
    duty = await duty_queries.get_duty_by_id(duty_id=duty_id)
    if duty.user_id != user.id:
        raise UserHasNoPermission
    duty = await duty_queries.change_duty_date(duty=duty, date=date)
    return duty


@router.delete("/{duty_id}")
async def delete_duty(
        duty_id: DutyIdDp,
        user: AuthorizedUserType,
        db: SessionDep,
):
    duty_queries = DutyRepositories(db=db)
    duty = await duty_queries.get_duty_by_id(duty_id=duty_id, db=db)
    if duty.user_id != user.id:
        raise UserHasNoPermission
    await duty_queries.delete_duty(duty=duty, db=db)
    return {"status": "success"}
