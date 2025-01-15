import jwt
import pytest

from models.pydantic.auth import TokenData, Token, UserOriginTypes
from services.auth import TokenServices

TEST_ACCESS_EXPIRE_TIME = 30
TEST_REFRESH_EXPIRE_TIME = 60
SECRET_KEY = "test_secret"
ALGORITHM = "HS256"


@pytest.fixture(scope="module")
def token_service():
    return TokenServices(secret_key=SECRET_KEY, algorithm=ALGORITHM, access_expire_time=TEST_ACCESS_EXPIRE_TIME,
                         refresh_expire_time=TEST_REFRESH_EXPIRE_TIME)


@pytest.fixture(scope="module")
def token_data():
    return TokenData(
        id=1,
        username="XXXXXXXXX",
        origin=UserOriginTypes.web
    )

@pytest.mark.asyncio
async def test_create_access_token(token_service, token_data):
    data = token_data
    token = await token_service._create_access_token(data)

    # Decode the token to verify its contents
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data['id'] == 1

@pytest.mark.asyncio
async def test_create_refresh_token(token_service, token_data):
    data = token_data
    token = await token_service._create_refresh_token(data)

    # Decode the token to verify its contents
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data['id'] == 1

@pytest.mark.asyncio
async def test_get_tokens(token_service, token_data):
    tokens = await token_service.get_tokens(token_data)
    assert isinstance(tokens, Token)
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None


@pytest.mark.asyncio
async def test_decode_token(token_service, token_data):
    token = await token_service._create_access_token(token_data)

    decoded_data = await token_service.decode_token(token)
    assert decoded_data.id == 1


@pytest.mark.asyncio
async def test_create_token_expire_time_zero(token_service, token_data):
    with pytest.raises(Exception, match="expire time must be grater than zero"):
        await token_service._create_token(token_data, expire_time=0)
