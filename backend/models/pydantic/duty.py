from datetime import date

from pydantic import BaseModel, Field


class DutyCreate(BaseModel):
    user_id: int
    room_id: int
    date: date


class DutyChange(BaseModel):
    date: date


