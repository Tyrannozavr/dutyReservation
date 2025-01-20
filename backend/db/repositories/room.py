import datetime
import uuid

from sqlalchemy import delete
from sqlmodel import Session, select

from models.sqlmodels.auth import DutiesRoom, Duty


class RoomRepositoriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def get_rooms(self):
        stmt = select(DutiesRoom)
        rooms = self.db.exec(stmt)
        return rooms.all()

    async def get_user_rooms(self, user_id: int):
        stmt = select(DutiesRoom).where(DutiesRoom.user_id == user_id)
        rooms = self.db.exec(stmt)
        return rooms.all()

    async def get_room_by_identifier(self, room_identifier: uuid.UUID):
        stmt = select(DutiesRoom).where(DutiesRoom.identifier == room_identifier)
        room = self.db.exec(stmt).first()
        return room

    async def get_room_by_id(self, room_id: int) -> DutiesRoom:
        stmt = select(DutiesRoom).where(DutiesRoom.id == room_id)
        room = self.db.exec(stmt).first()
        return room

    async def create_room(self, owner_id: int, name: str = "",
                          is_multiple_selection: bool = False) -> DutiesRoom:
        room = DutiesRoom(owner_id=owner_id, name=name,
                          is_multiple_selection=is_multiple_selection
                          )
        self.db.add(room)
        return room

    async def create_duties_for_room(self, room_id: int, dates: list[datetime.date]):
        available_duties = [
            Duty(room_id=room_id, date=duty_date)
            for duty_date in dates
        ]

        self.db.add_all(available_duties)
        return available_duties

    async def delete_duties_per_room(self, room_id: int):
        stmt = delete(Duty).where(Duty.room_id == room_id)
        self.db.exec(stmt)

    async def get_all_users_rooms(self, user_id):
        stmt = select(DutiesRoom).where(DutiesRoom.owner_id == user_id)
        rooms = self.db.exec(stmt)
        return rooms.all()

    async def delete_room(self, room_id: int):
        stmt = select(DutiesRoom).where(DutiesRoom.id == room_id)
        room = self.db.exec(stmt).first()
        self.db.delete(room)
        return room

    async def get_duties_per_room(self, room_id: int) -> list[Duty]:
        stmt = select(Duty).where(Duty.room_id == room_id)
        rooms = self.db.exec(stmt)
        return rooms.all()


class RoomRepositories(RoomRepositoriesMixin):
    pass

# room_queries = Queries()
