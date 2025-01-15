from typing import Any

from sqlmodel import Session

from db.queries.duty import DutyQueries
from db.queries.room import RoomQueries


class RoomServices:
    def __init__(self, db: Session, queries: Any = None):
        """first of all I've added queries for testing (mock queries instance)"""
        self.queries = RoomQueries(db=db) if not queries else queries
        self.db = db

    async def create_room(self, name: str, owner_id: int, year: int, month: int,
                          duties_per_day: int = 1):
        room = await self.queries.create_room(
            name=name,
            owner_id=owner_id,
            duties_per_day=duties_per_day
        )
        self.db.commit()
        await self.queries.create_duties_for_room(
            room_id=room.id,
            year=year,
            month=month,
            duties_per_day=duties_per_day
        )
        self.db.commit()
        self.db.refresh(room)
        return room
