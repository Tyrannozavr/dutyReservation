from sqlmodel import Session, select

from models.pydantic.auth import TelegramUserData as TelegramUserDataPydantic, UserInDb, UserOriginTypes, UserDbCreate, \
    TelegramUserDataIn
from models.sqlmodels.auth import TelegramUserData as TelegramUserDataDb, User, TELEGRAM_PREFIX


class UserQueriesMixin:
    @staticmethod
    def get_or_create_tg_user(init_data: TelegramUserDataIn, db: Session) -> TelegramUserDataDb:
        telegram_id = init_data.id
        user_tg_data = db.get(TelegramUserDataDb, telegram_id)
        if not user_tg_data:
            user_data_db_create = UserDbCreate(
                username=f"{TELEGRAM_PREFIX}{init_data.username}",
                first_name=init_data.first_name,
                last_name=init_data.last_name,
                origin=UserOriginTypes.telegram
            )
            user = user_queries.create_user(user_data_db_create, db)
            user_tg_data = TelegramUserDataDb(
                telegram_id=telegram_id,
                language_code=init_data.language_code,
                allows_write_to_pm=init_data.allows_write_to_pm,
                photo_url=init_data.photo_url,
                user=user
            )
            db.add(user_tg_data)
            # db.commit()
        return user_tg_data

    @staticmethod
    def create_user(user_data: UserDbCreate, db: Session) -> User:
        user_data = user_data.model_dump()
        user = User(**user_data)
        db.add(user)
        # db.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> User | None:
        return db.get(User, user_id)

    @staticmethod
    def get_user_by_internal_username(internal_username: str, db: Session) -> User | None:
        stmt = select(User).where(User.internal_username == internal_username)
        user = db.exec(stmt).first()
        return user

class Queries(UserQueriesMixin):
    pass

user_queries = Queries()