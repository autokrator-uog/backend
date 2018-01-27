import logging
import atexit
import sys

import click
import coloredlogs
from flask import Flask
from flask_sockets import Sockets

logger = logging.getLogger(__name__)


def bootstrap():
    logger.info("Bootstrapping app...")

    app = Flask(__name__)

    logger.info("Loading config...")
    app.config.from_object('config.default')

    # setup logging
    coloredlogs.install(level=logging.DEBUG)

    sockets = Sockets(app)

    @app.route('/')
    def hello_world():
        return 'This is BFAF'

    # register HTTP blueprints
    from endpoints.rest.init import init_blueprint
    app.register_blueprint(init_blueprint, url_prefix='/init')

    # register WebSockets blueprints
    from endpoints.websockets.updates import updates_blueprint
    sockets.register_blueprint(updates_blueprint, url_prefix='/updates')

    # set up background threads
    from endpoints.websockets.poller import NewInfoPollerThread
    app.poller_thread = NewInfoPollerThread(app)
    app.poller_thread.start()

    @atexit.register
    def close_poller_thread():
        app.poller_thread.exit = True

    return app


gunicorn_app = bootstrap()


@click.group()
@click.pass_context
def entrypoint(context):
    context.obj['app'] = gunicorn_app


@entrypoint.command()
@click.pass_context
def run(context):
    print("Running local dev server.")
    app = context.obj['app']

    app.config['DEBUG'] = True

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


@entrypoint.command()
def test():
    import pytest
    pytest.main(['test/'])


if __name__ == '__main__':
    entrypoint(obj={})
