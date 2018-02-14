import logging
import atexit
import sys
import os

import click
import coloredlogs
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sockets import Sockets

from services.exceptions import ServiceException

logger = logging.getLogger(__name__)


def bootstrap():
    # setup logging
    coloredlogs.install(level=logging.DEBUG)

    logger.info("Bootstrapping app...")

    app = Flask(__name__)
    cors = CORS(app, resources={"*": {"origins": "*"}}) # enable cross-origin resource sharing

    logger.info("Loading config...")
    app.config.from_object('config.default')
    
    if os.environ.get("ENV", "").upper() == "PROD":
        app.config.from_object('config.prod')

    sockets = Sockets(app)

    @app.route('/')
    def hello_world():
        return 'This is BFAF'

    @app.errorhandler(ServiceException)
    def service_error(error):
        return jsonify({
            "message": "Error from a dependent service: type={} {}"
                .format(error.__class__.__name__, str(error))
        }), 500

    # register HTTP blueprints
    from endpoints.rest.init import init_blueprint
    app.register_blueprint(init_blueprint, url_prefix='/init')

    # register WebSockets blueprints
    from endpoints.websockets.updates import updates_blueprint
    sockets.register_blueprint(updates_blueprint, url_prefix='/updates')

    # set up background thread
    @app.before_first_request
    def set_up_poller_thread():
        logger.info("Setting up poller thread...")

        from endpoints.websockets.poller import NewInfoPollerThread
        app.poller_thread = NewInfoPollerThread(app)
        app.poller_thread.start()

        @atexit.register
        def close_poller_thread():
            logger.warning("Exiting... cleaning up poller thread.")
            app.poller_thread.exit = True
            app.poller_thread.join(timeout=3000)
            logger.info("Poller thread cleaned up.")

        app.close_poller_thread = close_poller_thread

    return app


gunicorn_app = bootstrap()


@click.group()
@click.pass_context
def entrypoint(context):
    context.obj['app'] = gunicorn_app


@entrypoint.command()
@click.option('--port', default=5000, type=click.IntRange(0, 65535))
@click.pass_context
def run(context, port):
    logger.warning("Running local dev server on port %d", port)

    app = context.obj['app']
    app.config['DEBUG'] = True

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    import signal

    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)

    def stop(sig, frame):
        logger.warning("SIGINT received: stopping server")

        if server.started:
            server.stop()

        app.close_poller_thread()

        sys.exit(0)

    signal.signal(signal.SIGINT, stop)

    server.serve_forever()


@entrypoint.command()
def test():
    import pytest
    pytest.main(['test/'])


if __name__ == '__main__':
    entrypoint(obj={})
