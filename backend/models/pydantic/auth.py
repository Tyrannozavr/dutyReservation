from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.pydantic.types import UserOriginTypes


class BaseUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class UserInDb(BaseUser):
    id: int
    hashed_password: str | None = None
    origin: UserOriginTypes


class UserDbCreate(BaseUser):
    hashed_password: str | None = None
    origin: UserOriginTypes


class UserOut(BaseUser):
    link: str | None


class TelegramUserInitData(BaseModel):
    # Unique identifier for the telegram user
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class TelegramInitData(BaseModel):
    user: TelegramUserInitData
    chat_instance: int | None = None
    chat_type: str | None = None
    auth_date: int | None = None


class TelegramUserData(BaseModel):
    language_code: str | None
    allows_write_to_pm: bool | None
    photo_url: str | None
    user: UserInDb

    def __int__(self, **data):
        if "first_name" in data or "last_name" in data or "username" in data:
            self.user = UserInDb(**data)
        super().__init__(**data)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str  # here will be a id
    username: str | None = None
    exp: datetime | None = None
    first_name: str | None = None
    last_name: str | None = None
    origin: UserOriginTypes | None = None
    type: str = Field(default="access")

    @property
    def user_id(self):
        return int(self.sub)


class TelegramUserDataIn(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class TelegramUserDataCreate(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    allows_write_to_pm: bool | None
    photo_url: str | None
    user_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class UserDataIn(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    password: str


class UserDataCreate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
