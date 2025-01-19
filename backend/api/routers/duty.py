import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query

from api.dependencies.auth import AuthorizedUserType, TokenDataDep
from api.dependencies.database import SessionDep
from api.dependencies.duty import DutyIdDp, DutyServicesDep, DateDep
from api.dependencies.room import DutiesRoomIdentifierDep
from api.errors.duty import UserHasNoPermission
from db.repositories.duty import DutyRepositories
from models.pydantic.auth import UserRead
from models.pydantic.duty import DutiesWithUsersResponse, FreeDutiesResponse, FreeDuty, DutyWithUser, DutyTaken
from tests.services.integrational_tests.test_room import duty_services

router = APIRouter(prefix="/{room_identifier}")
router_without_room = APIRouter()

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
        date: DateDep,
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep,
):
    duty = await duty_services.set_duty_user_if_free(
        user_id=token_data.user_id,
        room_id=room.id,
        date=date
    )
    return duty

@router.put("/", response_model=DutyTaken)
async def reserve_or_change_duty(
        token_data: TokenDataDep,
        date: DateDep,
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep
):
    """Reserves a date if the user can set one extra duty or delete last duty and takes a new one with requested date"""
    duty = await duty_services.set_or_change_duty_user(user_id=token_data.user_id, room_id=room.id, date=date)
    return duty


@router_without_room.put("/{duty_id}", response_model=DutyTaken)
async def change_duty(
        duty_id: DutyIdDp,
        token_data: TokenDataDep,
        date: DateDep,
        duty_services: DutyServicesDep
):
    duty = await duty_services.change_duty_date(duty_id=duty_id, user_id=token_data.user_id, date=date)
    return duty


@router_without_room.delete("/{duty_id}")
async def delete_duty(
        duty_id: DutyIdDp,
        token_data: TokenDataDep,
        duty_services: DutyServicesDep,
):
    await duty_services.delete_duty_from_user(duty_id=duty_id, user_id=token_data.user_id)
    return {"status": "success"}
