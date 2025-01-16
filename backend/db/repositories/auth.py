from sqlmodel import Session, select

from models.pydantic.auth import TelegramUserData as TelegramUserDataPydantic, UserInDb, UserOriginTypes, UserDbCreate, \
    TelegramUserDataIn
from models.sqlmodels.auth import TelegramUserData as TelegramUserDataDb, User, TELEGRAM_PREFIX


class UserRepositoriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def get_or_create_tg_user(self, init_data: TelegramUserDataIn) -> TelegramUserDataDb:
        telegram_id = init_data.id
        user_tg_data = self.db.get(TelegramUserDataDb, telegram_id)
        if not user_tg_data:
            user_data_db_create = UserDbCreate(
                username=f"{TELEGRAM_PREFIX}{init_data.username}",
                first_name=init_data.first_name,
                last_name=init_data.last_name,
                origin=UserOriginTypes.telegram
            )
            user = await self.create_user(user_data_db_create)
            user_tg_data = TelegramUserDataDb(
                telegram_id=telegram_id,
                language_code=init_data.language_code,
                allows_write_to_pm=init_data.allows_write_to_pm,
                photo_url=init_data.photo_url,
                user=user
            )
            self.db.add(user_tg_data)
        return user_tg_data

    async def create_user(self, user_data: UserDbCreate) -> User:
        user_data = user_data.model_dump()
        user = User(**user_data)
        self.db.add(user)
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    async def get_user_by_internal_username(self, internal_username: str) -> User | None:
        stmt = select(User).where(User.internal_username == internal_username)
        user = self.db.exec(stmt).first()
        return user


class UserRepositories(UserRepositoriesMixin):
    pass

