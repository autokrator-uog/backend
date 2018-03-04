
import logging
from flask import Blueprint, request, current_app, jsonify

from services.transactionservice.client import TransactionServiceClient
from services.accountsservice.client import AccountsServiceClient


logger = logging.getLogger(__name__)
transaction_blueprint = Blueprint('transaction', __name__)


@transaction_blueprint.route('/send', methods=['POST'])
def send_money():
    client = TransactionServiceClient(current_app.config.get("TRANSACTION_SERVICE_URL", "localhost"))
    data = request.get_json()

    client.do_transaction_request(
        data.get("from_account_id"),
        data.get("to_account_id"),
        data.get("amount")
    )

    return jsonify({
        "status": "pending"
    }), 200


@transaction_blueprint.route('/deposit', methods=['POST'])
def deposit():
    client = AccountsServiceClient(current_app.config.get("ACCOUNTS_SERVICE_URL", "localhost"))
    data = request.get_json()

    client.do_account_deposit(
        data.get("toAccount"),
        data.get("amount")
    )

    return jsonify({
        "status": "pending"
    }), 200


@transaction_blueprint.route('/withdrawal', methods=['POST'])
def withdrawal():
    client = AccountsServiceClient(current_app.config.get("ACCOUNTS_SERVICE_URL", "localhost"))
    data = request.get_json()

    client.do_account_withdraw(
        data.get("fromAccount"),
        data.get("amount")
    )

    return jsonify({
        "status": "pending"
    }), 200
