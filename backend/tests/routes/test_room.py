import os
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from api.errors.auth import UserAlreadyExist
from core.config import get_settings
from db.database import DATABASE_URL, DATABASE_FILENAME
from main import app
from models.pydantic.auth import UserDataCreate, TokenData
from models.pydantic.types import UserOriginTypes
from services.auth import UserServices, TokenServices

engine = create_engine(DATABASE_URL)
# Create all tables
SQLModel.metadata.create_all(engine)


def db_session():
    with Session(engine) as session:
        yield session


def cleanup_database():
    if os.path.exists(DATABASE_FILENAME):
        os.remove(DATABASE_FILENAME)


def settings():
    return get_settings()


class TestRoomHandlers(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = TestClient(app)
        self.token = None  # This will hold the bearer token for authenticated requests
        self.db = next(db_session())
        await self.create_user_and_get_token()

    @classmethod
    def tearDownClass(cls):
        cleanup_database()

    async def create_user_and_get_token(self):
        # Mock user creation and token generation
        user_services = UserServices(db=self.db)
        token_services = TokenServices(
            algorithm=settings().auth_algorithm,
            secret_key=settings().secret_key
        )

        # Assuming user_services.create_user returns a user object with an id
        user_data = UserDataCreate(
            username="testuser",
            password="testpassword"
        )
        try:
            user = await user_services.create_user(user_data=user_data, origin=UserOriginTypes.web)
        except UserAlreadyExist:
            user = await user_services.get_user_by_username(username="testuser")
        token_data = TokenData(
            sub=str(user.id),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            origin=UserOriginTypes.web
        )
        self.token = await token_services._create_access_token(token_data)

    async def test_get_rooms_by_user(self):
        response = self.client.get("/room/", headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)

    async def test_create_room(self) -> dict:
        room_data = {"name": "Test Room", "date": {
            "year": 2025, "month": 1
        }}
        response = self.client.post("/room/", json=room_data, headers={"Authorization": f"Bearer {self.token}"})

        self.assertEqual(response.status_code, 201)
        response = response.json()

        return response
        # Add more assertions based on expected output

    async def test_delete_room(self):
        room = await self.test_create_room()
        # Assuming you have a room with id 1
        response = self.client.delete(f"/room/{room.get('id')}", headers={"Authorization": f"Bearer {self.token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})

    async def test_update_room(self):
        await self.create_user_and_get_token()
        room = await self.test_create_room()

        room_data = {
            "is_multiple_selection": True,
            "duties_per_day": 2
        }
        response = self.client.patch(f"/room/{room.get('id')}", json=room_data, headers={"Authorization": f"Bearer {self.token}"})

        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected output


if __name__ == '__main__':
    unittest.main()
