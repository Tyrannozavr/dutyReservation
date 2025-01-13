from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from api.dependencies.auth import InitDataDep, SettingsDep, AuthorizedUserType, validated_telegram_init_data, \
    UserDataCreateDep
from api.dependencies.database import SessionDep
from api.errors.auth import IncorrectUsernameOrPassword
from db.queries import auth
from db.queries.auth import get_or_create_tg_user
from models.pydantic.auth import Token, UserOut, UserInDb, TokenData, UserOriginTypes
from models.sqlmodels.auth import User
from services.auth import get_hashed_password, get_tokens, authenticate_user

router = APIRouter()


@router.post("/login", include_in_schema=False)
def login(settings: SettingsDep, db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    """Takes initData from telegram webapp as username and "telegram" as a password to get tokens with telegram
    initData"""
    if form_data.password == "telegram":
        init_data = validated_telegram_init_data(form_data.username, settings=settings)
        return telegram_auth(init_data=init_data, settings=settings, db=db)
    else:
        user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
        if not user:
            raise IncorrectUsernameOrPassword
        token_data = TokenData(id=user.id, username=user.username, first_name=user.first_name,
                               last_name=user.last_name, origin=UserOriginTypes.web)
        return get_tokens(data=token_data, settings=settings)


@router.post(
    "/telegram",
    status_code=200,
    responses={
        200: {"description": "Successful authorization"},
        201: {"description": "Resource created"},
        404: {"description": "InitData isn't appropriate"},
    }
)
def telegram_auth(init_data: InitDataDep, settings: SettingsDep, db: SessionDep):
    """allows to get access to this platform using telegram's webapp initData"""
    if not init_data:
        raise HTTPException(status_code=404, detail="InitData isn't appropriate")
    user_tg_data = get_or_create_tg_user(init_data, db)
    user = user_tg_data.user
    token_data = TokenData(id=user.id, username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=user.origin)
    return get_tokens(data=token_data, settings=settings)

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
        db:  SessionDep,
        user_data: UserDataCreateDep,
        settings: SettingsDep,
):
    user_data_db = UserInDb(**user_data.model_dump(), hashed_password=get_hashed_password(user_data.password))

    user = await auth.create_user(user_data=user_data_db, db=db)
    token_data = TokenData(id=user.id, username=user.username, first_name=user.first_name,
                           last_name=user.last_name, origin=UserOriginTypes.web)
    return get_tokens(data=token_data, settings=settings)


# @router.get(
#     "/refresh",
#     status_code=200,
#     response_model=Token
# )
# def refresh_token(user: AuthorizedUserType, settings: SettingsDep):
#     token_data = user.model_dump()
#     access_token = create_access_token(data=token_data, settings=settings)
#     refresh_token = create_refresh_token(data=token_data, settings=settings)
#     return Token(access_token=access_token, refresh_token=refresh_token, token_type='bearer')

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

