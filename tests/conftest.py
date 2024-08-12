from Employee.models import Employees
from Projects.models import Projects
import pytest
from unittest.mock import patch, MagicMock
from db import db

@pytest.fixture()
def client():
    mock_client = MagicMock()
    with patch('paho.mqtt.client.Client',return_value=mock_client):
        from app import app
        with app.test_client() as test_client:
            yield test_client, mock_client
@pytest.fixture()
def new_employee():
    return Employees(name="test",department = "IT")

from flask import Flask
from pytest_mock_resources import create_mysql_fixture
from sqlalchemy.orm import scoped_session, sessionmaker


# Mocking the database
mysql = create_mysql_fixture(db.Model, session=None)

@pytest.fixture
def dbsession(mysql):
    Session = sessionmaker(bind=mysql)
    session = scoped_session(Session)
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def mock_app():
    mock_app = MagicMock(spec=Flask)
    yield mock_app

@pytest.fixture
def mock_logger():
    mock_logger = MagicMock()
    yield mock_logger

