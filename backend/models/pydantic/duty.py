from datetime import date

from pydantic import BaseModel

from models.pydantic.auth import UserRead


class DutyCreate(BaseModel):
    user_id: int
    room_id: int
    date: date


class DutyChange(BaseModel):
    date: date

class DutyWithUser(BaseModel):
    id: int
    user: UserRead | None = None
    date: date
    name: str | None

class FreeDuty(BaseModel):
    id: int
    date: date
    name: str | None

class DutyTaken(BaseModel):
    id: int
    date: date

class DutyRead(DutyTaken):
    name: str

class DutiesWithUsersResponse(BaseModel):
    duties: list[DutyWithUser]

class FreeDutiesResponse(BaseModel):
    duties: list[FreeDuty]

class DutyUpdate(BaseModel):
    date: date
    name: str

class DutyDate(BaseModel):
    duty_date: date
