import datetime
import uuid
from typing import Any

from sqlmodel import Session

from api.errors.duty import UserHasNoPermission
from api.errors.room import RoomNotFound
from db.repositories.room import RoomRepositories
from logger import logger
from models.pydantic.room import RoomUpdateSettings, RoomCreate
from models.sqlmodels import DutiesRoom, RoomStorage


class RoomServices:
    def __init__(self, db: Session, repositories: Any = None):
        """first of all I've added queries for testing (mock queries instance)"""
        self.room_repositories = RoomRepositories(db=db) if not repositories else repositories
        self.db = db

    async def store_room(self, user_id: int, room_id: int) -> RoomStorage | None:
        storage = await self.room_repositories.store_room_to_user(user_id=user_id, room_id=room_id)
        self.db.commit()
        return storage

    async def delete_room_from_storage(self, user_id: int, room_id: int) -> str | None:
        await self.room_repositories.delete_room_from_storage(room_id=room_id, user_id=user_id)
        try:
            self.db.commit()
            return "ok"
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error with removing room: {e}")
            return None

    async def get_stored_room_list(self, user_id: int) -> list[DutiesRoom]:
        return await self.room_repositories.get_stored_room_list(user_id=user_id)

    async def get_user_rooms(self, user_id):
        return await self.room_repositories.get_all_users_rooms(user_id=user_id)

    async def create_room(self, room_data: RoomCreate, owner_id: int):
        room = await self.room_repositories.create_room(
            name=room_data.name,
            owner_id=owner_id,
            is_multiple_selection=room_data.is_multiple_selection,
        )
        self.db.commit()
        if room_data.duty_list:
            await self.room_repositories.create_duties_for_room(
                room_id=room.id,
                duty_list=room_data.duty_list
            )
        self.db.commit()
        self.db.refresh(room)
        return room

    async def get_room_by_identifier(self, identifier: uuid.UUID):
        room = await self.room_repositories.get_room_by_identifier(room_identifier=identifier)
        if not room:
            raise RoomNotFound
        return room

    async def get_room_by_id(self, room_id: int) -> DutiesRoom:
        return await self.room_repositories.get_room_by_id(room_id=room_id)

    async def validate_is_user_owner(self, room_id: int, user_id):
        room = await self.room_repositories.get_room_by_id(room_id=room_id)
        if not room:
            raise RoomNotFound
        if room.owner_id != user_id:
            raise UserHasNoPermission

    async def delete_room(self, user_id, room_id):
        await self.validate_is_user_owner(room_id=room_id, user_id=user_id)
        await self.room_repositories.delete_room(room_id=room_id)
        self.db.commit()

    async def update_room(self, user_id, room_id: int, update_data: RoomUpdateSettings) -> DutiesRoom:
        await self.validate_is_user_owner(user_id=user_id, room_id=room_id)
        room = await self.get_room_by_id(room_id=room_id)
        if update_data.name:
            room.name = update_data.name
        if update_data.is_multiple_selection:
            room.is_multiple_selection = update_data.is_multiple_selection
        if update_data.extra_duties:
            await self.room_repositories.create_duties_for_room(
            room_id=room.id,
            duty_list=update_data.extra_duties
        )
        self.db.add(room)
        try:
            self.db.commit()
            self.db.refresh(room)
            return room
        except Exception as e:
            logger.error("Exception in update room while try to commit ", e)
            raise e
