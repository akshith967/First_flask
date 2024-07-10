from Employee.models import Employees
import pytest
from unittest.mock import patch, MagicMock
@pytest.fixture()
def client():
    mock_client = MagicMock()
    print("setup")
    with patch('paho.mqtt.client.Client', return_value = mock_client):
        from app import app
        with app.test_client() as test_client:
            yield (test_client, mock_client)
            print("x")
    print("teardown")
@pytest.fixture(scope = "module")
def new_employee():
    return Employees(name="test",department = "IT")

