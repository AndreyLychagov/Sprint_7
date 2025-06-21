import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


def login_courier(login, password):
    return requests.post(
        f'{BASE_URL}/courier/login',
        data={"login": login, "password": password}
    )


def create_order(color=None):
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2025-06-30",
        "comment": "Saske, come back to Konoha"
    }

    if color:
        payload["color"] = [color] if isinstance(color, str) else color

    return requests.post(f'{BASE_URL}/orders', json=payload)

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))