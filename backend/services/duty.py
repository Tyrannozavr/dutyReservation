import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from api.dependencies.database import SessionDep
from db.errors.duty import DutyOccupied
from db.queries.duty import DutyQueries
from models.pydantic.duty import DutyCreate, DutyChange


class DutiesServices:

    def __init__(self, db: SessionDep):
        self.queries = DutyQueries(db=db)
        self.db = db

    def get_all_duties_in_room(self, room_id: int):
        return self.queries.get_all_duties_in_room(room_id)

    def get_duty(self, duty_id):
        return self.queries.get_duty_by_id(duty_id)

    def create_duty(self, duty: DutyCreate):
        self.queries.create_duty(
            user_id=duty.user_id,
            room_id=duty.room_id,
            date=duty.date,
        )
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise DutyOccupied

    def update_duty(self, duty_id: int, duty_change: DutyChange):
        return self.queries.update_duty(duty_id=duty_id, duty_change=duty_change)

    def delete_duty(self, duty_id):
        return self.queries.delete_duty(duty_id)


