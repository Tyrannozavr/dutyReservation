import unittest

from fastapi import HTTPException
from sqlmodel import Session, create_engine

from models.pydantic.auth import UserDataCreate, UserInDb, TelegramUserDataIn
from models.sqlmodels import *
from services.auth import UserServices  # Replace with the actual module name


class TestUserServices(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database
        cls.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(cls.engine)

    async def asyncSetUp(self):
        # Create a new session for each test
        self.session = Session(self.engine)
        self.user_services = UserServices(db=self.session)
        self.telegram_id = 22

    async def test_user_creation(self):
        username = "testuser723"
        password = "securepassword"
        user_data = UserDataCreate(username=username, password=password)

        user = await self.user_services.create_user(user_data=user_data, origin=UserOriginTypes.web)
        self.session.commit()
        self.session.refresh(user)
        self.assertEqual(user.username, username)

    async def test_authenticate_user_success(self):
        username = "testuser"
        password = "securepassword"
        user_data = UserDataCreate(username=username, password=password)

        await self.user_services.create_user(user_data=user_data, origin=UserOriginTypes.web)
        self.session.commit()
        authenticated_user = await self.user_services.authenticate_user(username, password)
        self.assertEqual(authenticated_user.username, username)

    async def test_authenticate_user_invalid_username(self):
        username = "invaliduser"
        password = "securepassword"

        with self.assertRaises(HTTPException):
            await self.user_services.authenticate_user(username, password)

    async def test_authenticate_user_invalid_password(self):
        username = "testuser1"
        password = "securepassword"
        wrong_password = "wrongpassword"

        hashed_password = await self.user_services._get_hashed_password(password)
        user_data = UserInDb(
            id=1,
            username=username,
            hashed_password=hashed_password,
            origin=UserOriginTypes.web)

        user = User.model_validate(user_data)
        user.hashed_password = await self.user_services._get_hashed_password(password)

        self.session.add(user)
        self.session.commit()

        with self.assertRaises(HTTPException):
            await self.user_services.authenticate_user(username, wrong_password)

    async def test_is_username_already_taken(self):
        # await self.test_user_creation()
        username = "testuser"

        is_taken = await self.user_services.is_username_already_taken(username)

        self.assertTrue(is_taken)

    async def test_is_username_not_taken(self):
        username = "newuser"

        is_taken = await self.user_services.is_username_already_taken(username)

        self.assertFalse(is_taken)

    async def test_get_or_create_tg_user_success(self):
        init_data = TelegramUserDataIn(username="tg_testuser", first_name="Telegram", last_name="User",
                                       id=self.telegram_id)

        tg_user_data = await self.user_services.get_or_create_tg_user(init_data)

        self.assertEqual(tg_user_data.username, init_data.username)
        self.assertEqual(tg_user_data.user.first_name, init_data.first_name)
        self.assertEqual(tg_user_data.user.last_name, init_data.last_name)

    async def test_get_or_create_tg_user_success2(self):
        init_data = TelegramUserDataIn(id=1204615429, first_name='Ульяна', last_name='', username=None,
                                       language_code='ru',
                                       allows_write_to_pm=True,
                                       photo_url='https://t.me/i/userpic/320/kQWtXT_LxVFGPoTwIqBOn4f2g3pg5Km4OH698SLWyE8.svg')

        tg_user_data = await self.user_services.get_or_create_tg_user(init_data)

        self.assertEqual(tg_user_data.username, init_data.username)
        self.assertEqual(tg_user_data.user.first_name, init_data.first_name)
        self.assertEqual(tg_user_data.user.last_name, init_data.last_name)

    async def test_get_or_create_tg_user_success3(self):
        init_data = TelegramUserDataIn(id=7594503250, first_name='Влад', last_name='', username='Archetypen',
                                       language_code='ru',
                                       allows_write_to_pm=None,
                                       photo_url='https://t.me/i/userpic/320/mVuI_rAVWcOsVcrQKegMdsNMg7tVWyrB-smVoHEYCXOhjGcxBDtLn2IFADSznhyo.svg')

        tg_user_data = await self.user_services.get_or_create_tg_user(init_data)

        self.assertEqual(tg_user_data.username, init_data.username)
        self.assertEqual(tg_user_data.user.first_name, init_data.first_name)
        self.assertEqual(tg_user_data.user.last_name, init_data.last_name)

    async def test_get_or_create_tg_user_success_double(self):
        init_data = TelegramUserDataIn(username="tg_testuser", first_name="Telegram", last_name="User",
                                       id=self.telegram_id)

        tg_user_data = await self.user_services.get_or_create_tg_user(init_data)

        self.assertEqual(tg_user_data.username, init_data.username)
        self.assertEqual(tg_user_data.user.first_name, init_data.first_name)
        self.assertEqual(tg_user_data.user.last_name, init_data.last_name)

        tg_user_data_again = await self.user_services.get_or_create_tg_user(init_data)

        self.assertEqual(tg_user_data_again.username, init_data.username)
        self.assertEqual(tg_user_data_again.user.first_name, init_data.first_name)
        self.assertEqual(tg_user_data_again.user.last_name, init_data.last_name)

    async def test_get_or_create_tg_user_username_taken(self):
        username = "tg_takenuser11"
        telegram_id = 3432
        init_data = TelegramUserDataIn(id=telegram_id, username=username, first_name="Taken",
                                       last_name="User")

        data = UserDataCreate(
            username=username
        )
        await self.user_services.create_user(user_data=data, origin=UserOriginTypes.web)
        tg_user_data = await self.user_services.get_or_create_tg_user(init_data)

        self.assertIsNone(tg_user_data.user.username)  # Assuming the method returns None if username is taken
        self.assertEqual(tg_user_data.user.first_name, init_data.first_name)
        self.assertEqual(tg_user_data.user.last_name, init_data.last_name)


if __name__ == "__main__":
    unittest.main()
