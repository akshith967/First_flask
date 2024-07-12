from Employee.models import Employees
from Projects.models import Projects
import pytest
from unittest.mock import patch, MagicMock
from db import db
import pytest

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
    mock_client.reset_mock()
@pytest.fixture(scope = "module")
def new_employee():
    return Employees(name="test",department = "IT")

from flask import Flask
from pytest_mock_resources import create_mysql_fixture
mysql = create_mysql_fixture(db.Model, session=True)
@pytest.fixture
def dbsession(mysql):
    session = mysql
    yield session


@pytest.fixture
def mock_app(dbsession):
    # Configure the mock app's config attribute
    mock_app = MagicMock(spec=Flask)
    # engine = dbsession.bind
    # mock_app.config = {
    #     'SQLALCHEMY_DATABASE_URI': str(engine.url),
    #     'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    # }
    # from flask_sqlalchemy_session import flask_scoped_session
    #
    # session = flask_scoped_session(dbsession, mock_app)

    yield mock_app
