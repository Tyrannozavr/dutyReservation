from typing import Annotated

from fastapi import Body, HTTPException
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from api.dependencies.database import SessionDep
from core.config import Settings, get_settings
from models.pydantic.auth import UserDataIn, TokenData, TelegramInitData, RefreshTokenIn, LoginData
from models.sqlmodels import User
from services.auth import UserServices, TokenServices
from services.telegram import TelegramInitDataService
from fastapi import Query
InitDataStringDep = Annotated[str, Body(title="body title", description="body description")]

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_token_services(settings: SettingsDep):
    return TokenServices(secret_key=settings.secret_key, algorithm=settings.auth_algorithm,
                         access_expire_time=float(settings.access_token_expire_minutes),
                         refresh_expire_time=float(settings.refresh_token_expire_minutes),
                         token_type="bearer")


TokenServicesDep = Annotated[TokenServices, Depends(get_token_services)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    description="IMPORTANT! use initData from telegram webapp as username and string \"telegram\" "
                "as password",
)


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)], token_services: TokenServicesDep) -> TokenData:
    """Have no requests to DB"""
    return await token_services.decode_token(token=token)

async def get_token_data_query(access_token: Annotated[str, Query()], token_services: TokenServicesDep) -> TokenData:
    """Have no requests to DB"""
    return await token_services.decode_token(token=access_token)


def get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_services(db: SessionDep, pwd_context: Annotated[CryptContext, Depends(get_pwd_context)]) -> UserServices:
    return UserServices(pwd_context=pwd_context, db=db)


user_services_dep = Annotated[UserServices, Depends(get_user_services)]


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], user_services: user_services_dep,
        token_services: TokenServicesDep) -> User:
    """Makes request to DB"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload_data = await token_services.decode_token(token)
        user = await user_services.get_user_by_id(user_id=int(payload_data.sub))
    except InvalidTokenError:
        raise credentials_exception
    if not user:
        raise credentials_exception
    return user


def get_telegram_services(settings: SettingsDep):
    telegram_bot_token = settings.telegram_bot_token
    return TelegramInitDataService(bot_token=telegram_bot_token)


async def get_telegram_init_data(init_data: InitDataStringDep,
                                 telegram_services: Annotated[TelegramInitDataService, Depends(get_telegram_services)]
                                 ) -> TelegramInitData:
    return await telegram_services.validated_telegram_init_data(init_data=init_data)


InitDataDep = Annotated[TelegramInitData, Depends(get_telegram_init_data)]

AuthorizedUserType = Annotated[User, Depends(get_current_user)]
UserDataCreateDep = Annotated[UserDataIn, Body()]
TokenDataDep = Annotated[TokenData, Depends(get_token_data)]
TokenDataQueryDep = Annotated[TokenData, Depends(get_token_data_query)]
RefreshTokenDep = Annotated[RefreshTokenIn, Body()]
TelegramInitDataServiceDep = Annotated[TelegramInitDataService, Depends(get_telegram_services)]
LoginDataDep = Annotated[LoginData, Body()]