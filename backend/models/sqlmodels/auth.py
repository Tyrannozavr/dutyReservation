from typing import Optional, Any

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from models.pydantic.auth import UserOriginTypes


def generate_user_link(username: str, origin: UserOriginTypes):
    if origin is UserOriginTypes.telegram:
        return f"https://t.me/{username}"


class User(SQLModel, table=True):
    """If the user came from telegram and this username is already taken it will be free until user set it explicitly"""
    id: int | None = Field(primary_key=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    username: str | None = Field(unique=True, nullable=True)
    tg_data: Optional["TelegramUserData"] = Relationship(back_populates="user")
    duties: list["Duty"] = Relationship(back_populates="user")
    hashed_password: str | None = Field(default=None)
    origin: UserOriginTypes
    rooms: list["DutiesRoom"] = Relationship(back_populates="owner")


    @property
    def link(self):
        if self.origin is UserOriginTypes.telegram:
            return generate_user_link(username=self.tg_data.telegram_username, origin=UserOriginTypes.telegram)
        return ""


class TelegramUserData(SQLModel, table=True):
    id: int = Field(primary_key=True, description="This is exactly telegram id")
    username: str = Field(index=True, description="This is telegram username")
    language_code: str | None = Field(default=None)
    allows_write_to_pm: bool | None = Field(default=None)
    photo_url: str | None = Field(default=None)

    user_id: int | None = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tg_data")

    model_config = ConfigDict(from_attributes=True)
