import datetime

from sqlalchemy import update
from sqlmodel import Session, select

from models.pydantic.duty import DutyChange
from models.sqlmodels.duty import Duty


class DutyQueriesMixin:
    def __init__(self, db: Session):
        self.db = db

    async def get_all_duties_in_room(self, room_id: int) -> list[Duty]:
        stmt = select(Duty).where(Duty.room_id == room_id)
        duties = self.db.exec(stmt).all()
        return duties

    async def get_duty_by_id(self, duty_id: int):
        """it works fine even if the session wasn't commit before retrieving this (delete for example)"""
        stmt = select(Duty).where(Duty.id == duty_id)
        duty = self.db.exec(stmt).first()
        return duty

    async def create_duty(self, room_id: int, date: datetime.date, user_id: int | None = None):
        duty = Duty(user_id=user_id, room_id=room_id, date=date)
        self.db.add(duty)
        return duty

    async def set_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        """allows to set user for date if it is still free and is not occupied by third db_session"""
        stmt = (select(Duty)
                  .where(Duty.room_id == room_id)
                  .where(Duty.date == date)
                  .where(Duty.user_id.is_(None))
                  .limit(1)
                  .with_for_update()
                  )
        record = self.db.exec(stmt).first()
        if record:
            update_stmt = (update(Duty)
                           .where(Duty.id == record.id)
                           .where(Duty.user_id.is_(None))
                           .values(user_id=user_id))
            self.db.exec(update_stmt)
            self.db.refresh(record)
            return record

    async def update_duty(self, duty_id, duty_change: DutyChange):
        duty_data = duty_change.model_dump(exclude_unset=True)
        db_duty = self.db.get(Duty, duty_id)
        db_duty.sqlmodel_update(duty_data)
        return db_duty

    async def delete_duty(self, duty_id: int | None = None, duty: Duty | None = None):
        if duty is None and duty_id is None:
            raise ValueError("Either duty or duty_id must be provided")
        if duty is None:
            duty = await self.get_duty_by_id(duty_id=duty_id)
        self.db.delete(duty)
        return duty

    async def get_duties_by_user_id(self, user_id: int):
        stmt = select(Duty).where(Duty.user_id == user_id)
        duties = self.db.exec(stmt).all()
        return duties

class DutyQueries(DutyQueriesMixin):
    pass


# duty_queries = Queries()
