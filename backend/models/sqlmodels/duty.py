import datetime

from sqlmodel import SQLModel, Field, Relationship

from models.sqlmodels.auth import User


class Duty(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="duties")

    date: datetime.date = Field(default=None, unique=True)


