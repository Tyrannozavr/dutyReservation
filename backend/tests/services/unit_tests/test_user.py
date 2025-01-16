import pytest
from unittest.mock import AsyncMock, Mock, MagicMock
from passlib.context import CryptContext

from db.repositories.auth import UserRepositories
from models.pydantic.auth import UserDataIn, UserOriginTypes, TelegramInitData
from services.auth import UserServices


@pytest.fixture
def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def mock_user_repositories():
    return Mock(spec=UserRepositories)


@pytest.fixture
def user_services(pwd_context, mock_user_repositories, mock_db_session):
    return UserServices(pwd_context=pwd_context, db=mock_db_session, repositories=mock_user_repositories)


@pytest.mark.asyncio
async def test_get_hashed_password(user_services):
    plaintext_password = "mysecretpassword"
    hashed_password = await user_services._get_hashed_password(plaintext_password)

    assert hashed_password is not None
    assert user_services.pwd_context.verify(plaintext_password, hashed_password)


@pytest.mark.asyncio
async def test_verify_password(user_services):
    plaintext_password = "mysecretpassword"
    hashed_password = await user_services._get_hashed_password(plaintext_password)

    result = await user_services.verify_password(plaintext_password, hashed_password)
    assert result is True

    wrong_password = "wrongpassword"
    result = await user_services.verify_password(wrong_password, hashed_password)
    assert result is False


@pytest.mark.asyncio
async def test_authenticate_user_success(user_services, mock_user_repositories):
    username = "testuser"
    password = "mysecretpassword"
    user_mock = Mock(hashed_password=await user_services._get_hashed_password(password))

    mock_user_repositories.get_user_by_username = AsyncMock(return_value=user_mock)

    authenticated_user = await user_services.authenticate_user(username, password)

    assert authenticated_user is user_mock


@pytest.mark.asyncio
async def test_authenticate_user_failure_no_user(user_services, mock_user_repositories):
    username = "nonexistentuser"
    password = "mysecretpassword"

    mock_user_repositories.get_user_by_username = AsyncMock(return_value=None)

    authenticated_user = await user_services.authenticate_user(username, password)

    assert authenticated_user is False


@pytest.mark.asyncio
async def test_authenticate_user_failure_wrong_password(user_services, mock_user_repositories):
    username = "testuser"
    correct_password = "mysecretpassword"
    wrong_password = "wrongpassword"

    user_mock = Mock(hashed_password=await user_services._get_hashed_password(correct_password))
    mock_user_repositories.get_user_by_username = AsyncMock(return_value=user_mock)

    authenticated_user = await user_services.authenticate_user(username, wrong_password)

    assert authenticated_user is False


@pytest.mark.asyncio
async def test_create_user(user_services, mock_user_repositories):
    user_data = UserDataIn(username="testuser", password="mysecretpassword")
    origin = UserOriginTypes.web  # Replace with actual origin type

    user_mock = Mock()
    mock_user_repositories.create_user = AsyncMock(return_value=user_mock)

    created_user = await user_services.create_user(user_data=user_data, origin=origin)

    assert created_user is user_mock
    mock_user_repositories.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_get_or_create_tg_user(user_services, mock_user_repositories):
    init_data = TelegramInitData(
        id=1,
        first_name="first_name"
    )  # Populate with necessary fields
    tg_user_mock = Mock()
    mock_user_repositories.get_or_create_tg_user = AsyncMock(return_value=tg_user_mock)

    tg_user = await user_services.get_or_create_tg_user(init_data=init_data)

    assert tg_user is tg_user_mock
