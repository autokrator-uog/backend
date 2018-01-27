import pytest


@pytest.fixture
def test_client(flask_app):
    return flask_app.test_client()
