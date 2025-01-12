from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from api.dependencies.auth import InitDataDep, SettingsDep, AuthorizedUserType, get_current_user, \
    validated_telegram_init_data
from api.dependencies.database import SessionDep
from db.queries.auth import get_or_create_tg_user
from models.pydantic.auth import Token, UserOut, UserOriginsTypes
from models.sqlmodels.auth import User, TelegramUserData
from services.auth import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/login")
def login(settings: SettingsDep, db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    init_data = validated_telegram_init_data(form_data.username, settings=settings)
    return telegram_auth(init_data=init_data, settings=settings, db=db)

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
    token_data = user_tg_data.user.model_dump()
    access_token = create_access_token(data=token_data, settings=settings)
    refresh_token = create_refresh_token(data=token_data, settings=settings)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type='bearer')


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






# @router.get(
#     "/me2",
#     status_code=200,
#     response_model=UserOut
# )
# def get_user2():
#     return user