import asyncio
import datetime

import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from api.errors.duty import DutyIsAlreadyTaken
from db.repositories.duty import DutyRepositories
from models.pydantic.types import UserOriginTypes
from models.sqlmodels.auth import DutiesRoom
from models.sqlmodels.auth import User  # Assuming you have this model defined

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
        room = DutiesRoom(id=1, owner_id=user.id, year=datetime.date.today().year, month=datetime.date.today().year)
        db_session.add(room)
        return user, room


@pytest.mark.asyncio
async def test_load_set_duty_user(db_session, duty_queries, setup_data):
    users_request_per_time = 200
    free_duties_per_day = 3
    user, room = setup_data

    # Create 2 duties for today
    await asyncio.gather(
        *[
            duty_queries.create_duty(room_id=room.id, date=datetime.date.today())
            for _ in range(free_duties_per_day)
        ]
    )
    db_session.commit()  # Commit the duties creation

    duty_date = datetime.date.today()

    async def try_set_duty_user(user_id):
        try:
            return await duty_queries.set_duty_user_if_free(user_id=user_id, room_id=room.id, date=duty_date)
        except DutyIsAlreadyTaken:
            pass

    # Simulate 5 concurrent requests for user reservations
    user_ids = [user_id for user_id in range(1, users_request_per_time + 1)]  # Assuming user IDs are 1 through 5
    results = await asyncio.gather(*(try_set_duty_user(user_id) for user_id in user_ids))

    # Check results
    successful_reservations = [result for result in results if result is not None]

    # There should be only 2 successful reservations
    assert len(successful_reservations) <= free_duties_per_day
    assert all(result.date == duty_date for result in successful_reservations)

    # Check that the correct users were assigned
    # assert successful_reservations[0].user_id in [1, 2]
    # assert successful_reservations[1].user_id in [1, 2]
    for user_assume_reserved in range(free_duties_per_day):
        assert successful_reservations[user_assume_reserved].user_id in list(range(1, free_duties_per_day + 1))

    # Ensure remaining attempts are None
    for i in range(free_duties_per_day, len(results)):
        assert results[i] is None
