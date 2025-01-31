import datetime
import json
import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from api.errors.duty import UserAlreadyTookAllDuties, DutyDoesntExist, UserHasNoPermission, DutyIsAlreadyTaken, \
    DutyDoesntMatchRoom
from db.errors.duty import DutyOccupied
from db.repositories.duty import DutyRepositories
from db.repositories.room import RoomRepositories
from models.pydantic.auth import UserRead
from models.pydantic.duty import DutyCreate, DutyUpdate, DutiesWithUsersResponse, DutyWithUser
from models.sqlmodels import Duty


class DutyBase:
    def __init__(self, db: Session):
        self.duty_repository = DutyRepositories(db=db)
        self.room_repository = RoomRepositories(db=db)
        self.db = db


class DutyValidationMixin(DutyBase):
    async def is_user_can_reserve_duty(self, room_id: int, user_id: int) -> bool:
        user_duties = await self.duty_repository.get_all_users_duty_in_the_room(user_id=user_id, room_id=room_id)
        room = await self.room_repository.get_room_by_id(room_id=room_id)
        if len(user_duties) > 0 and room.is_multiple_selection == False:
            return False
        else:
            return True

    async def validate_user_can_reserve_duty(self, room_id: int, user_id: int):
        if not await self.is_user_can_reserve_duty(room_id=room_id, user_id=user_id):
            raise UserAlreadyTookAllDuties

    async def is_user_an_owner(self, user_id: int, duty_id: int | None = None, duty: Duty | None = None) -> bool:
        if not duty and not duty_id:
            raise ValueError("Duty or duty_id must be provided")
        if duty is None:
            duty = await self.duty_repository.get_duty_by_id(duty_id=duty_id)
        return duty.user_id == user_id

    async def is_user_a_creator(self, user_id: int, duty_id: int) -> bool:
        creator_id = await self.duty_repository.get_duty_creator_id(duty_id=duty_id)
        return creator_id == user_id

    async def validate_is_user_a_creator(self, user_id: int, duty_id: int):
        if not await self.is_user_a_creator(user_id=user_id, duty_id=duty_id):
            raise UserHasNoPermission

    async def validate_is_user_owner(self, user_id: int, duty_id: int | None = None, duty: Duty | None = None):
        if not await self.is_user_an_owner(user_id=user_id, duty_id=duty_id, duty=duty):
            raise UserHasNoPermission


class DutyManagementServices(DutyValidationMixin):
    async def commit_changes(self):
        try:
            self.db.commit()
        except Exception as e:
            logging.error(f"Error committing changes: {e}")
            self.db.rollback()
            raise e

    async def delete_duty_from_user(self, duty_id: int, user_id: int):
        """Sets user in duty as None"""
        duty = await self.get_duty(duty_id=duty_id)
        if not duty:
            raise DutyDoesntExist
        await self.validate_is_user_owner(user_id=user_id, duty=duty)
        duty.user = None
        self.db.add(duty)
        await self.commit_changes()
        return duty

    async def delete_duty(self, user_id: int, duty_id: int) -> Duty | None:
        await self.validate_is_user_a_creator(user_id=user_id, duty_id=duty_id)
        response = await self.duty_repository.delete_duty(duty_id=duty_id)
        await self.commit_changes()
        return response

    async def create_duty(self, duty: DutyCreate) -> Duty | None:
        new_duty = await self.duty_repository.create_duty(
            user_id=duty.user_id,
            room_id=duty.room_id,
            date=duty.date,
        )
        try:
            self.db.commit()
            return new_duty
        except IntegrityError:
            self.db.rollback()
            raise DutyOccupied("Duty already exists for this user in this room on this date.")
        except Exception as e:
            logging.error(f"Error committing changes: {e}")
            self.db.rollback()
            raise e

    async def update_duty(self, update_data: DutyUpdate, duty_id: int, user_id: int) -> Duty | None:
        await self.validate_is_user_a_creator(duty_id=duty_id, user_id=user_id)
        response = await self.duty_repository.update_duty(duty_id=duty_id, duty_change=update_data)
        await self.commit_changes()
        return response

    async def set_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        await self.validate_user_can_reserve_duty(room_id=room_id, user_id=user_id)
        duty = await self.duty_repository.set_duty_user_if_free(user_id=user_id, room_id=room_id, date=date)
        await self.commit_changes()
        return duty

    async def set_duty_user_by_duty_id(self, duty_id: int, user_id: int, room_id: int) -> Duty:
        """Sets given use_id as duty.user_id if user can reserve duty in given room and duty.user_id is still free"""
        await self.validate_user_can_reserve_duty(user_id=user_id, room_id=room_id)
        duty = await self.duty_repository.get_duty_by_id(duty_id=duty_id)
        if duty.room_id != room_id:
            raise DutyDoesntMatchRoom
        if duty.user_id is not None:
            raise DutyIsAlreadyTaken
        duty.user_id = user_id
        self.db.add(duty)
        await self.commit_changes()
        return duty

    async def set_or_change_duty_user(self, user_id: int, room_id: int, date: datetime.date) -> Duty | None:
        if await self.is_user_can_reserve_duty(user_id=user_id, room_id=room_id):
            duty = await self.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        else:
            duties = await self.duty_repository.get_all_users_duty_in_the_room(user_id=user_id, room_id=room_id)
            last_duty = duties[-1]
            last_duty.user_id = None
            self.db.add(last_duty)
            duty = await self.set_duty_user(user_id=user_id, room_id=room_id, date=date)
        await self.commit_changes()
        return duty

    async def get_duty(self, duty_id):
        return await self.duty_repository.get_duty_by_id(duty_id)

    async def reserve_another_duty(self, duty_id: int, user_id: int, date: datetime.date) -> Duty:
        duty = await self.get_duty(duty_id=duty_id)
        await self.validate_is_user_owner(duty=duty, user_id=user_id)
        new_duty = await self.duty_repository.get_free_duty_by_date(date=date)
        if new_duty:
            duty.user_id = None
            new_duty.user_id = user_id
            self.db.add(new_duty)
            self.db.add(duty)
            await self.commit_changes()
            self.db.refresh(new_duty)
            return new_duty
        else:
            raise DutyIsAlreadyTaken

    async def get_all_duties(self):
        return await self.duty_repository.get_all_duties()


class DutyRoomManagementServices(DutyValidationMixin):
    async def get_all_duties_in_room(self, room_id: int):
        return await self.duty_repository.get_all_duties_in_room(room_id)

    async def get_all_duties_with_users_in_the_room(self, room_id: int) -> list[Duty]:
        return await self.duty_repository.get_all_duties_with_users_in_the_room(room_id=room_id)

    async def get_all_duties_with_users_in_the_room_json(self, room_id: int) -> json:
        duties = await self.get_all_duties_with_users_in_the_room(room_id=room_id)
        duties_data = DutiesWithUsersResponse(duties=[
            DutyWithUser(
                **duty.model_dump(), user=UserRead(**duty.user.model_dump()))
            if duty.user else DutyWithUser(**duty.model_dump())
            for duty in duties
        ])
        duties_data_jsonable = jsonable_encoder(duties_data)
        duties_json = json.dumps(duties_data_jsonable)
        return duties_json

    async def get_all_free_duties_in_the_room(self, room_id: int) -> list[Duty]:
        return await self.duty_repository.get_all_free_duties_in_the_room(room_id=room_id)



class DutyServices(DutyManagementServices, DutyRoomManagementServices):
    pass
