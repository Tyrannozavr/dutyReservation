from fastapi import APIRouter

from api.dependencies.auth import AuthorizedUserType, TokenDataDep
from api.dependencies.database import SessionDep
from api.dependencies.room import RoomServicesDep, RoomParamsDep, DutiesRoomUpdateParams, \
    DutiesRoomIdDp
from db.repositories.room import RoomRepositories
from models.pydantic.room import RoomRead
from models.sqlmodels.auth import Duty

router = APIRouter(tags=["room"])


@router.get("/")
async def get_rooms_by_user(
        user: AuthorizedUserType,
        db: SessionDep,
) -> list[Duty]:
    room_queries = RoomRepositories(db=db)
    room = await room_queries.get_all_user_rooms(user_id=user.id)
    return room


@router.post("/", response_model=RoomRead)
async def create_room(
        user: AuthorizedUserType,
        room_data: RoomParamsDep,
        room_services: RoomServicesDep
):
    room = await room_services.create_room(
        name=room_data.name,
        owner_id=user.id,
        duties_per_day=room_data.duties_per_day,
        year=room_data.date.year,
        month=room_data.date.month,
        is_multiple_selection=room_data.is_multiple_selection
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
