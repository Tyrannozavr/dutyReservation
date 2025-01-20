import datetime
from typing import Annotated

from fastapi import Depends, Path, Body

from api.dependencies.database import SessionDep
from db.repositories.duty import DutyRepositories
from db.repositories.room import RoomRepositories
from models.pydantic.duty import DutyData, DutyReserve
from services.duty import DutyServices


async def get_duty_queries(db: SessionDep) -> DutyRepositories:
    return DutyRepositories(db=db)


async def get_room_queries(db: SessionDep) -> RoomRepositories:
    return RoomRepositories(db=db)

async def get_duty_services(db: SessionDep) -> DutyServices:
    return DutyServices(db=db)

DutyIdDp = Annotated[int, Path()]
DutyIdBodyDp = Annotated[DutyReserve, Body()]
DutyRepositoriesDep = Annotated[DutyRepositories, Depends(get_duty_queries)]
RoomRepositoriesDep = Annotated[RoomRepositories, Depends(get_room_queries)]
DutyServicesDep = Annotated[DutyServices, Depends(get_duty_services)]
DutyDataDep = Annotated[DutyData, Body()]
DutyIdDep = Annotated[int, Body()]