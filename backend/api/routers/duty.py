import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query

from api.dependencies.auth import AuthorizedUserType, TokenDataDep
from api.dependencies.database import SessionDep
from api.dependencies.duty import DutyIdDp, DutyServicesDep
from api.dependencies.room import DutiesRoomIdentifierDep
from api.errors.duty import UserHasNoPermission
from db.repositories.duty import DutyRepositories
from models.pydantic.auth import UserRead
from models.pydantic.duty import DutiesWithUsersResponse, FreeDutiesResponse, FreeDuty, DutyWithUser, DutyTaken
from tests.services.integrational_tests.test_room import duty_services

router = APIRouter(prefix="/{room_identifier}")


@router.get("/", response_model=DutiesWithUsersResponse | FreeDutiesResponse)
async def get_all_duties_in_room(
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep,
        free: bool = Query(default=False, description="Set true to retrieve only free duties")
):
    if free:
        free_duties = await duty_services.get_all_free_duties_in_the_room(room_id=room.id)
        return FreeDutiesResponse(duties=[FreeDuty(**duty.model_dump()) for duty in free_duties])
    else:
        duties = await duty_services.get_all_duties_with_users_in_the_room(room_id=room.id)
        return DutiesWithUsersResponse(
            duties=[
                DutyWithUser(
                    **duty.model_dump(),
                    user=UserRead(**duty.user.model_dump())
                ) if duty.user else DutyWithUser(**duty.model_dump())
                for duty in duties
            ]
        )


@router.post("/", response_model=DutyTaken)
async def reserve_duty(
        token_data: TokenDataDep,
        date: Annotated[datetime.date, Body()],
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep,
):
    duty = await duty_services.set_duty_user(
        user_id=token_data.user_id,
        room_id=room.id,
        date=date
    )
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
