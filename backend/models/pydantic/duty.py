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

class FreeDuty(BaseModel):
    id: int
    date: date

class DutiesWithUsersResponse(BaseModel):
    duties: list[DutyWithUser]

class FreeDutiesResponse(BaseModel):
    duties: list[FreeDuty]