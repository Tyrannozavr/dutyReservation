import pytest
from sqlmodel import Session, create_engine, SQLModel

from models.sqlmodels.auth import *
from models.sqlmodels.duty import *

from db.queries.auth import get_or_create_tg_user, create_user, get_user_by_id, \
    get_user_by_username  # Adjust the import according to your project structure
from models.pydantic.auth import TelegramUserData as TelegramUserDataPydantic, UserInDb, UserOriginTypes

# Set up a test database
DATABASE_URL = "sqlite:///./test.db"  # Use an in-memory SQLite database for testing
engine = create_engine(DATABASE_URL)

# Create all tables in the test database
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    with Session(engine) as session:
        yield session
        session.rollback()  # Rollback after each test


@pytest.fixture
def test_user_data():
    return UserInDb(id=1, first_name="Test", last_name="User", username="testuser",
                    origin=UserOriginTypes.telegram)


@pytest.fixture
def telegram_user_data(test_user_data):
    return TelegramUserDataPydantic(
        language_code="en",
        allows_write_to_pm=True,
        photo_url="http://example.com/photo.jpg",
        user=test_user_data,
    )


def test_get_or_create_tg_user(db_session, telegram_user_data):
    user_tg_data = get_or_create_tg_user(telegram_user_data, db_session)
    assert user_tg_data is not None
    assert user_tg_data.user.internal_username == f"{TELEGRAM_PREFIX}testuser"  # Assuming TELEGRAM_PREFIX is "telegram_"

    # Try to get the same user again
    user_tg_data_again = get_or_create_tg_user(telegram_user_data, db_session)
    assert user_tg_data_again.telegram_id == user_tg_data.telegram_id  # Should return the same instance
    assert user_tg_data_again.user.id == user_tg_data.user.id  # Should return the same instance


def test_create_user(db_session, test_user_data):
    created_user = create_user(test_user_data, db_session)
    assert created_user is not None
    assert created_user.username == test_user_data.username


def test_get_user_by_id(db_session, test_user_data):
    # First, create the user in the database
    create_user(test_user_data, db_session)

    # Now retrieve it by ID
    retrieved_user = get_user_by_id(test_user_data.id, db_session)
    assert retrieved_user is not None
    assert retrieved_user.username == test_user_data.username


def test_get_user_by_username(db_session, test_user_data):
    # First, create the user in the database
    create_user(test_user_data, db_session)

    # Now retrieve it by username
    retrieved_user = get_user_by_username(test_user_data.username, db_session)
    assert retrieved_user is not None
    assert retrieved_user.username == test_user_data.username
