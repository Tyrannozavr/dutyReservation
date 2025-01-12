import datetime

from sqlmodel import SQLModel, Field, Relationship

from models.sqlmodels.auth import User


class Duty(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="duties")

    date: datetime.date = Field(default=None, unique=True)


class DutyModes(SQLModel, table=True):
    id: int = Field(primary_key=True)
    duty_month: int = Field(default_factory=lambda: datetime.datetime.utcnow().month)
    is_multiple_selection: bool = Field(default=False)