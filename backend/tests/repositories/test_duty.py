import datetime
from datetime import timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session

from api.errors.duty import DutyIsAlreadyTaken
from db.repositories.duty import DutyRepositories
from models.pydantic.duty import DutyChange
from models.pydantic.types import UserOriginTypes
from models.sqlmodels import DutiesRoom
from models.sqlmodels import User  # Assuming you have this model defined

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def duty_queries(db_session):
    """Create a new database session for a test."""
    return DutyRepositories(db_session)


@pytest.fixture(scope="module")
def setup_data():
    """Set up initial data for tests."""
    user = User(first_name="Test", last_name="User", username="testuser",
                origin=UserOriginTypes.telegram, hashed_password="XXXXXXXXXXXXXX",
                id=1)  # Adjust fields according to your User model
    with Session(engine) as db_session:
        db_session.add(user)
        db_session.commit()
        room = DutiesRoom(id=1, owner_id=user.id)
        db_session.add(room)
        return user, room


@pytest.mark.asyncio
async def test_create_duty(setup_data, duty_queries):
    user, room = setup_data
    duty = await duty_queries.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today())
    assert duty.user_id == user.id
    assert duty.room_id == room.id
    assert duty.date == datetime.date.today()


@pytest.mark.asyncio
async def test_get_duty_by_id(db_session, duty_queries, setup_data):
    user, room = setup_data
    duty = await duty_queries.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today())
    db_session.commit()
    db_session.refresh(duty)
    retrieved_duty = await duty_queries.get_duty_by_id(duty.id)
    assert retrieved_duty.id == duty.id


@pytest.mark.asyncio
async def test_set_duty_user(db_session, duty_queries, setup_data):
    user, room = setup_data
    # create 2 duties
    [
        await duty_queries.create_duty(room_id=room.id, date=datetime.date.today())
        for _ in range(2)
    ]
    db_session.commit()
    duty_date = datetime.date.today()
    first_user = await duty_queries.set_duty_user_if_free(user_id=1, room_id=room.id, date=duty_date)
    assert first_user.date == duty_date
    second_user = await duty_queries.set_duty_user_if_free(user_id=2, room_id=room.id, date=datetime.date.today())
    assert second_user.date == duty_date
    # try to occupy date which is already taken (there was 2 free duty on this date)
    with pytest.raises(DutyIsAlreadyTaken):
        third_user = await duty_queries.set_duty_user_if_free(user_id=3, room_id=room.id, date=datetime.date.today())
        assert third_user is None


@pytest.mark.asyncio
async def test_get_all_duties_in_room(duty_queries, db_session):
    local_room_id = 13
    local_user_id = 13
    await duty_queries.create_duty(user_id=local_user_id, room_id=local_room_id, date=datetime.date.today())
    try:
        duties = await duty_queries.get_all_duties_in_room(local_room_id)
    except IntegrityError:
        db_session.rollback()
        duties = await duty_queries.get_all_duties_in_room(local_room_id)
    assert len(duties) == 1


@pytest.mark.asyncio
async def test_change_duty_date(db_session, duty_queries, setup_data):
    date = datetime.date.today() - datetime.timedelta(days=1)

    user, room = setup_data
    duty = await duty_queries.create_duty(user_id=user.id, room_id=room.id, date=date)
    db_session.commit()
    db_session.refresh(duty)
    new_date = datetime.date.today() + datetime.timedelta(days=1)
    duty_change = DutyChange(date=new_date)
    updated_duty = await duty_queries.update_duty(duty_id=duty.id, duty_change=duty_change)
    assert updated_duty.date == new_date


@pytest.mark.asyncio
async def test_get_duties_for_user(db_session, duty_queries, setup_data):
    local_user_id = 12
    user, room = setup_data
    date_first = datetime.date.today() + timedelta(days=3)
    date_second = datetime.date.today() + timedelta(days=4)

    await duty_queries.create_duty(user_id=local_user_id, room_id=room.id, date=date_first)
    await duty_queries.create_duty(user_id=local_user_id, room_id=room.id, date=date_second)

    db_session.commit()
    user_duties = await duty_queries.get_duties_by_user_id(user_id=local_user_id)
    assert len(user_duties) == 2


@pytest.mark.asyncio
async def test_delete_duty(db_session, duty_queries, setup_data):
    user, room = setup_data
    duties = await duty_queries.get_all_duties_in_room(room_id=room.id)
    duty = duties[0]
    await duty_queries.delete_duty(duty_id=duty.id)
    deleted_duty = await duty_queries.get_duty_by_id(duty.id)

    assert deleted_duty is None
