import os
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from api.errors.auth import UserAlreadyExist
from core.config import get_settings
from db.database import DATABASE_URL, engine
from main import app
from models.pydantic.auth import UserDataCreate, TokenData
from models.pydantic.room import RoomCreate
from models.pydantic.types import UserOriginTypes
from services.auth import UserServices, TokenServices
from services.duty import DutyServices
from services.room import RoomServices
from models.sqlmodels.auth import *


def cleanup_database():
    if os.path.exists(DATABASE_URL):
        os.remove(DATABASE_URL)


def db_session():
    with Session(engine) as session:
        yield session


def settings():
    return get_settings()


class TestDutyHandlers(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        # Create an engine for the in-memory database
        cls.engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    def setUp(self):
        # Create tables in the in-memory database before each test
        SQLModel.metadata.create_all(self.engine)
        self.client = TestClient(app)
        self.token = None  # This will hold the bearer token for authenticated requests
        self.db = Session(self.engine)  # Create a new session for each test
        self.room_services = RoomServices(db=self.db)
        self.duty_services = DutyServices(db=self.db)
        self.owner_id = 1
        self.user_id = 2

    async def asyncSetUp(self):
        await self.create_user_and_get_token()
        await self.create_test_room()

    def tearDown(self):
        # Close the session after each test
        self.db.close()
        cleanup_database()


    @classmethod
    def tearDownClass(cls):
        # Dispose of the engine after all tests
        cls.engine.dispose()

    async def create_user_and_get_token(self):
        user_data = UserDataCreate(username="testuser", password="testpassword")
        user_service = UserServices(self.db)
        try:
            user = await user_service.create_user(user_data, origin=UserOriginTypes.web)
        except UserAlreadyExist:
            user = await user_service.get_user_by_username(username="testuser")
        token_service = TokenServices(
            algorithm=settings().auth_algorithm,
            secret_key=settings().secret_key
        )
        token_data = TokenData(
            sub=str(user.id),
            username=user.username,
            origin=user.origin
        )
        self.token = await token_service._create_access_token(token_data)

    async def create_test_room(self):
        room_data = RoomCreate(
            is_multiple_selection=False,
            duty_dates=[
                datetime.date(2025, 2, 2),
                datetime.date(2025, 2, 12),
            ]
        )
        room = await self.room_services.create_room(room_data=room_data, owner_id=self.owner_id)
        self.room_identifier = room.identifier

    async def test_reserve_date(self):
        new_date = "2025-02-02"  # Example new date
        response = self.client.put(
            f"/duty/{self.room_identifier}/",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"duty_date": new_date}
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("id", response.json())  # Adjust according to your actual response structure
        duty = response.json()
        return duty

    async def test_reserve_invalid_date(self):
        new_date = "2026-02-02"  # Example new date
        response = self.client.put(
            f"/duty/{self.room_identifier}/",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"duty_date": new_date}
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("detail", response.json())  # Adjust according to your actual response structure


    async def test_delete_duty(self):
        duty = await self.test_reserve_date()

        response = self.client.delete(
            f"/duty/{duty.get('id')}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.json(), {"status": "success"})
        self.assertEqual(200, response.status_code)

    async def test_change_duty(self):
        duty = await self.test_reserve_date()
        response = self.client.put(
            f"/duty/{duty.get('id')}",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"duty_date": "2025-02-12"}
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("date", response.json())

