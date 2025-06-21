import requests
from helpers import BASE_URL

class TestGetOrdersList:
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 200

        response_data = response.json()
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)