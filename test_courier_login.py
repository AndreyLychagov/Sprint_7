import pytest
from helpers import login_courier

class TestCourierLogin:
    def test_courier_login_success(self, setup_courier):
        login, password, _ = setup_courier
        response = login_courier(login, password)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("login,password", [
        ("", "valid_password"),
        ("valid_login", ""),
    ])
    def test_courier_login_missing_credentials(self, setup_courier, login, password):
        valid_login, valid_password, _ = setup_courier

        actual_login = valid_login if login == "valid_login" else login
        actual_password = valid_password if password == "valid_password" else password

        response = login_courier(actual_login, actual_password)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @pytest.mark.parametrize("login,password", [
        ("wrong_login", "valid_password"),
        ("valid_login", "wrong_password"),
    ])
    def test_courier_login_invalid_credentials(self, setup_courier, login, password):
        valid_login, valid_password, _ = setup_courier

        actual_login = valid_login if login == "valid_login" else login
        actual_password = valid_password if password == "valid_password" else password

        response = login_courier(actual_login, actual_password)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    def test_courier_login_nonexistent_user(self):
        response = login_courier("nonexistent_user", "password123")
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"