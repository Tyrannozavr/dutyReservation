import datetime
import uuid

from sqlmodel import Session, select

from api.errors.room import RoomNotFound
from db.repositories.duty import DutyRepositories
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

    async def create_room(self, owner_id: int, name: str = "", duties_per_day: int = 1,
                          is_multiple_selection: bool = False) -> DutiesRoom:
        room = DutiesRoom(owner_id=owner_id, duties_per_day=duties_per_day, name=name,
                          is_multiple_selection=is_multiple_selection)
        self.db.add(room)
        return room

    async def create_duties_for_room(self, room_id: int, month: int, year: int, duties_per_day: int):
        days_per_month = (datetime.date(year=year, month=month + 1, day=1) - datetime.timedelta(days=1)).day
        available_duties = [
            Duty(room_id=room_id, date=datetime.date(year=year, month=month, day=day))
            for _ in range(duties_per_day) for day in range(1, days_per_month + 1)
        ]

        self.db.add_all(available_duties)
        self.db.commit()
        return available_duties

    async def get_all_user_rooms(self, user_id):
        stmt = select(DutiesRoom).where(DutiesRoom.owner_id == user_id)
        rooms = self.db.exec(stmt).all()
        return rooms

    async def delete_room(self, room_id: int):
        stmt = select(DutiesRoom).where(DutiesRoom.id == room_id)
        room = self.db.exec(stmt).first()
        self.db.delete(room)
        return room


class RoomRepositories(RoomRepositoriesMixin):
    pass

# room_queries = Queries()
