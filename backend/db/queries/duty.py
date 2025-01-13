import datetime

from sqlmodel import Session, select

from models.sqlmodels.duty import Duty


class DutyQueriesMixin:

    @staticmethod
    async def get_all_duties_in_room(room_id: int, db: Session):
        stmt = select(Duty).where(Duty.room_id == room_id)
        duties = db.exec(stmt).all()
        return duties

    @staticmethod
    async def get_duty_by_id(duty_id: int, db: Session):
        stmt = select(Duty).where(Duty.id == duty_id)
        duty = db.exec(stmt).first()
        return duty

    @staticmethod
    async def create_duty(user_id: int, room_id: int, date: datetime.date, db: Session):
        duty = Duty(user_id=user_id, room_id=room_id, date=date)
        db.add(duty)
        # db.commit()
        # db.refresh(duty)
        return duty

    @staticmethod
    async def change_duty_date(db: Session, date: datetime.date, duty_id: int | None = None, duty: Duty | None = None):
        """duty or duty_id must be provided"""
        if duty is None and duty_id is None:
            raise ValueError("Either duty or duty_id must be provided")
        if duty is None:
            duty = await DutyQueriesMixin.get_duty_by_id(duty_id=duty_id, db=db)
        duty.date = date
        db.add(duty)
        db.commit()
        db.refresh(duty)
        return duty

    @staticmethod
    async def delete_duty(db: Session, duty_id: int | None = None, duty: Duty | None = None):
        if duty is None and duty_id is None:
            raise ValueError("Either duty or duty_id must be provided")
        if duty is None:
            duty = await DutyQueriesMixin.get_duty_by_id(duty_id=duty_id, db=db)
        db.delete(duty)
        # db.commit()


class Queries(DutyQueriesMixin):
    pass


duty_queries = Queries()
