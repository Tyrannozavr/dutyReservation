import uuid
import pytest
from sqlmodel import SQLModel, create_engine, Session
from db.queries.room import RoomQueriesMixin
from models.sqlmodels.auth import *
from models.sqlmodels.duty import *

# Set up an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)

# Create the database schema
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="function")
def db_session():
    # Create a new session for each test
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def setup_rooms(db_session):
    # Create some test rooms
    room1 = DutiesRoom(owner_id=1, month=5, year=2023)
    room2 = DutiesRoom(owner_id=1, month=6, year=2023)
    db_session.add(room1)
    db_session.add(room2)
    # db_session.commit()
    return room1, room2


@pytest.mark.asyncio
async def test_get_room_by_identifier(db_session, setup_rooms):
    room1, _ = setup_rooms
    result = await RoomQueriesMixin.get_room_by_identifier(room_identifier=room1.identifier, db=db_session)
    assert result is not None
    assert result.identifier == room1.identifier


@pytest.mark.asyncio
async def test_create_room(db_session):
    owner_id = 1
    room = await RoomQueriesMixin.create_room(db=db_session, owner_id=owner_id, month=7, year=2023)
    assert room is not None
    assert room.owner_id == owner_id
    assert room.month == 7
    assert room.year == 2023


@pytest.mark.asyncio
async def test_get_all_user_rooms(db_session, setup_rooms):
    room1, room2 = setup_rooms
    rooms = await RoomQueriesMixin.get_all_user_rooms(db=db_session, user_id=1)
    assert len(rooms) == 2
    assert room1 in rooms
    assert room2 in rooms


@pytest.mark.asyncio
async def test_delete_room(db_session, setup_rooms):
    room1, _ = setup_rooms
    db_session.commit()
    deleted_room = await RoomQueriesMixin.delete_room(db=db_session, room_id=room1.id)

    assert deleted_room is not None
    assert deleted_room.id == room1.id

    # Verify that the room is no longer in the database
    remaining_rooms = await RoomQueriesMixin.get_all_user_rooms(db=db_session, user_id=1)
    assert len(remaining_rooms) == 1  # Only one room should remain after deletion
