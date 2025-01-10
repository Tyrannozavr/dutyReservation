from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt

from core.config import Settings


def create_token(data: dict, expire_time: float, secret_key: str, algorithm: str):
    if expire_time <= 0:
        raise Exception("expire time must be grater than zero")
    expires_delta = timedelta(minutes=expire_time)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def create_access_token(data: dict, settings: Settings):
    expire_time = float(settings.access_token_expire_minutes)
    access_token = create_token(data=data, expire_time=expire_time, secret_key=settings.secret_key,
                                algorithm=settings.auth_algorithm)
    return access_token

def create_refresh_token(data: dict, settings: Settings):
    expire_time = float(settings.refresh_token_expire_minutes)
    refresh_token = create_token(data=data, expire_time=expire_time, secret_key=settings.secret_key,
                                algorithm=settings.auth_algorithm)
    return refresh_token


def decode_token(token: str, settings: Settings):
    secret_key = settings.secret_key
    algorith = settings.auth_algorithm
    data = jwt.decode(token, secret_key, algorith)
    return data
