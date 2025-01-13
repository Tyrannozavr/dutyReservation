import datetime

import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from db.queries.duty import DutyQueriesMixin
from models.pydantic.auth import UserOriginTypes
from models.sqlmodels.auth import User  # Assuming you have this model defined
from models.sqlmodels.duty import DutiesRoom


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="module")
def db_session():
    """Create a new database session for a test."""
    with Session(engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="module")
def setup_data(db_session):
    """Set up initial data for tests."""
    user = User(first_name="Test", last_name="User", internal_username="testuser",
                origin=UserOriginTypes.telegram, hashed_password="XXXXXXXXXXXXXX",
                id=1)  # Adjust fields according to your User model
    db_session.add(user)
    db_session.commit()

    room = DutiesRoom(id=1, owner_id=user.id)
    db_session.add(room)
    return user, room


@pytest.mark.asyncio
async def test_create_duty(db_session, setup_data):
    user, room = setup_data
    duty = await DutyQueriesMixin.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today(),
                                              db=db_session)
    assert duty.user_id == user.id
    assert duty.room_id == room.id
    assert duty.date == datetime.date.today()


@pytest.mark.asyncio
async def test_get_duty_by_id(db_session, setup_data):
    user, room = setup_data
    duty = await DutyQueriesMixin.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today(),
                                              db=db_session)
    db_session.commit()
    db_session.refresh(duty)
    retrieved_duty = await DutyQueriesMixin.get_duty_by_id(duty.id, db=db_session)
    assert retrieved_duty.id == duty.id


@pytest.mark.asyncio
async def test_get_all_duties_in_room(db_session, setup_data):
    user, room = setup_data
    await DutyQueriesMixin.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today(), db=db_session)

    duties = await DutyQueriesMixin.get_all_duties_in_room(room.id, db=db_session)
    assert len(duties) > 0


@pytest.mark.asyncio
async def test_change_duty_date(db_session, setup_data):
    user, room = setup_data
    duty = await DutyQueriesMixin.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today(),
                                              db=db_session)
    db_session.commit()
    db_session.refresh(duty)
    new_date = datetime.date.today() + datetime.timedelta(days=1)
    updated_duty = await DutyQueriesMixin.change_duty_date(db=db_session, date=new_date, duty_id=duty.id)

    assert updated_duty.date == new_date


@pytest.mark.asyncio
async def test_delete_duty(db_session, setup_data):
    user, room = setup_data
    duty = await DutyQueriesMixin.create_duty(user_id=user.id, room_id=room.id, date=datetime.date.today(),
                                              db=db_session)
    db_session.commit()
    db_session.refresh(duty)
    await DutyQueriesMixin.delete_duty(db=db_session, duty_id=duty.id)

    deleted_duty = await DutyQueriesMixin.get_duty_by_id(duty.id, db=db_session)
    assert deleted_duty is None
