import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from main import app  # Assuming your FastAPI app is defined in main.py
from models.pydantic.auth import UserDataIn, UserOriginTypes, TelegramInitData
from services.auth import UserServices
from services.telegram import TelegramInitDataService

telegram_id=3432
telegram_first_name="John Silver"
test_bot_token = "supersecret_bot_token"

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    # Create a new database session for each test
    with Session() as session:
        yield session


@pytest.fixture
def create_user(db_session):
    # Helper function to create a user for testing purposes
    async def _create_user(username: str, password: str):
        user_services = UserServices(db=db_session)
        # user = User(username=username, hashed_password=password)  # Adjust according to your User model
        # db_session.add(user)
        user_data = UserDataIn(
            username=username,
            password=password
        )
        user = await user_services.create_user(user_data=user_data, origin=UserOriginTypes.web)
        db_session.commit()
        return user
    return _create_user

@pytest.fixture
def telegram_services():
    return TelegramInitDataService(bot_token=test_bot_token)

def test_init_data_generation(token_service):
    example_data = {
        "user_id": "123456789",
        "username": "example_user",
        "chat_id": "987654321",
        "auth_date": "1633036800",  # Example timestamp
    }

    # Your bot token (replace with your actual token)
    bot_token = "test_bot_token"

    # Generate the query string with a valid signature
    query_string = token_service.generate_webapp_signature_data(example_data, bot_token)
    print(query_string)
    data = token_service.validated_telegram_init_data(query_string, telegram_bot_token=bot_token)
    print("data is", data)


def test_login_telegram(client):
    init_data = TelegramInitData(
        id=telegram_id,
        first_name=telegram_first_name
    )
    # init_data_string = get_validated_telegram_init_data_string(init_data=init_data)
    response = client.post("/token", data={"username": "init_data_string", "password": "telegram"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_username(client):
    response = client.post("/token", data={"username": "invalid_user", "password": "wrong_password"})
    assert response.status_code == 401  # Unauthorized


def test_login_valid_user(client, create_user):
    user = create_user("test_user", "test_password")
    response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_access_token(client):
    # First, log in to get a refresh token
    login_response = client.post("/token", data={"username": "test_user", "password": "telegram"})
    refresh_token = login_response.json().get("refresh_token")

    response = client.post("/token/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_telegram_auth(client):
    # Mock valid init_data for Telegram authentication
    init_data = {"username": "test_user"}  # Adjust according to your actual init_data structure
    response = client.post("/telegram", json=init_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_user(client):
    user_data = {
        "username": "new_user",
        "password": "new_password",
        # Add other required fields based on your UserDataCreateDep model
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 201
    assert "access_token" in response.json()


def test_get_user(client, create_user):
    user = create_user("test_user", "test_password")

    # Log in to get an access token for the user
    login_response = client.post("/token", data={"username": "test_user", "password": "test_password"})
    access_token = login_response.json().get("access_token")

    response = client.get("/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == user.username

# Add more tests as needed...
