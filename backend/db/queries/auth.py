from sqlmodel import Session, select

from models.pydantic.auth import TelegramUserData as TelegramUserDataPydantic, UserInDb, UserOriginTypes
from models.sqlmodels.auth import TelegramUserData as TelegramUserDataDb, User, TELEGRAM_PREFIX


def get_or_create_tg_user(init_data: TelegramUserDataPydantic, db: Session) -> TelegramUserDataDb:
    telegram_id = init_data.user.id
    user_tg_data = db.get(TelegramUserDataDb, telegram_id)
    if not user_tg_data:
        user_data = init_data.user.model_dump()
        user_data["username"] = f"{TELEGRAM_PREFIX}{user_data.get("username")}"
        telegram_id = user_data.pop("id")
        user = User(**user_data)
        init_data_dict = init_data.model_dump()
        init_data_dict["user"] = user
        user_tg_data = TelegramUserDataDb(**init_data_dict, telegram_id=telegram_id)
        db.add(user_tg_data)
        db.commit()
    return user_tg_data


def create_user(user_data: UserInDb, db: Session) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    return user

def get_user_by_id(user_id: int, db: Session) -> User:
    return db.get(User, user_id)

def get_user_by_username(username: str, db: Session) -> User:
    stmt = select(User).where(User.username == username)
    user = db.exec(stmt).first()
    return user