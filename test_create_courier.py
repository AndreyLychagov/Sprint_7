import pytest
import requests
from helpers import BASE_URL, generate_random_string


class TestCreateCourier:
    def test_create_courier_success(self, setup_courier):
        courier_data = setup_courier
        assert len(courier_data) == 3

    def test_create_duplicate_courier(self, setup_courier):
        login, password, first_name = setup_courier

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{BASE_URL}/courier', data=payload)
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field, setup_courier):
        login, password, first_name = setup_courier

        data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        del data[missing_field]

        response = requests.post(f'{BASE_URL}/courier', data=data)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    def test_create_courier_success_response(self):

        data = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(f'{BASE_URL}/courier', data=data)

        assert response.status_code == 201
        assert response.json() == {"ok": True}