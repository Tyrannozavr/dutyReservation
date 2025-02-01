import asyncio

from fastapi import APIRouter, status, HTTPException

from api.dependencies.auth import TokenDataDep
from api.dependencies.room import RoomServicesDep, RoomParamsDep, DutiesRoomUpdateParams, \
    DutiesRoomIdDp, DutiesRoomIdentifierDep
from api.dependencies.websockets import DutyRefreshWebSocketTask
from api.errors.duty import UserHasNoPermission
from models.pydantic.room import RoomOwnerRead, RoomCommonRead
from fastapi import Response
router = APIRouter(tags=["room"])


@router.get("")
async def get_rooms_created_by_user(
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> list[RoomOwnerRead]:
    """Returns rooms created by user"""
    room = await room_services.get_user_rooms(user_id=token_data.user_id)
    return room

@router.post("", response_model=RoomOwnerRead, status_code=status.HTTP_201_CREATED)
async def create_room(
        token: TokenDataDep,
        room_data: RoomParamsDep,
        room_services: RoomServicesDep
):
    room = await room_services.create_room(
        owner_id=token.user_id,
        room_data=room_data
    )
    return room


@router.get("/storage/{room_identifier}", tags=["customer"])
async def get_room_by_identifier(
        room: DutiesRoomIdentifierDep,
        token_data: TokenDataDep
) -> RoomCommonRead | RoomOwnerRead:
    if room.owner_id == token_data.user_id:
        return RoomOwnerRead.model_validate(room.model_dump())
    else:
        return RoomCommonRead.model_validate(room.model_dump())


@router.post("/storage/{room_identifier}", tags=["customer"])
async def add_room_to_storage(
        room: DutiesRoomIdentifierDep,
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> RoomCommonRead | None:
    await room_services.store_room(user_id=token_data.user_id, room_id=room.id)
    return room

@router.delete(
    "/storage/{room_identifier}", tags=["customer"]
)
async def delete_room_from_storage(
        room: DutiesRoomIdentifierDep,
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
):
    response = await room_services.delete_room_from_storage(user_id=token_data.user_id, room_id=room.id)
    if response:
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

@router.get("/storage", tags=["customer"])
async def get_rooms_stored_by_user(
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> list[RoomOwnerRead]:
    """Returns rooms stored by user"""
    room = await room_services.get_stored_room_list(user_id=token_data.user_id)
    return room


@router.get("/{room_id}", tags=["owner"])
async def get_room_by_id(
        token_data: TokenDataDep,
        room_identifier: DutiesRoomIdentifierDep,
        room_services: RoomServicesDep
) -> RoomOwnerRead:
    room = await room_services.get_room_by_identifier(room_identifier=room_identifier)
    if room.owner_id == token_data.user_id:
        return room
    else:
        raise UserHasNoPermission


@router.delete("/{room_id}", tags=["owner"])
async def delete_room(
        token_data: TokenDataDep,
        room_id: DutiesRoomIdDp,
        room_services: RoomServicesDep,
        refresh_websocket_duties: DutyRefreshWebSocketTask.by_room_id
) -> dict[str, str]:
    await room_services.delete_room(user_id=token_data.user_id, room_id=room_id)
    await refresh_websocket_duties
    return {"status": "success"}


@router.patch("/{room_id}", tags=["owner"])
async def update_room(
        token_data: TokenDataDep,
        room_id: DutiesRoomIdDp,
        room_services: RoomServicesDep,
        room_data: DutiesRoomUpdateParams,
        refresh_websocket_duties: DutyRefreshWebSocketTask.by_room_id,
) -> RoomOwnerRead:
    updated_room = await room_services.update_room(
        user_id=token_data.user_id,
        update_data=room_data,
        room_id=room_id
    )
    await refresh_websocket_duties()
    return updated_room
