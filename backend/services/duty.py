import datetime

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from api.errors.duty import UserAlreadyTookAllDuties, DutyDoesntExist, UserHasNoPermission, DutyIsAlreadyTaken, \
    DutyDoesntMatchRoom
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

    async def is_user_can_reserve_duty(self, room_id: int, user_id: int) -> bool:
        user_duties = await self.duty_repository.get_all_users_duty_in_the_room(user_id=user_id, room_id=room_id)
        room = await self.room_repository.get_room_by_id(room_id=room_id)
        if len(user_duties) > 0 and room.is_multiple_selection == False:
            return False
        else:
            return True

    async def change_duty_date(self, duty_id: int, user_id: int, date: datetime.date) -> Duty:
        duty = await self.get_duty(duty_id=duty_id)
        await self.validate_is_user_owner(duty=duty, user_id=user_id)
        new_duty = await self.duty_repository.get_free_duty_by_date(date=date)
        if new_duty:
            duty.user_id = None
            new_duty.user_id = user_id
            self.db.add(new_duty)
            self.db.add(duty)
            self.db.commit()
            self.db.refresh(new_duty)
            return new_duty
        else:
            raise DutyIsAlreadyTaken


    async def validate_user_can_reserve_duty(self, room_id: int, user_id: int):
        if not await self.is_user_can_reserve_duty(room_id=room_id, user_id=user_id):
            raise UserAlreadyTookAllDuties

    async def set_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        await self.validate_user_can_reserve_duty(room_id=room_id, user_id=user_id)
        duty = await self.duty_repository.set_duty_user_if_free(user_id=user_id, room_id=room_id, date=date)
        self.db.commit()
        return duty

    async def set_duty_user_by_duty_id(self, duty_id: int, user_id: int, room_id: int) -> Duty:
        await self.validate_user_can_reserve_duty(user_id=user_id, room_id=room_id)
        duty = await self.duty_repository.get_duty_by_id(duty_id=duty_id)
        if duty.room_id != room_id:
            raise DutyDoesntMatchRoom
        if duty.user_id is None:
            duty.user_id = user_id
        self.db.add(duty)
        try:
            self.db.commit()
            return duty

        except Exception as e:
            print(f"set duty by id error {e}")
            self.db.rollback()

    async def set_or_change_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty:
        if await self.is_user_can_reserve_duty(user_id=user_id, room_id=room_id):
            duty = await self.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        else:
            duties = await self.duty_repository.get_all_users_duty_in_the_room(user_id=user_id, room_id=room_id)
            last_duty = duties[-1]
            last_duty.user_id = None
            self.db.add(last_duty)
            duty = await self.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        try:
            self.db.commit()
            return duty
        except Exception as e:
            self.db.rollback()
            print("Error in set or change duty user ", e)

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


    async def is_user_owner(self, user_id: int, duty_id: int | None = None, duty: Duty | None = None) -> bool:
        if not duty and not duty_id:
            raise ValueError("Duty or duty_id must be provided")
        if duty is None:
            duty = await self.get_duty(duty_id=duty_id)
        return duty.user_id == user_id

    async def validate_is_user_owner(self, user_id: int, duty_id: int | None = None, duty: Duty | None = None):
        if not await self.is_user_owner(user_id=user_id, duty_id=duty_id, duty=duty):
            raise UserHasNoPermission

    async def delete_duty_from_user(self, duty_id: int, user_id: int):
        """Sets user in duty as None"""
        duty = await self.get_duty(duty_id=duty_id)
        if not duty:
            raise DutyDoesntExist
        await self.validate_is_user_owner(user_id=user_id, duty=duty)
        duty.user = None
        self.db.add(duty)
        self.db.commit()
        return duty
