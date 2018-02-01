
import logging
from flask import Blueprint, request, current_app, jsonify

from services.transactionservice.client import TransactionServiceClient


logger = logging.getLogger(__name__)
transaction_blueprint = Blueprint('transaction', __name__)


@transaction_blueprint.route('/send', methods=['POST'])
def send_money():
    client = TransactionServiceClient(current_app.config.get("TRANSACTION_SERVICE_URL", "localhost"))

    client.do_transaction_request(
        request.form.get("from_account_id"),
        request.form.get("to_account_id"),
        request.form.get("account")
    )

    return jsonify({
        "status": "pending"
    }), 200


@transaction_blueprint.route('/deposit', methods=['POST'])
def deposit():
    raise NotImplementedError()


@transaction_blueprint.route('/withdrawal', methods=['POST'])
def withdrawal():
    raise NotImplementedError()
