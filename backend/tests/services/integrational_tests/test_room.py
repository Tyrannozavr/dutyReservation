from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from sqlmodel import create_engine, Session

from api.errors.duty import UserHasNoPermission
from db.repositories.room import RoomRepositories
from models.pydantic.room import RoomUpdateSettings, RoomCreate
from models.sqlmodels import *
from services.duty import DutyServices
from services.room import RoomServices


@pytest.fixture(scope="module")
def test_db():
    # Создание базы данных в памяти
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)  # Создание таблиц

    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def room_services(test_db):
    return RoomServices(db=test_db)


@pytest.fixture(scope="function")
def duty_services(test_db):
    return DutyServices(db=test_db)


@pytest.mark.asyncio
async def test_create_room_integration(room_services, duty_services):
    name = "Integration Test Room"
    owner_id = 1
    year = 2023
    month = 10
    duties_per_day = 2

    # Вызов метода для создания комнаты
    room_data = RoomCreate(
        name=name,
    )
    result = await room_services.create_room(
        owner_id=owner_id,
        room_data=room_data
    )

    # Проверка, что комната была создана и сохранена в базе данных
    assert result.name == name
    assert result.owner_id == owner_id

    # Проверка, что комната действительно существует в базе данных
    rooms_in_db = await RoomRepositories(
        room_services.db).get_rooms()  # Предполагается, что есть метод для получения всех комнат
    assert len(rooms_in_db) == 1
    assert rooms_in_db[0].name == name

    days_in_month = (datetime.date(year=year, month=month + 1, day=1) - timedelta(days=1)).day


@pytest.mark.asyncio
async def test_create_room_with_invalid_data(room_services):
    # Arrange
    name = ""
    owner_id = 1
    is_multiple_selection = True

    # Act & Assert
    with pytest.raises(ValueError):
        room_data = RoomCreate(
            name=name,
            is_multiple_selection=12
        )
        await room_services.create_room(
            owner_id=owner_id,
            room_data=room_data
        )


@pytest.mark.asyncio
async def test_get_room_by_identifier_not_found(room_services):
    # Arrange
    identifier = uuid.uuid4()
    # Act & Assert
    with pytest.raises(Exception, match="Room not found"):
        await room_services.get_room_by_identifier(identifier)


#
@pytest.mark.asyncio
async def test_delete_room_not_found(room_services):
    # Arrange
    user_id = 1
    room_id = 999  # Non-existent room ID
    # Act & Assert
    with pytest.raises(Exception, match="Room not found"):
        await room_services.delete_room(user_id, room_id)


@pytest.mark.asyncio
async def test_update_room(room_services):
    # Arrange
    user_id = 1

    name = "Hello, world"
    room_data = RoomCreate(
        name=name,
        is_multiple_selection=False
    )
    room = await room_services.create_room(
        owner_id=user_id,
        room_data=room_data
    )
    update_data = RoomUpdateSettings(is_multiple_selection=True, name="New name")
    room = await room_services.update_room(room_id=room.id, user_id=user_id, update_data=update_data)
    assert room.is_multiple_selection == True
    assert room.name == "New name"


@pytest.mark.asyncio
async def test_update_room_invalid_data(room_services):
    user_id = 1
    name = "Hello, world"
    room_data = RoomCreate(
        name=name,
        is_multiple_selection=False
    )
    room = await room_services.create_room(
        owner_id=user_id,
        room_data=room_data
    )

    # Act & Assert
    with pytest.raises(ValueError):
        update_data = RoomUpdateSettings(is_multiple_selection=45)
        await room_services.update_room(user_id, room.id, update_data)


@pytest.mark.asyncio
async def test_update_room_invalid_user(room_services):
    user_id = 1
    name = "Hello, world"
    room_data = RoomCreate(
        name=name,
        is_multiple_selection=False
    )
    room = await room_services.create_room(
        owner_id=user_id,
        room_data=room_data
    )

    # Act & Assert
    with pytest.raises(UserHasNoPermission):
        update_data = RoomUpdateSettings(is_multiple_selection=True)  # Invalid value
        await room_services.update_room(user_id + 1, room.id, update_data)


@pytest.mark.asyncio
async def test_validate_is_user_owner_for_non_existent_room(room_services):
    # Arrange
    room_id = 999  # Non-existent room ID
    user_id = 1
    room_services.room_repositories.get_room_by_id = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(Exception, match="Room not found"):
        await room_services.validate_is_user_owner(room_id, user_id)
