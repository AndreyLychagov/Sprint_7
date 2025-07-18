import pytest
import requests
from helpers import BASE_URL, login_courier, generate_random_string


@pytest.fixture
def setup_courier():
    courier_data = register_new_courier_and_return_login_password()
    yield courier_data
    if courier_data:
        login, password, _ = courier_data
        response = login_courier(login, password)
        if response.status_code == 200:
            courier_id = response.json()["id"]
            requests.delete(f'{BASE_URL}/courier/{courier_id}')


def register_new_courier_and_return_login_password():

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/courier', data=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return None

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    import allure
    from allure_commons.types import AttachmentType
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        if 'response' in item.funcargs:
            response = item.funcargs['response']
            allure.attach(
                f"Request URL: {response.request.url}\n"
                f"Request Method: {response.request.method}\n"
                f"Request Body: {response.request.body}\n"
                f"Response Status Code: {response.status_code}\n"
                f"Response Body: {response.text}",
                name="API Request/Response",
                attachment_type=AttachmentType.TEXT
            )