
import logging
import json

from flask import Blueprint


logger = logging.getLogger(__name__)
updates_blueprint = Blueprint('updates', __name__)


ACCOUNTID_TO_SOCKET_MAPPING = {}


def get_all_account_ids_to_update():
    global ACCOUNTID_TO_SOCKET_MAPPING
    return ACCOUNTID_TO_SOCKET_MAPPING.keys()


def get_socket_for_account_id(account_id):
    global ACCOUNTID_TO_SOCKET_MAPPING
    return ACCOUNTID_TO_SOCKET_MAPPING[account_id]


@updates_blueprint.route('/')
@updates_blueprint.route('')
def updates_ws(socket):
    logger.debug("New websocket connection...")

    connect_message = socket.receive()
    connect_message_json = json.loads(connect_message)

    logger.debug("Connect message received - {}".format(connect_message_json))

    account_ids = connect_message_json.get('account_ids', [])
    for account_id in account_ids:
        ACCOUNTID_TO_SOCKET_MAPPING[account_id] = socket

    while not socket.closed:
        socket.receive()
        continue

    logger.info("Connection exited...")

    for account_id in account_ids:
        del ACCOUNTID_TO_SOCKET_MAPPING[account_id]
