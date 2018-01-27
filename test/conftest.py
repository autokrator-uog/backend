import pytest


@pytest.fixture
def flask_app():
    import bfaf

    yield bfaf.gunicorn_app

    bfaf.gunicorn_app.close_poller_thread()
