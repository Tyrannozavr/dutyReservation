from datetime import timedelta

import pytest
from sqlmodel import create_engine, Session, SQLModel
from services.room import RoomServices
from services.duty import DutiesServices
from db.queries.room import RoomQueries  # Замените на ваш модуль
from models.sqlmodels.duty import DutiesRoom  # Замените на ваши модели
from models.sqlmodels.auth import *
from models.sqlmodels.duty import *

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
    return DutiesServices(db=test_db)

@pytest.mark.asyncio
async def test_create_room_integration(room_services, duty_services):
    name = "Integration Test Room"
    owner_id = 1
    year = 2023
    month = 10
    duties_per_day = 2

    # Вызов метода для создания комнаты
    result = await room_services.create_room(
        name=name,
        owner_id=owner_id,
        year=year,
        month=month,
        duties_per_day=duties_per_day
    )

    # Проверка, что комната была создана и сохранена в базе данных
    assert result.name == name
    assert result.owner_id == owner_id

    # Проверка, что комната действительно существует в базе данных
    rooms_in_db = await RoomQueries(room_services.db).get_rooms()  # Предполагается, что есть метод для получения всех комнат
    assert len(rooms_in_db) == 1
    assert rooms_in_db[0].name == name

    days_in_month = (datetime.date(year=year, month=month+1, day=1) - timedelta(days=1)).day
    expected_duties = days_in_month * duties_per_day

    duties = await duty_services.get_all_duties()
    print("expected_", len(duties))
    assert len(duties) == expected_duties







