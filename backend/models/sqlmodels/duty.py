import datetime
import uuid

from sqlmodel import SQLModel, Field, Relationship

from models.sqlmodels.auth import User


class DutiesRoom(SQLModel, table=True):
    id: int = Field(primary_key=True)
    identifier: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="rooms")
    month: int = Field(default_factory=lambda: datetime.datetime.utcnow().month)
    year: int = Field(default_factory=lambda: datetime.datetime.utcnow().year)
    is_multiple_selection: bool = Field(default=False)
    duties: ["Duty"] = Relationship(back_populates="room")



class Duty(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="duties")
    room_id: int = Field(foreign_key="dutiesroom.id")
    room: DutiesRoom = Relationship(back_populates="duties")

    date: datetime.date = Field(default=None, unique=True)