from fastapi import APIRouter, Query, BackgroundTasks
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

from api.dependencies.auth import TokenDataDep, TokenDataQueryDep
from api.dependencies.duty import DutyIdDp, DutyServicesDep, DutyDataDep
from api.dependencies.room import DutiesRoomIdentifierDep
from api.dependencies.websockets import DutyRefreshWebSocketTask
from models.pydantic.auth import UserRead
from models.pydantic.duty import DutiesWithUsersResponse, FreeDutiesResponse, FreeDuty, DutyWithUser, DutyTaken, \
    DutyRead
from services.Websockets import duty_connection_manager
from tests.services.integrational_tests.test_room import duty_services

router = APIRouter(prefix="/{room_identifier}", tags=["customer"])
router_without_room = APIRouter(tags=["owner"])


@router.get("/duties", response_model=DutiesWithUsersResponse | FreeDutiesResponse)
async def get_all_duties_in_room(
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep,
        token_data: TokenDataDep,
        free: bool = Query(default=False, description="Set true to retrieve only free duties"),

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

@router.get("/ws/duties", response_model=list[DutyWithUser])
async def websocket_docs(
        websocket: WebSocket,
        duty_services: DutyServicesDep,
        room: DutiesRoomIdentifierDep,
        token_data: TokenDataQueryDep,
):
    return {
        "description": "WebSocket endpoint for duties.",
        "url": "/ws/duties",
        "usage": "Connect using a WebSocket client to send and receive messages."
    }
# https://fastapi.tiangolo.com/advanced/websockets/#using-depends-and-others
@router.websocket("/ws/duties")
async def websocket_endpoint(
        websocket: WebSocket,
        duty_services: DutyServicesDep,
        room: DutiesRoomIdentifierDep,
        token_data: TokenDataQueryDep,
):
    """
    WebSocket endpoint for duties.

    - **Accepts** messages from the client and echoes them back.
    - Connect using a WebSocket client to ws://<your-domain>/ws/duties.
    """
    await duty_connection_manager.connect(websocket=websocket)
    duties_json = await duty_services.get_all_duties_with_users_in_the_room_json(room_id=room.id)
    await duty_connection_manager.send_personal_message(websocket=websocket, message=duties_json)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await duty_connection_manager.disconnect(websocket)
    # await websocket.accept()
    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"Message text was: {data}")


@router.patch("/duties/{duty_id}", response_model=DutyTaken)
async def update_duty(
        token_data: TokenDataDep,
        duty_id: DutyIdDp,
        room: DutiesRoomIdentifierDep,
        duty_services: DutyServicesDep,
        background_tasks: BackgroundTasks
):
    """Sets duty user as user requested if duty is still free and user can reserve duty in this room"""
    duty = await duty_services.set_duty_user_by_duty_id(
        user_id=token_data.user_id,
        room_id=room.id,
        duty_id=duty_id
    )
    duties_json = await duty_services.get_all_duties_with_users_in_the_room_json(room_id=room.id)
    # background_tasks.add_task(duty_connection_manager.send_group_message, duties_json)
    await duty_connection_manager.send_group_message(duties_json)
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
