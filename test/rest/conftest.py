import pytest


@pytest.fixture
def flask_app():
    from bfaf import bootstrap
    return bootstrap()


@pytest.fixture
def test_client(flask_app):
    return flask_app.test_client()
