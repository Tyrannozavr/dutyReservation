import datetime
import uuid
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from models.pydantic.types import UserOriginTypes


def generate_user_link(username: str, origin: UserOriginTypes):
    if origin is UserOriginTypes.telegram:
        return f"https://t.me/{username}"
    return ""


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

    model_config = ConfigDict(from_attributes=True)

    @property
    def link(self):
        if self.origin is UserOriginTypes.telegram:
            return generate_user_link(username=self.tg_data.username, origin=UserOriginTypes.telegram)
        return ""

    def model_dump(self, *args, **kwargs):
        result = super().model_dump(*args, **kwargs)
        result["link"] = self.link
        return result


class TelegramUserData(SQLModel, table=True):
    id: int = Field(primary_key=True, description="This is exactly telegram id")
    username: str = Field(index=True, description="This is telegram username")
    language_code: str | None = Field(default=None)
    allows_write_to_pm: bool | None = Field(default=None)
    photo_url: str | None = Field(default=None)

    user_id: int | None = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tg_data")

    model_config = ConfigDict(from_attributes=True)


class DutiesRoom(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(default="")
    identifier: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="rooms")
    is_multiple_selection: bool = Field(default=False)
    month: int = Field(gt=0, lt=13)
    year: int = Field(ge=0)
    duties_per_day: int = Field(default=1)
    duties: list["Duty"] = Relationship(back_populates="room", sa_relationship_kwargs={"cascade": "delete"})


class Duty(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    user_id: int | None = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="duties")
    room_id: int = Field(foreign_key="dutiesroom.id")
    room: DutiesRoom = Relationship(back_populates="duties")

    date: datetime.date = Field(default=None)
