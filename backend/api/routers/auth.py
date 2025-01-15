from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from api.dependencies.auth import InitDataDep, SettingsDep, AuthorizedUserType, validated_telegram_init_data, \
    UserDataCreateDep, UserServicesDep, TokenServicesDep, RefreshTokenDep
from api.dependencies.database import SessionDep
from api.errors.auth import IncorrectUsernameOrPassword
from models.pydantic.auth import Token, UserOut, TokenData, UserOriginTypes
from models.sqlmodels.auth import User

router = APIRouter()


@router.post("/token", include_in_schema=False)
def login_for_access_token(settings: SettingsDep, db: SessionDep, user_services: UserServicesDep,
                           token_services: TokenServicesDep, form_data: OAuth2PasswordRequestForm = Depends()):
    """Takes initData from telegram webapp as username and "telegram" as a password to get tokens with telegram
    initData"""
    if form_data.password == "telegram":
        init_data = validated_telegram_init_data(form_data.username, telegram_bot_token=settings.telegram_bot_token)
        return telegram_auth(init_data=init_data, db=db)
    else:
        internal_username = User.get_internal_username(form_data.username, origin=UserOriginTypes.web)
        user = user_services.authenticate_user(username=internal_username, password=form_data.password)
        if not user:
            raise IncorrectUsernameOrPassword
        token_data = TokenData(sub=str(user.id), username=user.username, first_name=user.first_name,
                               last_name=user.last_name, origin=UserOriginTypes.web)
        return token_services.get_tokens(data=token_data)


@router.post(
    "/token/refresh",
    status_code=200,
    response_model=Token
)
async def refresh_access_token(token_services: TokenServicesDep, refresh_token: RefreshTokenDep):
    refresh_token_data = await token_services.decode_token(refresh_token)
    return token_services.get_tokens(data=refresh_token_data)


@router.post(
    "/telegram",
    status_code=200,
    responses={
        200: {"description": "Successful authorization"},
        201: {"description": "Resource created"},
        404: {"description": "InitData isn't appropriate"},
    }
)
def telegram_auth(init_data: InitDataDep, user_services: UserServicesDep, token_services: TokenServicesDep):
    """allows to get access to this platform using telegram's webapp initData"""
    if not init_data:
        raise HTTPException(status_code=404, detail="InitData isn't appropriate")

    user_tg_data = user_services.get_tg_user(init_data)
    user = user_tg_data.user
    token_data = TokenData(sub=str(user.id), username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=user.origin)
    return token_services.get_tokens(data=token_data)


@router.post(
    "/register",
    status_code=201,
    response_model=Token,
    responses={
        201: {"description": "Resource created"},
        404: {"description": "InitData isn't appropriate"},
    }
)
async def create_user(
        user_services: UserServicesDep,
        user_data: UserDataCreateDep,
        token_services: TokenServicesDep
):
    user = await user_services.create_user(user_data=user_data, origin=UserOriginTypes.web)
    token_data = TokenData(sub=str(user.id), username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=UserOriginTypes.web)
    return token_services.get_tokens(data=token_data)


@router.get(
    "/me",
    status_code=200,
    response_model=UserOut
)
def get_user(user: AuthorizedUserType, db: SessionDep):
    user_id = user.id
    stmt = select(User).where(User.id == user_id).join(User.tg_data)
    user_in_db = db.exec(stmt).first()
    return user_in_db
