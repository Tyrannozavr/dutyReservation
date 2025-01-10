from datetime import datetime, timezone, timedelta

import jwt

from api.dependencies.auth import SettingsDep


def create_access_token(data: dict, settings: SettingsDep):
    secret_key = settings.secret_key
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    algorithm = settings.auth_algorithm
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
