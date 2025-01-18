from unittest.mock import AsyncMock, Mock, MagicMock

import pytest
from fastapi import HTTPException
from passlib.context import CryptContext

from db.repositories.auth import UserRepositories
from models.pydantic.auth import UserDataIn, UserOriginTypes
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

    with pytest.raises(HTTPException):
        await user_services.authenticate_user(username, password)


@pytest.mark.asyncio
async def test_authenticate_user_failure_wrong_password(user_services, mock_user_repositories):
    username = "testuser"
    correct_password = "mysecretpassword"
    wrong_password = "wrongpassword"

    user_mock = Mock(hashed_password=await user_services._get_hashed_password(correct_password))
    mock_user_repositories.get_user_by_username = AsyncMock(return_value=user_mock)

    with pytest.raises(HTTPException):
        await user_services.authenticate_user(username, wrong_password)


@pytest.mark.asyncio
async def test_create_user(user_services, mock_user_repositories):
    user_data = UserDataIn(username="testuser12", password="mysecretpassword")
    origin = UserOriginTypes.web  # Replace with actual origin type

    user_mock = Mock()
    mock_user_repositories.create_user = AsyncMock(return_value=user_mock)
    mock_user_repositories.is_username_already_taken.return_value = None

    created_user = await user_services.create_user(user_data=user_data, origin=origin)

    assert created_user is user_mock
    mock_user_repositories.create_user.assert_called_once()
