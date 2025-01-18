import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from api.errors.duty import UserAlreadyTookAllDuties
from db.errors.duty import DutyOccupied
from db.repositories.duty import DutyRepositories
from db.repositories.room import RoomRepositories
from models.pydantic.duty import DutyCreate, DutyChange
from models.sqlmodels.auth import Duty


class DutyServices:
    def __init__(self, db: Session):
        self.duty_repository = DutyRepositories(db=db)
        self.room_repository = RoomRepositories(db=db)
        self.db = db

    async def get_all_duties_in_room(self, room_id: int):
        return await self.duty_repository.get_all_duties_in_room(room_id)

    async def get_all_duties_with_users_in_the_room(self, room_id: int) -> list[Duty]:
        return await self.duty_repository.get_all_duties_with_users_in_the_room(room_id=room_id)

    async def get_all_free_duties_in_the_room(self, room_id: int) -> list[Duty]:
        return await self.duty_repository.get_all_free_duties_in_the_room(room_id=room_id)

    async def get_all_duties(self):
        return await self.duty_repository.get_all_duties()

    async def validate_user_can_reserve_duty(self, room_id: int, user_id: int):
        user_duties = await self.duty_repository.get_all_users_duty_in_the_room(user_id=user_id, room_id=room_id)
        room = await self.room_repository.get_room_by_id(room_id=room_id)
        if len(user_duties) > 0 and room.is_multiple_selection == False:
            raise UserAlreadyTookAllDuties

    async def set_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        await self.validate_user_can_reserve_duty(room_id=room_id, user_id=user_id)
        duty = await self.duty_repository.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        self.db.commit()
        return duty

    async def get_duty(self, duty_id):
        return await self.duty_repository.get_duty_by_id(duty_id)

    async def create_duty(self, duty: DutyCreate) -> Duty | None:
        try:
            new_duty = await self.duty_repository.create_duty(
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
        return await self.duty_repository.update_duty(duty_id=duty_id, duty_change=duty_change)

    async def delete_duty(self, duty_id):
        return await self.duty_repository.delete_duty(duty_id)
