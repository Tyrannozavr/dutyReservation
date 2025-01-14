import datetime
from sqlalchemy.exc import IntegrityError

import pytest
from unittest.mock import AsyncMock, MagicMock
from db.errors.duty import DutyOccupied
from models.pydantic.duty import DutyCreate, DutyChange
from services.duty import DutiesServices


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def duty_queries_mock(mock_db_session):
    return AsyncMock()


@pytest.fixture
def duties_services(mock_db_session, duty_queries_mock):
    # Create an instance of DutiesServices with the mocked dependencies
    services = DutiesServices(db=mock_db_session)
    services.queries = duty_queries_mock  # Inject the mock queries
    return services


@pytest.mark.asyncio
async def test_get_all_duties_in_room(duties_services, duty_queries_mock):
    room_id = 1
    expected_duties = []  # Example expected result

    # Set up the mock to return the expected duties
    duty_queries_mock.get_all_duties_in_room.return_value = expected_duties

    # Call the service method
    result = await duties_services.get_all_duties_in_room(room_id)

    # Assert that the mock was called once with the correct argument
    duty_queries_mock.get_all_duties_in_room.assert_awaited_once_with(room_id)

    # Assert that the result is as expected
    assert result == expected_duties


@pytest.mark.asyncio
async def test_create_duty(duties_services, mock_db_session):
    duty_data = DutyCreate(user_id=1, room_id=1, date=datetime.date.today())

    # Mock the create_duty method
    duties_services.queries.create_duty = AsyncMock(return_value=None)

    # Call the service method
    await duties_services.create_duty(duty_data)

    # Assert that create_duty was called with correct parameters
    duties_services.queries.create_duty.assert_awaited_once_with(
        user_id=duty_data.user_id,
        room_id=duty_data.room_id,
        date=duty_data.date,
    )



@pytest.mark.asyncio
async def test_create_duty_integrity_error(duties_services, mock_db_session):
    duty_data = DutyCreate(user_id=1, room_id=1, date=datetime.date.today())

    # Mock the create_duty method to raise IntegrityError
    duties_services.queries.create_duty = AsyncMock(side_effect=IntegrityError("", "", ""))

    # Check that the DutyOccupied exception is raised when creating a duty
    with pytest.raises(DutyOccupied):
        await duties_services.create_duty(duty_data)

@pytest.mark.asyncio
async def test_update_duty(duties_services, duty_queries_mock):
    duty_id = 1
    duty_change = DutyChange(user_id=1, room_id=1, date=datetime.date.today())

    # Mock the update_duty method
    duty_queries_mock.update_duty.return_value = None

    # Call the service method
    await duties_services.update_duty(duty_id, duty_change)

    # Assert that update_duty was called with correct parameters
    duty_queries_mock.update_duty.assert_awaited_once_with(duty_id=duty_id, duty_change=duty_change)


@pytest.mark.asyncio
async def test_delete_duty(duties_services, duty_queries_mock):
    duty_id = 1

    # Mock the delete_duty method
    duty_queries_mock.delete_duty.return_value = None

    # Call the service method
    await duties_services.delete_duty(duty_id)

    # Assert that delete_duty was called with the correct parameter
    duty_queries_mock.delete_duty.assert_awaited_once_with(duty_id)

