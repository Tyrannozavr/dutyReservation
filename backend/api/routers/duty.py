from fastapi import APIRouter, Query

from api.dependencies.auth import TokenDataDep
from api.dependencies.duty import DutyIdDp, DutyServicesDep, DutyDataDep
from api.dependencies.room import DutiesRoomIdentifierDep
from models.pydantic.auth import UserRead
from models.pydantic.duty import DutiesWithUsersResponse, FreeDutiesResponse, FreeDuty, DutyWithUser, DutyTaken, \
    DutyRead
from tests.services.integrational_tests.test_room import duty_services
from fastapi import APIRouter, Query

from api.dependencies.auth import TokenDataDep
from api.dependencies.duty import DutyIdDp, DutyServicesDep, DutyDataDep
from api.dependencies.room import DutiesRoomIdentifierDep
from models.pydantic.auth import UserRead
from models.pydantic.duty import DutiesWithUsersResponse, FreeDutiesResponse, FreeDuty, DutyWithUser, DutyTaken, \
    DutyRead
from tests.services.integrational_tests.test_room import duty_services

router = APIRouter(prefix="/{room_identifier}")
router_without_room = APIRouter()


@router.get("/duties", response_model=DutiesWithUsersResponse | FreeDutiesResponse)
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


@router.patch("/duties/{duty_id}", response_model=DutyTaken)
async def update_duty(
        token_data: TokenDataDep,
        duty_id: DutyIdDp,
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep,
):
    """Sets duty user as user requested if duty is still free and user can reserve duty in this room"""
    duty = await duty_services.set_duty_user_by_duty_id(
        user_id=token_data.user_id,
        room_id=room.id,
        duty_id=duty_id
    )
    return duty

@router.delete("/duties/{duty_id}")
async def set_duty_as_free(
        duty_id: DutyIdDp,
        token_data: TokenDataDep,
        duty_services: DutyServicesDep,
        room: DutiesRoomIdentifierDep
):
    await duty_services.delete_duty_from_user(duty_id=duty_id, user_id=token_data.user_id)
    return {"status": "success"}

@router_without_room.put("/{duty_id}", response_model=DutyRead | None)
async def update_duty(
        duty_id: DutyIdDp,
        token_data: TokenDataDep,
        duty_data: DutyDataDep,
        duty_services: DutyServicesDep
):
    """Updates duty if user is a creator of the room"""
    return await duty_services.update_duty(update_data=duty_data, duty_id=duty_id, user_id=token_data.user_id)


@router_without_room.delete("/{duty_id}")
async def delete_duty(
        duty_id: DutyIdDp,
        token_data: TokenDataDep,
        duty_services: DutyServicesDep,
):
    response = await duty_services.delete_duty(duty_id=duty_id, user_id=token_data.user_id)
    if response:
        return {"status": "success"}
