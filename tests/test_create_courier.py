import allure
import pytest
import requests
from helpers import BASE_URL, generate_random_string

@allure.feature('Создание курьера')
class TestCreateCourier:
    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f'{BASE_URL}/courier', data=payload)
        assert response.status_code == 201

    @allure.title('Создание курьера с повторяющимся логином')
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

    @allure.title('Создание курьера с пропущенным полем')
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
