import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session

from api.errors.auth import UserAlreadyExist
from core.config import get_settings
from db.database import DATABASE_URL, DATABASE_FILENAME
from main import app  # Assuming your FastAPI app is defined in main.py
from models.pydantic.auth import UserDataIn, TelegramInitData
from models.sqlmodels.auth import *
from services.auth import UserServices
from services.telegram import TelegramInitDataService

telegram_id = 3432
telegram_first_name = "John"
telegram_last_name = "Silver"
telegram_username = "An old pirate"

engine = create_engine(DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(engine)


@pytest.fixture(scope="session", autouse=True)
def cleanup_database():
    yield  # This will run tests
    # Cleanup code goes here, executed after all tests
    if os.path.exists(DATABASE_FILENAME):
        os.remove(DATABASE_FILENAME)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def user_services(db_session):
    return UserServices(db=db_session)


@pytest.fixture
def create_user(db_session, user_services):
    async def _create_user(username: str, password: str):
        user_data = UserDataIn(
            username=username,
            password=password
        )
        user = await user_services.create_user(user_data=user_data, origin=UserOriginTypes.web)
        return user

    return _create_user


@pytest.fixture
def telegram_services(settings):
    bot_token = settings.telegram_bot_token
    return TelegramInitDataService(bot_token=bot_token)


@pytest.mark.asyncio
async def test_init_data_generation(telegram_services):
    username = "example_user"
    tg_user = {
        "id": "123456789",
        "username": username,
        "first_name": "John",
    }

    # Generate the query string with a valid signature
    init_data_dict = {
        "user": tg_user,
        "chat_instance": "987654321",
        "auth_date": "1633036800",  # Example timestamp
    }
    init_data = TelegramInitData(
        **init_data_dict
    )
    query_string = await telegram_services.generate_webapp_signature_data(init_data)
    data = await telegram_services.validated_telegram_init_data(query_string)
    assert data.user.username == username
    return query_string


@pytest.mark.asyncio
async def test_login_telegram(client, telegram_services):
    user = {
        "id": telegram_id,
        "username": telegram_username,
        "first_name": telegram_first_name,
    }
    init_data_dict = {
        "user": user
    }
    init_data = TelegramInitData(**init_data_dict)
    init_data_string = await telegram_services.generate_webapp_signature_data(init_data)
    response = client.post("/auth/telegram", json=init_data_string)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_username(client):
    response = client.post("/auth/token", data={"username": "invalid_user", "password": "wrong_password"})
    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_login_valid_user(client, create_user, user_services):
    try:
        await create_user("test_user", "test_password")
    except UserAlreadyExist:
        pass
    response = client.post("/auth/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_access_token(client, create_user):
    # First, log in to get a refresh token
    try:
        await create_user("test_user", "test_password")
    except UserAlreadyExist:
        pass

    login_response = client.post("/auth/token", data={"username": "test_user", "password": "test_password"})
    refresh_token = login_response.json().get("refresh_token")
    response = client.post("/auth/token/refresh", json=refresh_token)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_telegram_auth(client, telegram_services):
    # Mock valid init_data for Telegram authentication
    init_data = await test_init_data_generation(telegram_services)
    init_data = {"username": init_data, "password": "telegram"}  # Adjust according to your actual init_data structure
    response = client.post("/auth/token", data=init_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_user(client):
    user_data = {
        "username": "new_user_one",
        "password": "new_password",
        # Add other required fields based on your UserDataCreateDep model
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_user(client, create_user, user_services):
    try:
        user = await create_user("test_user", "test_password")
    except UserAlreadyExist:
        user = await user_services.get_user_by_username(username="test_user")

    # Log in to get an access token for the user
    login_response = client.post("/auth/token", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.json().get("access_token")

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == user.username

    # if os.path.exists(DATABASE_FILENAME):
    #     os.remove(DATABASE_FILENAME)
