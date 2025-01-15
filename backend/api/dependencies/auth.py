import hashlib
import hmac
from operator import itemgetter
from typing import Annotated, Dict
from urllib.parse import parse_qsl, urlencode, quote_plus

from fastapi import Body, HTTPException
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from api.dependencies.database import SessionDep
from core.config import Settings, get_settings
from db.queries.auth import UserQueries
from models.pydantic.auth import UserDataIn, TelegramInitData, TokenData
from models.sqlmodels.auth import User
from services.auth import UserServices, TokenServices

InitDataStringDep = Annotated[str, Body(title="body title", description="body description")]


def check_webapp_signature(init_data: InitDataStringDep, telegram_bot_token: str) -> bool:
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
        key=b"WebAppData", msg=telegram_bot_token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return calculated_hash == hash_


SettingsDep = Annotated[Settings, Depends(get_settings)]


def validated_telegram_init_data(init_data: InitDataStringDep,
                                 telegram_bot_token: str) -> TelegramInitData | None:
    bot_token = telegram_bot_token
    data_verified = check_webapp_signature(init_data=init_data, telegram_bot_token=bot_token)
    if not data_verified:
        return None
    parsed_data = dict(parse_qsl(init_data))
    init_data = TelegramInitData(**parsed_data)
    return init_data


def generate_webapp_signature_data(data: Dict[str, str], token: str) -> str:
    """
    Generate a query string that will pass the web app signature check.

    Args:
        data (Dict[str, str]): The data to include in the query string.
        token (str): The bot token used for hashing.

    Returns:
        str: A query string with a valid signature hash.
    """
    # Sort the data and create the data check string
    sorted_items = sorted(data.items())
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_items)

    # Create the secret key
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )

    # Calculate the hash
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    # Add the hash to the data
    data['hash'] = calculated_hash

    # Create the final query string
    query_string = urlencode(data, quote_via=quote_plus)
    return query_string

InitDataDep = Annotated[TelegramInitData, Depends(validated_telegram_init_data)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    description="IMPORTANT! use initData from telegram webapp as username and string \"telegram\" "
                "as password",
)

def get_token_services(settings: SettingsDep):
    return TokenServices(secret_key=settings.secret_key, algorithm=settings.auth_algorithm,
                               access_expire_time=float(settings.access_token_expire_minutes),
                               refresh_expire_time=float(settings.refresh_token_expire_minutes),
                               token_type="bearer")
TokenServicesDep = Annotated[TokenServices, Depends(get_token_services)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep,
                           token_services: TokenServicesDep) -> User:
    """Makes request to DB"""
    user_queries = UserQueries(db=db)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload_data = await token_services.decode_token(token)
        user = await user_queries.get_user_by_id(user_id=int(payload_data.sub))
    except InvalidTokenError:
        raise credentials_exception
    if not user:
        raise credentials_exception
    return user



async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)], token_services: TokenServicesDep) -> TokenData:
    """Have no requests to DB"""
    return await token_services.decode_token(token=token)

def get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_services(db: SessionDep, pwd_context: Annotated[CryptContext, Depends(get_pwd_context)]) -> UserServices:
    return UserServices(pwd_context=pwd_context, db=db)



AuthorizedUserType = Annotated[User, Depends(get_current_user)]
UserDataCreateDep = Annotated[UserDataIn, Body()]
TokenDataDep = Annotated[TokenData, Depends(get_token_data)]
UserServicesDep = Annotated[UserServices, Depends(get_user_services)]
RefreshTokenDep = Annotated[str, Body()]