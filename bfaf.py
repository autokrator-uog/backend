import logging

import click
from flask import Flask
from flask_sockets import Sockets

logger = logging.getLogger(__name__)


def bootstrap():
    logger.info("Bootstrapping app...")

    app = Flask(__name__)
    sockets = Sockets(app)

    @app.route('/')
    def hello_world():
        return 'This is BFAF'

    # register HTTP blueprints
    from rest.init import init_blueprint
    app.register_blueprint(init_blueprint, url_prefix='/init')

    # register WebSockets blueprints
    # asdf

    logger.info("Loading config...")
    app.config.from_object('config.default')

    return app


@click.group()
@click.pass_context
def entrypoint(context):
    context.obj['app'] = bootstrap()


@entrypoint.command()
@click.pass_context
def run(context):
    print("Running local dev server.")
    app = context.obj['app']

    app.config['DEBUG'] = True
    app.run()


@entrypoint.command()
def test():
    import pytest
    pytest.main(['test/'])


if __name__ == '__main__':
    entrypoint(obj={})
