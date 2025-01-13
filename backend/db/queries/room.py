import uuid

from sqlmodel import Session, select

from models.sqlmodels.duty import DutiesRoom


class RoomQueriesMixin:
    @staticmethod
    async def get_room_by_identifier(room_identifier: uuid.UUID, db: Session):
        stmt = select(DutiesRoom).where(DutiesRoom.identifier == room_identifier)
        room = db.exec(stmt).first()
        return room

    @staticmethod
    async def create_room(db: Session, owner_id: int, month: int | None = None, year: int | None = None,
                          is_multiple_selection: bool = False):
        room = DutiesRoom(owner_id=owner_id, month=month, year=year, is_multiple_selection=is_multiple_selection)
        db.add(room)
        return room

    @staticmethod
    async def get_all_user_rooms(db: Session, user_id):
        stmt = select(DutiesRoom).where(DutiesRoom.owner_id == user_id)
        rooms = db.exec(stmt).all()
        return rooms

    @staticmethod
    async def delete_room(db: Session, room_id: int):
        stmt = select(DutiesRoom).where(DutiesRoom.id == room_id)
        room = db.exec(stmt).first()
        db.delete(room)
        return room


class Queries(RoomQueriesMixin):
    pass

room_queries = Queries()