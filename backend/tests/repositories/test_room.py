from datetime import timedelta

import pytest
from sqlmodel import create_engine, Session

from db.repositories.duty import DutyRepositories
from db.repositories.room import RoomRepositories
from models.sqlmodels import *

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
def room_queries(db_session):
    return RoomRepositories(db_session)


@pytest.fixture(scope="function")
def duty_queries(db_session):
    return DutyRepositories(db_session)


@pytest.fixture(scope="function")
def setup_rooms(db_session):
    # Create some test rooms
    room1 = DutiesRoom(owner_id=1, month=1, year=3000)
    room2 = DutiesRoom(owner_id=1, month=12, year=3000)
    db_session.add(room1)
    db_session.add(room2)
    # db_session.commit()
    return room1, room2


@pytest.mark.asyncio
async def test_get_room_by_identifier(db_session, setup_rooms, room_queries):
    room1, _ = setup_rooms
    result = await room_queries.get_room_by_identifier(room_identifier=room1.identifier)
    assert result is not None
    assert result.identifier == room1.identifier


@pytest.mark.asyncio
async def test_create_room(db_session, room_queries):
    owner_id = 1
    room = await room_queries.create_room(owner_id=owner_id, name="testings")
    assert room is not None
    assert room.owner_id == owner_id
    assert room.name == "testings"



@pytest.mark.asyncio
async def test_get_all_user_rooms(db_session, setup_rooms, room_queries):
    room1, room2 = setup_rooms
    rooms = await room_queries.get_all_users_rooms(user_id=1)
    assert len(rooms) == 2
    assert room1 in rooms
    assert room2 in rooms


@pytest.mark.asyncio
async def test_delete_room(db_session, setup_rooms, room_queries):
    room1, _ = setup_rooms
    db_session.commit()
    deleted_room = await room_queries.delete_room(room_id=room1.id)

    assert deleted_room is not None
    assert deleted_room.id == room1.id

    # Verify that the room is no longer in the database
    remaining_rooms = await room_queries.get_all_users_rooms(user_id=1)
    assert len(remaining_rooms) == 1  # Only one room should remain after deletion
