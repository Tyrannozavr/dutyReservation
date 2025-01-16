# from unittest import TestCase, IsolatedAsyncioTestCase
#
# import pytest
# from sqlalchemy import create_engine
# from sqlmodel import Session
#
# from db.repositories.auth import UserRepositories
# from models.pydantic.auth import UserDbCreate, UserInDb, \
#     TelegramUserDataIn
# from models.sqlmodels.auth import *
# from models.sqlmodels.duty import *
#
# DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(DATABASE_URL)
#
# # Create all tables in the test database
# SQLModel.metadata.create_all(engine)
#
# @pytest.fixture(scope="function")
# def db_session():
#     """Create a new database session for a test."""
#     with Session(engine) as session:
#         yield session
#         session.rollback()  # Rollback after each test
#
# @pytest.fixture(scope="module")
# def test_user_data_create():
#     return UserDbCreate(first_name="Test", last_name="User", username="testuser",
#                         origin=UserOriginTypes.telegram)
#
#
# @pytest.fixture(scope="module")
# def test_user_data():
#     return UserInDb(id=1, first_name="Test", last_name="User", username="testuser",
#                     origin=UserOriginTypes.telegram)
#
#
# @pytest.fixture(scope="module")
# def telegram_user_data():
#     return TelegramUserDataIn(
#         id=1225,
#         first_name="test_first_name",
#         # Assuming this is the correct field name
#         last_name="test_last_name",
#         username="testuser",
#         language_code="en",
#         allows_write_to_pm=True,
#         photo_url="http://example.com/photo.jpg",
#     )
# @pytest.fixture(scope="function")
# def user_queries(db_session):
#     return UserRepositories(db=db_session)
#
#
# @pytest.mark.asyncio
# async def test_create_user(test_user_data_create, user_queries):
#     created_user = await user_queries.create_user(test_user_data_create)
#     assert created_user is not None
#     assert created_user.username == test_user_data_create.username
#
#
# @pytest.mark.asyncio
# async def test_get_user_by_id(db_session, test_user_data_create, user_queries):
#     # First, create the user in the database
#     created_user = await user_queries.create_user(test_user_data_create)
#     db_session.commit()
#     db_session.refresh(created_user)
#     # Now retrieve it by ID
#     retrieved_user = await user_queries.get_user_by_id(created_user.id)
#     assert retrieved_user is not None
#     assert retrieved_user.username == test_user_data_create.username
#
# @pytest.mark.asyncio
# async def test_get_user_by_username(db_session, test_user_data_create, user_queries):
#     # Now retrieve it by username
#     username = User.get_username(test_user_data_create.username, origin=UserOriginTypes.web)
#     retrieved_user = await user_queries.get_user_by_username(username)
#     assert retrieved_user is not None
#     assert retrieved_user.username == test_user_data_create.username
