
import logging
from flask import Blueprint, request, current_app, jsonify

from services.exceptions import ServiceException
from services.userservice.client import UserServiceClient
from services.accountsservice.client import AccountsServiceClient
from services.accountsservice.exception import AccountsServiceException
from services.userservice.exception import UserNotFoundException

logger = logging.getLogger(__name__)
init_blueprint = Blueprint('init', __name__)


@init_blueprint.errorhandler(ServiceException)
def service_error(error):
    return jsonify({
        "message": "Error from a dependent service: {}".format(str(error))
    }), 500


@init_blueprint.route('')
def get_initial_details():
    user_name = request.args.get("user_name")

    if user_name is None:
        return "You must specify a user_name parameter", 400

    # start putting together the response JSON
    response = {
        "user_name": user_name,
        "accounts": []
    }

    # connect to the microservices
    user_service = UserServiceClient(current_app.config.get("USER_SERVICE_URL", "localhost"))
    accounts_service = AccountsServiceClient(current_app.config.get("ACCOUNTS_SERVICE_URL", "localhost"))

    # get all the users' money accounts
    try:
        accounts = user_service.get_accounts_for_user(user_name)
    except UserNotFoundException:
        return "User not found", 404

    for account in accounts:
        try:
            details = accounts_service.get_account_details(account)
            statement = accounts_service.get_account_statement(account)

            response['accounts'].append({
                'details': details,
                'statement': statement
            })
        except AccountsServiceException as exception:
            logger.error(exception)

    return jsonify(response)
