from fastapi import APIRouter, status

from api.dependencies.auth import TokenDataDep
from api.dependencies.room import RoomServicesDep, RoomParamsDep, DutiesRoomUpdateParams, \
    DutiesRoomIdDp
from models.pydantic.room import RoomRead

router = APIRouter(tags=["room"])


@router.get("/")
async def get_rooms_by_user(
        token_data: TokenDataDep,
        room_services: RoomServicesDep,
) -> list[RoomRead]:
    room = await room_services.get_user_rooms(user_id=token_data.user_id)
    return room


@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
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
