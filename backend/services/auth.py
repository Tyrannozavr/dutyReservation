from datetime import datetime, timezone, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from db.queries.auth import UserQueries
from models.pydantic.auth import Token, TokenData, UserDbCreate, UserDataIn, UserOriginTypes, TelegramInitData


class TokenServices:
    def __init__(self, secret_key: str, algorithm: str, access_expire_time: float, refresh_expire_time: float,
                 token_type: str = "bearer"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_expire_time
        self.refresh_token_expire_minutes = refresh_expire_time
        self.token_type = token_type

    async def _create_token(self, data: TokenData, expire_time: float):
        if expire_time <= 0:
            raise Exception("expire time must be grater than zero")
        expires_delta = timedelta(minutes=expire_time)
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.exp = expire
        encoded_jwt = jwt.encode(to_encode.model_dump(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def _create_access_token(self, data: TokenData):
        expire_time = float(self.access_token_expire_minutes)
        access_token = await self._create_token(data=data, expire_time=expire_time)
        return access_token

    async def _create_refresh_token(self, data: TokenData):
        expire_time = float(self.refresh_token_expire_minutes)
        refresh_token = await self._create_token(data=data, expire_time=expire_time)
        return refresh_token

    async def get_tokens(self, data: TokenData):
        access_token = await self._create_access_token(data=data)
        refresh_token = await self._create_refresh_token(data=data)
        return Token(access_token=access_token, refresh_token=refresh_token, token_type=self.token_type)

    # async def decode_token(self, token: str) -> TokenData:
    #     data = jwt.decode(token, self.secret_key, self.algorithm)
    #     return TokenData(**data)
    async def decode_token(self, token: str) -> TokenData:
        try:
            data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            # Check if the token is expired
            if 'exp' in data and datetime.fromtimestamp(data['exp'], timezone.utc) < datetime.now(timezone.utc):
                print("is expired")
                raise Exception("Token has expired")
            return TokenData(**data)
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

class UserServices:
    def __init__(self, pwd_context: CryptContext, db: Session, user_queries: Any = None):
        self.pwd_context = pwd_context
        self.queries = UserQueries(db=db) if not user_queries else user_queries

    async def _get_hashed_password(self, plaintext_password: str) -> str:
        return self.pwd_context.hash(plaintext_password)

    async def verify_password(self, plaintext_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plaintext_password, hashed_password)

    async def authenticate_user(self, internal_username: str, password: str):
        user = await self.queries.get_user_by_internal_username(internal_username=internal_username)
        if not user:
            return False
        if not await self.verify_password(plaintext_password=password, hashed_password=user.hashed_password):
            return False
        return user

    async def get_or_create_tg_user(self, init_data: TelegramInitData):
        return await self.queries.get_or_create_tg_user(init_data=init_data)

    async def create_user(self, user_data: UserDataIn, origin: UserOriginTypes):
        user_db = UserDbCreate(**user_data.model_dump(), hashed_password=await self._get_hashed_password(user_data.password),
                               origin=origin)
        user = await self.queries.create_user(user_data=user_db)
        return user
