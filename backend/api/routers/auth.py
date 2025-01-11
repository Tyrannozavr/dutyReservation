from fastapi import HTTPException
from fastapi.routing import APIRouter
from sqlmodel import select

from api.dependencies.auth import InitDataDep, SettingsDep, AuthorizedUserType
from api.dependencies.database import SessionDep
from db.queries.auth import get_or_create_tg_user
from models.pydantic.auth import Token, UserOut, UserOriginsTypes
from models.sqlmodels.auth import User, TelegramUserData
from services.auth import create_access_token, create_refresh_token

router = APIRouter()


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


'user=%7B%22id%22%3A972834722%2C%22first_name%22%3A%22%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B9%22%2C%22last_name%22%3A%22%D0%A1%D1%87%D0%B8%D1%81%D0%BB%D1%91%D0%BD%D0%BE%D0%BA%22%2C%22username%22%3A%22tyrannozavr%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FxJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg%22%7D&chat_instance=5919894213088809580&chat_type=private&auth_date=1736280453&signature=ru-H3ccFkx-Z1bBwBQ98MW38-3C02T2cAUbf0yP94VbJEKp0kcWI2VWVs_4U4vJm2_Zilxj6BDIFTH54uI8jBA&hash=93063c75042cb6076876c9d7b4540e409c6e71338454e9dcb93dfeb1'
