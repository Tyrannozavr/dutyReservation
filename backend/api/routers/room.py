import asyncio

from fastapi import APIRouter, status, HTTPException

from api.dependencies.auth import TokenDataDep
from api.dependencies.room import RoomServicesDep, RoomParamsDep, DutiesRoomUpdateParams, \
    DutiesRoomIdDp, DutiesRoomIdentifierDep
from models.pydantic.room import RoomRead, RoomCommonRead
from fastapi import Response
router = APIRouter(tags=["room"])


@router.get("")
async def get_rooms_created_by_user(
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> list[RoomRead]:
    """Returns rooms created by user"""
    room = await room_services.get_user_rooms(user_id=token_data.user_id)
    return room

@router.post("", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
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


@router.get("/storage/{room_identifier}")
async def get_room(
        room: DutiesRoomIdentifierDep,
) -> RoomCommonRead | None:
    # await asyncio.sleep(5)  #it is for testing frontend
    return room

@router.post("/storage/{room_identifier}")
async def add_room_to_storage(
        room: DutiesRoomIdentifierDep,
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> RoomCommonRead | None:
    await room_services.store_room(user_id=token_data.user_id, room_id=room.id)
    return room

@router.delete(
    "/storage/{room_identifier}",
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

@router.get("/storage")
async def get_rooms_stored_by_user(
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> list[RoomRead]:
    """Returns rooms stored by user"""
    room = await room_services.get_stored_room_list(user_id=token_data.user_id)
    return room


@router.delete("/{room_id}")
async def delete_room(
        token_data: TokenDataDep,
        room_id: DutiesRoomIdDp,
        room_services: RoomServicesDep
) -> dict[str, str]:
    await room_services.delete_room(user_id=token_data.user_id, room_id=room_id)
    return {"status": "success"}


@router.patch("/{room_id}")
async def update_room(
        token_data: TokenDataDep,
        room_id: DutiesRoomIdDp,
        room_services: RoomServicesDep,
        room_data: DutiesRoomUpdateParams,
) -> RoomRead:
    updated_room = await room_services.update_room(
        user_id=token_data.user_id,
        update_data=room_data,
        room_id=room_id
    )
    return updated_room
