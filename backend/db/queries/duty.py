import datetime

from sqlmodel import Session

from models.sqlmodels.duty import Duty


def add_duty(user_id: int, date: datetime.date, db: Session):
    duty = Duty(user_id=user_id, date=date)
    db.add(duty)
    db.commit()
    db.refresh(duty)
    return duty