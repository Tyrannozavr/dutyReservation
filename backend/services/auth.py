from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext
from sqlmodel import Session

from db.queries.auth import user_queries
from models.pydantic.auth import Token, TokenData, UserDbCreate, UserDataIn


class TokenServices:
    def __init__(self, secret_key: str, algorithm: str, access_expire_time: float, refresh_expire_time: float,
                 token_type: str = "bearer"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_expire_time
        self.refresh_token_expire_minutes = refresh_expire_time
        self.token_type = token_type

    def _create_token(self, data: TokenData, expire_time: float):
        if expire_time <= 0:
            raise Exception("expire time must be grater than zero")
        expires_delta = timedelta(minutes=expire_time)
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.exp = expire
        encoded_jwt = jwt.encode(to_encode.model_dump(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def _create_access_token(self, data: TokenData):
        expire_time = float(self.access_token_expire_minutes)
        access_token = self._create_token(data=data, expire_time=expire_time)
        return access_token

    def _create_refresh_token(self, data: TokenData):
        expire_time = float(self.refresh_token_expire_minutes)
        refresh_token = self._create_token(data=data, expire_time=expire_time)
        return refresh_token

    def get_tokens(self, data: TokenData):
        access_token = self._create_access_token(data=data)
        refresh_token = self._create_refresh_token(data=data)
        return Token(access_token=access_token, refresh_token=refresh_token, token_type=self.token_type)

    def decode_token(self, token: str) -> TokenData:
        data = jwt.decode(token, self.secret_key, self.algorithm)
        return TokenData(**data)


class UserServices:
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def _get_hashed_password(self, plaintext_password: str) -> str:
        return self.pwd_context.hash(plaintext_password)

    def verify_password(self, plaintext_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plaintext_password, hashed_password)

    def authenticate_user(self, internal_username: str, password: str, db: Session):
        user = user_queries.get_user_by_internal_username(internal_username=internal_username, db=db)
        if not user:
            return False
        if not self.verify_password(plaintext_password=password, hashed_password=user.hashed_password):
            return False
        return user

    async def create_user(self, user_data: UserDataIn, db: Session):
        user_db = UserDbCreate(**user_data.model_dump(), hashed_password=self._get_hashed_password(user_data.password))
        user = await user_queries.create_user(user_data=user_db, db=db)
        return user
