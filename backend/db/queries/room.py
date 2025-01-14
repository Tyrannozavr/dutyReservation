import uuid

from sqlmodel import Session, select

from models.sqlmodels.duty import DutiesRoom


class RoomQueriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def get_room_by_identifier(self, room_identifier: uuid.UUID):
        stmt = select(DutiesRoom).where(DutiesRoom.identifier == room_identifier)
        room = self.db.exec(stmt).first()
        return room

    async def create_room(self, owner_id: int, month: int | None = None, year: int | None = None,
                          is_multiple_selection: bool = False):
        room = DutiesRoom(owner_id=owner_id, month=month, year=year, is_multiple_selection=is_multiple_selection)
        self.db.add(room)
        return room

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