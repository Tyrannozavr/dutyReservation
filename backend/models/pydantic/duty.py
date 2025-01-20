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


class DutiesWithUsersResponse(BaseModel):
    duties: list[DutyWithUser]

class FreeDutiesResponse(BaseModel):
    duties: list[FreeDuty]

class DutyData(BaseModel):
    duty_date: date

class DutyReserve(BaseModel):
    duty_id: int