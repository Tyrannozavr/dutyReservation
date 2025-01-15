import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from db.errors.duty import DutyOccupied
from db.queries.duty import DutyQueries
from models.pydantic.duty import DutyCreate, DutyChange
from models.sqlmodels.duty import Duty


class DutiesServices:
    def __init__(self, db: Session):
        self.queries = DutyQueries(db=db)
        self.db = db

    def get_all_duties_in_room(self, room_id: int):
        return self.queries.get_all_duties_in_room(room_id)

    async def set_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        duty = await self.queries.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        return duty

    def get_duty(self, duty_id):
        return self.queries.get_duty_by_id(duty_id)

    async def create_duty(self, duty: DutyCreate) -> Duty | None:
        try:
            new_duty = await self.queries.create_duty(
                user_id=duty.user_id,
                room_id=duty.room_id,
                date=duty.date,
            )
            self.db.commit()
            return new_duty
        except IntegrityError:
            self.db.rollback()
            raise DutyOccupied("Duty already exists for this user in this room on this date.")

    def update_duty(self, duty_id: int, duty_change: DutyChange):
        return self.queries.update_duty(duty_id=duty_id, duty_change=duty_change)

    def delete_duty(self, duty_id):
        return self.queries.delete_duty(duty_id)


