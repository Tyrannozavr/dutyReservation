from sqlmodel import Session

from models.pydantic.auth import TelegramUserData as TelegramUserDataPydantic
from models.sqlmodels.auth import TelegramUserData as TelegramUserDataDb, User


def get_or_create_tg_user(init_data: TelegramUserDataPydantic, db: Session) -> TelegramUserDataDb:
    telegram_id = init_data.user.id
    user = db.get(TelegramUserDataDb, telegram_id)
    if not user:
        user_data = init_data.user.model_dump()
        telegram_id = user_data.pop("id")
        user = User(**user_data)
        init_data_dict = init_data.model_dump()
        init_data_dict["user"] = user
        user_tg_data = TelegramUserDataDb(**init_data_dict, telegram_id=telegram_id)
        db.add(user_tg_data)
        db.commit()
    return user

