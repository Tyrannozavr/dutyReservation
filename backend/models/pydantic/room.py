import datetime
import uuid

from pydantic import BaseModel, Field




class RoomCreate(BaseModel):
    name: str | None = Field(description="Название голосования", default=None)
    is_multiple_selection: bool = Field(default=False,
                                        description="Может ли один человек выбрать несколько дежурств в один месяц")
    duty_dates: list[datetime.date] | None = Field(default=None, description="Даты дежурств, которые будут автоматически "
                                                                             "созданы при создании комнаты")


class RoomRead(BaseModel):
    id: int
    identifier: uuid.UUID
    is_multiple_selection: bool


class RoomUpdateSettings(BaseModel):
    name: str | None = None
    is_multiple_selection: bool
    extra_duties_dates: list[datetime.date] | None = Field(default=None, description="Duties to add to this room")