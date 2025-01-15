from sqlmodel import Session

from api.dependencies.database import SessionDep
from db.queries.room import RoomQueries


class RoomServices:
    def __init__(self, db: Session):
        self.queries = RoomQueries(db=db)
        self.db = db

    async def create_room(self, name: str, owner_id: int, year: int, month: int,
                          duties_per_day: int = 1):
        room = await self.queries.create_room(
            name=name,
            owner_id=owner_id,
            duties_per_day=duties_per_day
        )
        self.db.commit()
        self.db.refresh(room)
        await self.queries.create_duties_for_room(
            room_id=room.id,
            year=year,
            month=month,
            duties_per_day=duties_per_day
        )
        self.db.commit()
        return room