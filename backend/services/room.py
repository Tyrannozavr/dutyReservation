import uuid
from typing import Any

from sqlmodel import Session

from api.errors.duty import UserHasNoPermission
from api.errors.room import RoomNotFound
from db.repositories.room import RoomRepositories
from models.pydantic.room import RoomUpdateSettings, RoomCreate
from models.sqlmodels.auth import DutiesRoom


class RoomServices:
    def __init__(self, db: Session, repositories: Any = None):
        """first of all I've added queries for testing (mock queries instance)"""
        self.repositories = RoomRepositories(db=db) if not repositories else repositories
        self.db = db


    async def get_user_rooms(self, user_id):
        return await self.repositories.get_all_users_rooms(user_id=user_id)

    async def create_room(self, room_data: RoomCreate, owner_id: int):
        room = await self.repositories.create_room(
            name=room_data.name,
            owner_id=owner_id,
            duties_per_day=room_data.duties_per_day,
            is_multiple_selection=room_data.is_multiple_selection,
            year=room_data.date.year,
            month=room_data.date.month
        )
        self.db.commit()
        await self.repositories.create_duties_for_room(
            room_id=room.id,
            year=room_data.date.year,
            month=room_data.date.month,
            duties_per_day=room_data.duties_per_day,
        )
        self.db.commit()
        self.db.refresh(room)
        return room

    async def get_room_by_identifier(self, identifier: uuid.UUID):
        room = await self.repositories.get_room_by_identifier(room_identifier=identifier)
        if not room:
            raise RoomNotFound
        return room

    async def get_room_by_id(self, room_id: int) -> DutiesRoom:
        return await self.repositories.get_room_by_id(room_id=room_id)

    async def validate_is_user_owner(self, room_id: int, user_id):
        room = await self.repositories.get_room_by_id(room_id=room_id)
        if not room:
            raise RoomNotFound
        if room.owner_id != user_id:
            raise UserHasNoPermission

    async def delete_room(self, user_id, room_id):
        await self.validate_is_user_owner(room_id=room_id, user_id=user_id)
        await self.repositories.delete_room(room_id=room_id)
        self.db.commit()

    async def update_room(self, user_id, room_id: int, update_data: RoomUpdateSettings) -> DutiesRoom:
        await self.validate_is_user_owner(user_id=user_id, room_id=room_id)
        room = await self.get_room_by_id(room_id=room_id)
        room = room.sqlmodel_update(update_data)
        await self.repositories.delete_duties_per_room(room_id=room_id)
        await self.repositories.create_duties_for_room(
            room_id=room.id,
            year=room.year,
            month=room.month,
            duties_per_day=update_data.duties_per_day,
        )
        self.db.add(room)
        try:
            self.db.commit()
            self.db.refresh(room)
            return room
        except Exception as e:
            print("Exc", e)
            raise e