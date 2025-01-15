import datetime
import uuid

from sqlmodel import Session, select

from models.sqlmodels.duty import DutiesRoom, Duty


class RoomQueriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def get_room_by_identifier(self, room_identifier: uuid.UUID):
        stmt = select(DutiesRoom).where(DutiesRoom.identifier == room_identifier)
        room = self.db.exec(stmt).first()
        return room

    async def create_room(self, owner_id: int, name: str = "", duties_per_day: int = 1):
        room = DutiesRoom(owner_id=owner_id, duties_per_day=duties_per_day, name=name)
        self.db.add(room)
        return room

    async def create_duties_for_room(self, room_id: int, month: int, year: int, duties_per_day: int):
        days_per_month = (datetime.date(year=year, month=month+1, day=1) - datetime.timedelta(days=1)).day
        available_duties = [
            Duty(user_id=None, room_id=room_id, date=datetime.date(year=year, month=month, day=day))
            for day in range(1, days_per_month + 1)
        ]
        available_duties = [duty for _ in range(duties_per_day) for duty in available_duties]
        self.db.add_all(available_duties)
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


class RoomQueries(RoomQueriesMixin):
    pass

# room_queries = Queries()