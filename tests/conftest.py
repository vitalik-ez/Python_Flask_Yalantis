import flask
import pytest
import os
import tempfile

from main import app as flask_app, create_app, db, model


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(testing_config=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def model_object_detection():
    yield model


