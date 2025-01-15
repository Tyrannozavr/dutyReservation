from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserOriginTypes(str, Enum):
    telegram = "telegram"
    web = "web"


class BaseUser(BaseModel):
    first_name: str | None
    last_name: str | None
    username: str


class UserInDb(BaseUser):
    id: int
    hashed_password: str | None = None
    origin: UserOriginTypes


class UserDbCreate(BaseUser):
    hashed_password: str | None = None
    origin: UserOriginTypes


class UserOut(BaseUser):
    link: str | None

class TelegramInitData(BaseModel):
    # Unique identifier for the telegram user
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None




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
    id: int
    username: str
    exp: datetime | None = None
    first_name: str | None = None
    last_name: str | None = None
    origin: UserOriginTypes


class TelegramUserDataIn(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    allows_write_to_pm: bool | None
    photo_url: str | None


class UserDataIn(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    password: str
