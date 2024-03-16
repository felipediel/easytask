"""Test configuration."""
import pytest

from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient

from easytask import create_app
from easytask.core.database import db


@pytest.fixture()
def app() -> Flask:
    """Create app."""
    app = create_app(env="testing")
    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """Create client."""
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    """Create CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def database(app: Flask):
    """Initialize the test database."""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
