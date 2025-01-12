from datetime import datetime, timezone, timedelta
from typing import Annotated

from sqlmodel import Session

from db.queries.auth import get_user_by_username
from models.pydantic.auth import Token, TokenData

import jwt
from passlib.context import CryptContext

from core.config import Settings


def create_token(data: TokenData, expire_time: float, secret_key: str, algorithm: str):
    if expire_time <= 0:
        raise Exception("expire time must be grater than zero")
    expires_delta = timedelta(minutes=expire_time)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    # to_encode.update({"exp": expire})
    to_encode.exp = expire
    encoded_jwt = jwt.encode(to_encode.model_dump(), secret_key, algorithm=algorithm)
    return encoded_jwt


def create_access_token(data: TokenData, settings: Settings):
    expire_time = float(settings.access_token_expire_minutes)
    access_token = create_token(data=data, expire_time=expire_time, secret_key=settings.secret_key,
                                algorithm=settings.auth_algorithm)
    return access_token

def create_refresh_token(data: TokenData, settings: Settings):
    expire_time = float(settings.refresh_token_expire_minutes)
    refresh_token = create_token(data=data, expire_time=expire_time, secret_key=settings.secret_key,
                                algorithm=settings.auth_algorithm)
    return refresh_token

def get_tokens(data: TokenData, settings: Settings):

    access_token = create_access_token(data=data, settings=settings)
    refresh_token = create_refresh_token(data=data, settings=settings)
    return Token(access_token=access_token, refresh_token=refresh_token,  token_type="bearer")


def decode_token(token: str, settings: Settings) -> TokenData:
    secret_key = settings.secret_key
    algorith = settings.auth_algorithm
    data = jwt.decode(token, secret_key, algorith)
    return TokenData(**data)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(plaintext_password: str) -> str:
    return pwd_context.hash(plaintext_password)

def verify_password(plaintext_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plaintext_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_username(username=username, db=db)
    if not user:
        return False
    if not verify_password(plaintext_password=password, hashed_password=user.hashed_password):
        return False
    return user

