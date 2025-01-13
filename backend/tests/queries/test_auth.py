import pytest
from sqlalchemy import create_engine
from sqlmodel import Session

from db.queries.auth import user_queries  # Adjust the import according to your project structure
from models.pydantic.auth import UserDbCreate, UserInDb, \
    TelegramUserDataIn
from models.sqlmodels.auth import *
from models.sqlmodels.duty import *

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)

# Create all tables in the test database
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    with Session(engine) as session:
        yield session
        session.rollback()  # Rollback after each test


@pytest.fixture(scope="module")
def test_user_data_create():
    return UserDbCreate(first_name="Test", last_name="User", username="testuser",
                        origin=UserOriginTypes.telegram)


@pytest.fixture(scope="module")
def test_user_data():
    return UserInDb(id=1, first_name="Test", last_name="User", username="testuser",
                    origin=UserOriginTypes.telegram)


@pytest.fixture(scope="module")
def telegram_user_data():
    return TelegramUserDataIn(
        id=1225,
        first_name="test_first_name",
        # Assuming this is the correct field name
        last_name="test_last_name",
        username="testuser",
        language_code="en",
        allows_write_to_pm=True,
        photo_url="http://example.com/photo.jpg",
    )


def test_get_or_create_tg_user(db_session, telegram_user_data):
    user_tg_data = user_queries.get_or_create_tg_user(telegram_user_data, db_session)
    assert user_tg_data is not None
    assert user_tg_data.user.internal_username == f"{TELEGRAM_PREFIX}testuser"  # Assuming TELEGRAM_PREFIX is "telegram_"

    # Try to get the same user again
    user_tg_data_again = user_queries.get_or_create_tg_user(telegram_user_data, db_session)
    assert user_tg_data_again.telegram_id == user_tg_data.telegram_id  # Should return the same instance
    assert user_tg_data_again.user.id == user_tg_data.user.id  # Should return the same instance


def test_create_user(db_session, test_user_data_create):
    created_user = user_queries.create_user(test_user_data_create, db_session)
    assert created_user is not None
    assert created_user.username == test_user_data_create.username


def test_get_user_by_id(db_session, test_user_data_create):
    # First, create the user in the database
    created_user = user_queries.create_user(test_user_data_create, db_session)
    db_session.commit()
    db_session.refresh(created_user)
    # Now retrieve it by ID
    retrieved_user = user_queries.get_user_by_id(created_user.id, db_session)
    assert retrieved_user is not None
    assert retrieved_user.username == test_user_data_create.username


def test_get_user_by_username(db_session, test_user_data_create):
    # Now retrieve it by username
    internal_username = User.get_internal_username(test_user_data_create.username, origin=UserOriginTypes.web)
    retrieved_user = user_queries.get_user_by_internal_username(internal_username, db_session)
    assert retrieved_user is not None
    assert retrieved_user.username == test_user_data_create.username
