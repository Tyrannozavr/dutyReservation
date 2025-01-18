import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from db.errors.duty import DutyOccupied
from db.repositories.duty import DutyRepositories
from models.pydantic.duty import DutyCreate, DutyChange
from models.sqlmodels.auth import Duty


class DutiesServices:
    def __init__(self, db: Session):
        self.repositories = DutyRepositories(db=db)
        self.db = db

    async def get_all_duties_in_room(self, room_id: int):
        return await self.repositories.get_all_duties_in_room(room_id)

    async def get_all_duties(self):
        return await self.repositories.get_all_duties()

    async def set_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        duty = await self.repositories.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        return duty

    async def get_duty(self, duty_id):
        return await self.repositories.get_duty_by_id(duty_id)

    async def create_duty(self, duty: DutyCreate) -> Duty | None:
        try:
            new_duty = await self.repositories.create_duty(
                user_id=duty.user_id,
                room_id=duty.room_id,
                date=duty.date,
            )
            self.db.commit()
            return new_duty
        except IntegrityError:
            self.db.rollback()
            raise DutyOccupied("Duty already exists for this user in this room on this date.")

    async def update_duty(self, duty_id: int, duty_change: DutyChange):
        return await self.repositories.update_duty(duty_id=duty_id, duty_change=duty_change)

    async def delete_duty(self, duty_id):
        return await self.repositories.delete_duty(duty_id)
