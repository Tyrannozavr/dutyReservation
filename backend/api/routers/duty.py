import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Body, Path

from api.dependencies.auth import AuthorizedUserType
from api.dependencies.database import SessionDep
from db.queries.duty import queries as DutyQueries

router = APIRouter()


@router.post("/create_duty/")
async def reserve_duty(
        user: AuthorizedUserType,
        db: SessionDep,
        date: Annotated[datetime.date, Body()]
):
    duty = await DutyQueries.create_duty(request_user_id=user.id, date=date, db=db)
    return duty


@router.put("/update_duty/{duty_id}")
async def change_duty(
        duty_id: Annotated[int, Path()],
        user: AuthorizedUserType,
        date: Annotated[datetime.date, Body()],
        db: SessionDep,

):
    duty = await DutyQueries.change_duty(request_user_id=user.id, duty_id=duty_id, date=date, db=db)
    return duty
