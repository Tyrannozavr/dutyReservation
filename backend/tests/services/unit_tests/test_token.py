import unittest
from datetime import datetime, timedelta, timezone

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
        sub="1",
        username="XXXXXXXXX",
        origin=UserOriginTypes.web
    )


@pytest.mark.asyncio
async def test_create_access_token(token_service, token_data):
    data = token_data
    token = await token_service._create_access_token(data)

    # Decode the token to verify its contents
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data['sub'] == "1"


@pytest.mark.asyncio
async def test_create_refresh_token(token_service, token_data):
    data = token_data
    token = await token_service._create_refresh_token(data)

    # Decode the token to verify its contents
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data['sub'] == "1"


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
    assert decoded_data.sub == "1"


@pytest.mark.asyncio
async def test_create_token_expire_time_zero(token_service, token_data):
    with pytest.raises(Exception, match="expire time must be grater than zero"):
        await token_service._create_token(token_data, expire_time=0)


# Assuming TokenServices and TokenData are defined in the same module
# from your_module import TokenServices, TokenData

class TestTokenServices(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.secret_key = "your_secret_key"
        self.algorithm = "HS256"
        self.token_services = TokenServices(
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            access_expire_time=TEST_ACCESS_EXPIRE_TIME,
            refresh_expire_time=TEST_REFRESH_EXPIRE_TIME
        )
        self.user_id = "12"

    def create_token(self, exp_time):
        payload = {
            "sub": self.user_id,
            "exp": exp_time
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def test_decode_token_valid(self):
        # Create a token that expires in the future
        future_expiration = datetime.now(timezone.utc) + timedelta(minutes=5)
        token = self.create_token(future_expiration.timestamp())

        # Decode the token
        token_data = await self.token_services.decode_token(token)

        # Assert that the returned data matches the expected values
        self.assertEqual(token_data.sub, self.user_id)

    async def test_decode_token_expired(self):
        # Create a token that is already expired
        past_expiration = datetime.now(timezone.utc) - timedelta(minutes=5)
        token = self.create_token(past_expiration.timestamp())

        # Check that decoding raises an exception for expired token
        with self.assertRaises(Exception) as context:
            token_data = await self.token_services.decode_token(token)

        self.assertEqual(str(context.exception), "Token has expired")

    async def test_decode_token_invalid(self):
        # Use an invalid token (e.g., random string)
        invalid_token = "invalid.token.string"

        # Check that decoding raises an exception for invalid token
        with self.assertRaises(Exception) as context:
            await self.token_services.decode_token(invalid_token)

        self.assertEqual(str(context.exception), "Invalid token")


if __name__ == '__main__':
    unittest.main()
