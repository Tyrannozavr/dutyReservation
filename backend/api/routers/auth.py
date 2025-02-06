from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from api.dependencies.auth import InitDataDep, AuthorizedUserType, \
    UserDataCreateDep, UserServicesDep, TokenServicesDep, RefreshTokenDep, TelegramInitDataServiceDep, LoginDataDep
from api.errors.auth import IncorrectUsernameOrPassword, TelegramInitDataIncorrect
from logger import logger
from models.pydantic.auth import Token, UserRead, TokenData, UserOriginTypes

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(user_services: UserServicesDep,
                                 token_services: TokenServicesDep,
                                 telegram_services: TelegramInitDataServiceDep,
                                 form_data: OAuth2PasswordRequestForm = Depends(),
                                 ):
    """Takes parameters as a form data to test automatically generated auth form in swagger UI"""
    if form_data.password == "telegram":
        try:
            init_data = await telegram_services.validated_telegram_init_data(form_data.username)
            return await telegram_auth(
                init_data=init_data,
                user_services=user_services,
                token_services=token_services
            )
        except TelegramInitDataIncorrect:
            logger.info("username taken as init data is", form_data.username)
    user = await user_services.authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise IncorrectUsernameOrPassword
    token_data = TokenData(sub=str(user.id), username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=UserOriginTypes.web)
    return await token_services.get_tokens(data=token_data)


@router.post("/login", response_model=Token)
async def login_for_access_token(user_services: UserServicesDep,
                                 token_services: TokenServicesDep,
                                 telegram_services: TelegramInitDataServiceDep,
                                 login_data: LoginDataDep,
                                 ):
    if login_data.password == "telegram":
        try:
            init_data = await telegram_services.validated_telegram_init_data(login_data.username)
            return await telegram_auth(
                init_data=init_data,
                user_services=user_services,
                token_services=token_services
            )
        except TelegramInitDataIncorrect:
            logger.info("username taken as init data is", login_data.username)
    user = await user_services.authenticate_user(username=login_data.username, password=login_data.password)
    if not user:
        raise IncorrectUsernameOrPassword
    token_data = TokenData(sub=str(user.id), username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=UserOriginTypes.web)
    return await token_services.get_tokens(data=token_data)


@router.post(
    "/token/refresh",
    status_code=200,
    response_model=Token
)
async def refresh_access_token(token_services: TokenServicesDep, refresh_token: RefreshTokenDep):
    refresh_token_data = await token_services.decode_token(refresh_token.refresh_token)
    if refresh_token_data.type == "refresh":
        return await token_services.get_tokens(data=refresh_token_data)
    else:
        raise InvalidTokenError


@router.post(
    "/telegram",
    status_code=200,
    responses={
        200: {"description": "Successful authorization"},
        201: {"description": "Resource created"},
        404: {"description": "InitData isn't appropriate"},
    },
    response_model=Token
)
async def telegram_auth(init_data: InitDataDep, user_services: UserServicesDep, token_services: TokenServicesDep):
    """allows to get access to this platform using telegram's webapp initData"""
    if not init_data:
        raise HTTPException(status_code=404, detail="InitData isn't appropriate")
    user_tg_data = await user_services.get_or_create_tg_user(init_data.user)
    user = user_tg_data.user
    token_data = TokenData(sub=str(user.id), username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=user.origin)
    tokens = await token_services.get_tokens(data=token_data)
    return tokens


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
    return await token_services.get_tokens(data=token_data)


@router.get(
    "/me",
    status_code=200,
    response_model=UserRead
)
def get_user(user: AuthorizedUserType):
    return user
