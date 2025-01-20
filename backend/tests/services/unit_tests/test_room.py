from unittest.mock import AsyncMock, MagicMock

import pytest

from db.repositories.room import RoomRepositories
from models.pydantic.room import RoomCreate
from services.room import RoomServices


@pytest.fixture(scope="function")
def mock_db():
    return MagicMock()


@pytest.fixture
def room_repositories_mock(mock_db):
    queries = RoomRepositories(mock_db)
    queries.create_room = AsyncMock()
    queries.create_duties_for_room = AsyncMock()
    return queries


@pytest.fixture
def room_services(room_repositories_mock, mock_db):
    return RoomServices(db=mock_db, repositories=room_repositories_mock)


@pytest.mark.asyncio
async def test_create_room(room_services, room_repositories_mock):
    name = "Test Room"
    owner_id = 1
    year = 2023
    month = 10
    duties_per_day = 1

    # Создаем мок комнаты
    mock_room = MagicMock()
    mock_room.id = 1
    room_repositories_mock.create_room.return_value = mock_room

    # Вызов метода
    room_data = RoomCreate(
        name=name,
    )
    result = await room_services.create_room(
        owner_id=owner_id,
        room_data=room_data
    )

    # Проверка, что методы были вызваны с правильными аргументами
    room_repositories_mock.create_room.assert_awaited_once_with(
        is_multiple_selection=False,
        name="Test Room",
        owner_id=1
    )

    # Проверка, что результат совпадает с ожидаемым
    assert result == mock_room
