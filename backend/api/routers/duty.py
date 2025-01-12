import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path

from api.dependencies.auth import AuthorizedUserType
from api.dependencies.database import SessionDep
from api.errors.duty import UserHasNoPermission
from db.queries.duty import queries as duty_queries

router = APIRouter()


@router.get("/list/")
async def get_all_duties_in_month(month: int, db: SessionDep):
    duties_list = await duty_queries.get_all_duties_in_month(month_number=month, db=db)
    return duties_list

@router.post("/create/")
async def reserve_duty(
        user: AuthorizedUserType,
        db: SessionDep,
        date: Annotated[datetime.date, Body()]
):
    duty = await duty_queries.create_duty(request_user_id=user.id, date=date, db=db)
    return duty


@router.put("/update/{duty_id}")
async def change_duty(
        duty_id: Annotated[int, Path()],
        user: AuthorizedUserType,
        date: Annotated[datetime.date, Body()],
        db: SessionDep,
):
    duty = await duty_queries.get_duty_by_id(duty_id=duty_id, db=db)
    if duty.user_id != user.id:
        raise UserHasNoPermission
    duty = await duty_queries.change_duty(duty=duty, date=date, db=db)
    return duty

@router.delete("/delete/{duty_id}")
async def delete_duty(
        duty_id: Annotated[int, Path()],
        user: AuthorizedUserType,
        db: SessionDep,
):
    duty = await duty_queries.get_duty_by_id(duty_id=duty_id, db=db)
    if duty.user_id != user.id:
        raise UserHasNoPermission
    await duty_queries.delete_duty(duty=duty, db=db)
    return {"status": "success"}
