import datetime
import uuid

import pytz
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

from models.sqlmodels.auth import User


class DutiesRoom(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    identifier: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="rooms")
    month: int = Field(default_factory=lambda: datetime.datetime.now(pytz.timezone("UTC")).month)
    year: int = Field(default_factory=lambda: datetime.datetime.now(pytz.timezone("UTC")).year)
    is_multiple_selection: bool = Field(default=False)
    duties: list["Duty"] = Relationship(back_populates="room")


class Duty(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("room_id", "date", name="uq_date_room"),)
    id: int | None = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="duties")
    room_id: int = Field(foreign_key="dutiesroom.id")
    room: DutiesRoom = Relationship(back_populates="duties")

    date: datetime.date = Field(default=None)
