from enum import Enum

from pydantic import BaseModel


class BaseUser(BaseModel):
    first_name: str
    last_name: str | None
    username: str | None

class UserInDb(BaseUser):
    id: int
    first_name: str
    last_name: str | None
    username: str | None

class UserOut(BaseUser):
    link: str | None

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

class TelegramUserDataIn(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    allows_write_to_pm: bool | None
    photo_url: str | None


class UserOriginsTypes(str, Enum):
    telegram = "telegram"
