import hashlib
import hmac
from operator import itemgetter
from typing import Annotated
from urllib.parse import parse_qsl

from fastapi import Body, HTTPException
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from api.dependencies.database import SessionDep
from core.config import Settings, get_settings
from db.queries.auth import user_queries
from models.pydantic.auth import UserDataIn, TelegramInitData
from models.sqlmodels.auth import User
from services.auth_samples import token_services

InitDataStringDep = Annotated[str, Body(title="body title", description="body description")]


def check_webapp_signature(init_data: InitDataStringDep, token: str) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False

    hash_ = parsed_data.pop('hash')
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return calculated_hash == hash_


SettingsDep = Annotated[Settings, Depends(get_settings)]


def validated_telegram_init_data(init_data: InitDataStringDep,
                                 settings: SettingsDep) -> TelegramInitData | None:
    bot_token = settings.telegram_bot_token
    data_verified = check_webapp_signature(init_data=init_data, token=bot_token)
    if not data_verified:
        return None
    parsed_data = dict(parse_qsl(init_data))
    # user_data = json.loads(parsed_data.pop("user"))
    # user = UserInDb(**user_data, origin=UserOriginTypes.telegram)
    # init_data = TelegramInitData(**parsed_data, **user_data, user=user)
    init_data = TelegramInitData(**parsed_data)
    return init_data


InitDataDep = Annotated[TelegramInitData, Depends(validated_telegram_init_data)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    description="IMPORTANT! use initData from telegram webapp as username and string \"telegram\" "
                "as password",
)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], settings: SettingsDep, db: SessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload_data = token_services.decode_token(token)
        user = user_queries.get_user_by_id(user_id=payload_data.user_id, db=db)
        user = User(**payload_data)
    except InvalidTokenError:
        raise credentials_exception
    if not user:
        raise credentials_exception
    return user


AuthorizedUserType = Annotated[User, Depends(get_current_user)]
UserDataCreateDep = Annotated[UserDataIn, Body()]
