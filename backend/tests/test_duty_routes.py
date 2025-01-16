# import pytest
# from fastapi.testclient import TestClient
# from main import app  # Adjust this import based on your project structure
# from models.sqlmodels.auth import User
# from models.sqlmodels.auth import Duty, DutiesRoom as Room
# from api.dependencies.auth import AuthorizedUserType
# from datetime import date
#
#
# @pytest.fixture
# def client():
#     with TestClient(app) as c:
#         yield c
#
#
# @pytest.fixture
# def test_user(db_session):  # Assuming you have a fixture to provide a database session
#     user = User(username="testuser", password="testpassword")  # Modify as per your user model
#     db_session.add(user)
#     db_session.commit()
#     return user
#
#
# @pytest.fixture
# def test_room(db_session):  # Assuming you have a fixture to provide a database session
#     room = Room(name="Test Room")  # Modify as per your room model
#     db_session.add(room)
#     db_session.commit()
#     return room
#
#
# def test_get_all_duties_in_room(client, test_room):
#     response = client.get(f"/{test_room.id}/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)  # Assuming it returns a list of duties
#
#
# def test_reserve_duty(client, test_user, test_room):
#     response = client.post(
#         f"/{test_room.id}/",
#         json={"date": str(date.today())},
#         headers={"Authorization": f"Bearer {test_user.token}"},  # Adjust this based on your auth mechanism
#     )
#     assert response.status_code == 201  # Assuming successful creation returns 201
#     assert response.json()["user_id"] == test_user.id
#
#
# def test_change_duty(client, test_user, test_room):
#     # First, create a duty to change
#     duty_response = client.post(
#         f"/{test_room.id}/",
#         json={"date": str(date.today())},
#         headers={"Authorization": f"Bearer {test_user.token}"},  # Adjust this based on your auth mechanism
#     )
#     duty_id = duty_response.json()["id"]
#
#     # Now change the duty
#     new_date = date.today().replace(day=date.today().day + 1)
#     response = client.put(
#         f"/{test_room.id}/{duty_id}",
#         json={"date": str(new_date)},
#         headers={"Authorization": f"Bearer {test_user.token}"},  # Adjust this based on your auth mechanism
#     )
#     assert response.status_code == 200
#     assert response.json()["date"] == str(new_date)
#
#
# def test_delete_duty(client, test_user, test_room):
#     # First, create a duty to delete
#     duty_response = client.post(
#         f"/{test_room.id}/",
#         json={"date": str(date.today())},
#         headers={"Authorization": f"Bearer {test_user.token}"},  # Adjust this based on your auth mechanism
#     )
#     duty_id = duty_response.json()["id"]
#
#     # Now delete the duty
#     response = client.delete(
#         f"/{test_room.id}/{duty_id}",
#         headers={"Authorization": f"Bearer {test_user.token}"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {"status": "success"}
