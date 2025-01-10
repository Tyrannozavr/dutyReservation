from sqlmodel import Session

from models.pydantic.auth import TelegramInitData
from models.sqlmodels.auth import *


def get_or_create_user(init_data: TelegramInitData, db: Session):
    user_id = init_data.user.id
    user = db.get(TelegramUserData, user_id)
    return user

