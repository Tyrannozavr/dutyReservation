import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Body

from api.dependencies.auth import AuthorizedUserType
from api.dependencies.database import SessionDep
from db.queries.duty import add_duty

router = APIRouter()


@router.post("/add")
def preserve_duty(
        user: AuthorizedUserType,
        db: SessionDep,
        date: Annotated[datetime.date, Body()]
):
    duty = add_duty(user_id=user.id, date=date, db=db)
    return duty
