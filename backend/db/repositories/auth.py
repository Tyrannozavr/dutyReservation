from sqlmodel import Session, select

from models.pydantic.auth import UserDbCreate, \
    TelegramUserDataIn
from models.sqlmodels import User, TelegramUserData


class TelegramUserRepositoriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def create_tg_user(self, init_data: TelegramUserDataIn) -> TelegramUserData:
        user_tg = TelegramUserData(
            id=init_data.id,
            username=init_data.username,
            language_code=init_data.language_code,
            allows_write_to_pm=init_data.allows_write_to_pm,
            photo_url=init_data.photo_url
        )
        self.db.add(user_tg)
        return user_tg

    async def get_tg_user_by_id(self, telegram_id: int) -> TelegramUserData:
        stmt = select(TelegramUserData).where(TelegramUserData.id == telegram_id)
        user = self.db.exec(stmt)
        return user.first()

    async def get_tg_user_by_username(self, telegram_username: str) -> TelegramUserData | None:
        stmt = select(TelegramUserData).where(TelegramUserData.username == telegram_username)
        user = self.db.exec(stmt).first()
        return user


class UserRepositoriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user_data: UserDbCreate) -> User:
        user_data = user_data.model_dump()
        user = User(**user_data)
        self.db.add(user)
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = self.db.exec(stmt)
        return user.first()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = self.db.exec(stmt)
        return user.first()

    async def is_username_already_taken(self, username: str) -> bool:
        stmt = select(User).where(User.username == username)
        user = self.db.exec(stmt)
        return user.first() is not None

    async def get_all_users(self):
        stmt = select(User)
        users = self.db.exec(stmt)
        return users.all()


class UserRepositories(UserRepositoriesMixin, TelegramUserRepositoriesMixin):
    pass
