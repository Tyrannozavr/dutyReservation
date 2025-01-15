from typing import Optional, Any

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from models.pydantic.auth import UserOriginTypes

TELEGRAM_PREFIX = "tg_999_"


def generate_user_link(username: str, origin: UserOriginTypes):
    if origin is UserOriginTypes.telegram:
        return f"https://t.me/{username}"


class User(SQLModel, table=True):
    """internal username is for allow users to register directly from telegram and do not cause unique constraint with
    web registered users with their unique username"""
    id: int | None = Field(primary_key=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    internal_username: str = Field(unique=True)
    tg_data: Optional["TelegramUserData"] = Relationship(back_populates="user")
    duties: list["Duty"] = Relationship(back_populates="user")
    hashed_password: str | None = Field(default=None)
    origin: UserOriginTypes
    rooms: list["DutiesRoom"] = Relationship(back_populates="owner")

    @property
    def username(self):
        if self.is_from_telegram:
            return self.internal_username[len(TELEGRAM_PREFIX):]
        return self.internal_username

    @staticmethod
    def get_internal_username(username: str, origin: UserOriginTypes):
        if origin is UserOriginTypes.telegram:
            return TELEGRAM_PREFIX + username
        return username

    @property
    def link(self):
        if self.is_from_telegram:
            return generate_user_link(username=self.username, origin=UserOriginTypes.telegram)
        return ""

    @property
    def is_from_telegram(self):
        return self.internal_username.startswith(TELEGRAM_PREFIX)

    def model_dump(self, *args, **kwargs):
        # Call the original model_dump method to get all fields
        data = super().model_dump(*args, **kwargs)

        # Replace 'internal_username' with 'username'
        data['username'] = self.username

        # Optionally remove 'internal_username' if you don't want it in the output
        data.pop('internal_username', None)

        return data

    def __init__(self, **data: Any):
        if "username" in data:
            self.internal_username = data.get("username")
        super().__init__(**data)


class TelegramUserData(SQLModel, table=True):
    telegram_id: int = Field(primary_key=True)
    language_code: str | None = Field(default=None)
    allows_write_to_pm: bool | None = Field(default=None)
    photo_url: str | None = Field(default=None)

    user_id: int | None = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tg_data")

    model_config = ConfigDict(from_attributes=True)
