import unittest

from sqlalchemy import create_engine
from sqlmodel import Session

from db.repositories.auth import TelegramUserRepositoriesMixin
from models.sqlmodels.auth import *
from models.sqlmodels.duty import *

TEST_DATABASE_URL = "sqlite:///:memory:"

class TestTelegramUserRepositoriesMixin(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
        SQLModel.metadata.create_all(self.engine)

        # Create a new session for each test
        self.db = Session(self.engine)
        self.repository = TelegramUserRepositoriesMixin(db=self.db)
        self.telegram_id=123
        self.telegram_username="testuser"

    async def test_create_tg_user(self):
        init_data = TelegramUserData(
            id=self.telegram_id,
            username=self.telegram_username,
            language_code="en",
            allows_write_to_pm=True,
            photo_url="http://example.com/photo.jpg"
        )

        user_tg = await self.repository.create_tg_user(init_data)
        self.db.commit()
        self.db.refresh(user_tg)
        # Check that the user was added to the session
        self.assertEqual(user_tg.id, init_data.id)
        self.assertEqual(user_tg.username, init_data.username)

    async def test_get_tg_user_by_id(self):
        await self.test_create_tg_user()
        user = await self.repository.get_tg_user_by_id(self.telegram_id)

        # Verify that the correct query was executed
        self.assertEqual(user.id, self.telegram_id)

    async def test_get_tg_user_by_username(self):
        await self.test_create_tg_user()
        user = await self.repository.get_tg_user_by_username(self.telegram_username)

        # Verify that the correct query was executed
        self.assertEqual(user.username, self.telegram_username)

    async def test_get_tg_user_by_username_not_found(self):
        telegram_username = "nonexistentuser"
        user = await self.repository.get_tg_user_by_username(telegram_username)
        # Verify that the correct query was executed
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
