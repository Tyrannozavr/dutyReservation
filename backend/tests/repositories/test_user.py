import unittest
from sqlmodel import SQLModel, create_engine, Session, select
from db.repositories.auth import UserRepositoriesMixin
from models.pydantic.auth import UserDbCreate
from models.sqlmodels.auth import *
from models.sqlmodels.auth import *

# Define a test database URL for SQLite in-memory
TEST_DATABASE_URL = "sqlite:///:memory:"


class TestUserRepositoriesMixin(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Create an in-memory SQLite database and initialize the schema
        self.engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)
        self.repository = UserRepositoriesMixin(db=self.session)


    async def test_create_user(self):
        user_data = UserDbCreate(username="testuser", hashed_password="password", origin=UserOriginTypes.web)

        user = await self.repository.create_user(user_data)

        # Commit the session to persist the changes
        self.session.commit()

        # Verify that the user has been created in the database
        retrieved_user = await self.repository.get_user_by_id(user.id)
        self.assertEqual(retrieved_user.username, user_data.username)
        return user

    async def test_get_user_by_id(self):
        user = await self.test_create_user()
        self.session.commit()
        self.session.refresh(user)
        retrieved_user = await self.repository.get_user_by_id(user.id)
        self.assertEqual(retrieved_user.id, user.id)

    async def test_get_user_by_username(self):
        user = await self.test_create_user()
        self.session.commit()
        self.session.refresh(user)
        retrieved_user = await self.repository.get_user_by_username(user.username)
        self.assertEqual(retrieved_user.username, user.username)
        self.assertEqual(retrieved_user.id, user.id)

    async def test_is_username_already_taken(self):
        username = "testuser"
        user_data = UserDbCreate(username=username, origin=UserOriginTypes.telegram)

        await self.repository.create_user(user_data)
        self.session.commit()
        is_taken = await self.repository.is_username_already_taken(username)
        self.assertTrue(is_taken)

    async def test_is_username_not_taken(self):
        username = "newuser"

        is_taken = await self.repository.is_username_already_taken(username)
        self.assertFalse(is_taken)


if __name__ == "__main__":
    unittest.main()
