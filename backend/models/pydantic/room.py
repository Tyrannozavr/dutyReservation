import datetime
import uuid

from pydantic import BaseModel, Field


class DutyCreate(BaseModel):
    duty_date: datetime.date = Field(description="Дата дежурства")
    name: str | None = Field(default=None, description="Наименование дежурства")



class RoomCreate(BaseModel):
    name: str | None = Field(description="Название голосования", default=None)
    is_multiple_selection: bool = Field(default=False,
                                        description="Может ли один человек выбрать несколько дежурств в один месяц")
    duty_list: list[DutyCreate] | None = Field(default=None, description="Дежурства, которые будут автоматически "
                                                                             "созданы при создании комнаты")


class RoomOwnerRead(BaseModel):
    id: int
    identifier: uuid.UUID
    is_multiple_selection: bool
    name: str

class RoomCommonRead(BaseModel):
    identifier: uuid.UUID
    is_multiple_selection: bool
    name: str



class RoomUpdateSettings(BaseModel):
    name: str | None = None
    is_multiple_selection: bool
    extra_duties: list[DutyCreate] | None = Field(default=None)