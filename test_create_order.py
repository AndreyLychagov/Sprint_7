import pytest
from helpers import create_order

class TestCreateOrder:
    @pytest.mark.parametrize("color", [
        "BLACK",
        "GREY",
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_with_different_colors(self, color):
        response = create_order(color)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)