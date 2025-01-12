import datetime

from sqlmodel import Session, select

from models.sqlmodels.duty import Duty

HasNotPermissions = Exception("The user doesn't have enough permissions")

class DutyQueriesMixin:

    @staticmethod
    async def create_duty(request_user_id: int, date: datetime.date, db: Session):
        duty = Duty(user_id=request_user_id, date=date)
        db.add(duty)
        db.commit()
        db.refresh(duty)
        return duty

    @staticmethod
    async def change_duty(request_user_id: int, duty_id: int, db: Session, date: datetime.date):
        stmt = select(Duty).where(Duty.id == duty_id)
        duty = db.exec(stmt).first()
        if duty.user_id != request_user_id:
            raise HasNotPermissions
        duty.date = date
        db.add(duty)
        db.commit()
        db.refresh(duty)
        return duty

    @staticmethod
    async def delete_duty(request_user_id: int, duty_id: int, db: Session):
        stmt = select(Duty).where(Duty.id == duty_id)
        duty = db.exec(stmt).first()
        if duty.user_id != request_user_id:
            raise HasNotPermissions
        db.delete(duty)
        db.commit()

class Queries(DutyQueriesMixin):
    pass


queries = Queries()
