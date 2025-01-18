import uuid

from pydantic import BaseModel, Field


class DateParam(BaseModel):
    month: int = Field(gt=0, lt=13, description="Месяц дежурств")
    year: int = Field(ge=0, description="Год месяца")


class RoomCreate(BaseModel):
    date: DateParam
    name: str = Field(description="Название голосования")
    duties_per_day: int = Field(gt=0, default=1, description="Дежурств в день")
    is_multiple_selection: bool = Field(default=False,
                                        description="Может ли один человек выбрать несколько дежурств в один месяц")


class RoomRead(BaseModel):
    id: int
    identifier: uuid.UUID
    is_multiple_selection: bool
    duties_per_day: int
    month: int
    year: int


class RoomUpdateSettings(BaseModel):
    is_multiple_selection: bool
    duties_per_day: int = Field(gt=0)
