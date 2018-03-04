import logging
import json

from services.accountsservice.exception import AccountsServiceException, AccountNotFoundException
from services.baseclient import ServiceClient

logger = logging.getLogger(__name__)


class AccountsServiceClient(ServiceClient):

    def get_account_details(self, account_id):
        response = self._session.get("{}/account/{}".format(self.url, account_id))

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise AccountNotFoundException("Account {} not found!".format(account_id))
        else:
            raise AccountsServiceException("Error: status_code='{}' body='{}'".format(response.status_code, response.content))

    def get_account_statement(self, account_id):
        response = self._session.get("{}/account/{}/statement".format(self.url, account_id))

        if response.status_code == 200:
            return response.json().get('statements', [])
        elif response.status_code == 404:
            raise AccountNotFoundException("Account {} not found!".format(account_id))
        else:
            raise AccountsServiceException("Accounts Service Error: status={} body='{}'"
                    .format(response.status_code, response.content))
        
    def do_account_deposit(self, to_account_id, amount):
        payload = {
            'amount': amount
        }
        logger.debug("Sending /account/{}/deposit request: {}".format(to_account_id, json.dumps(payload)))
        
        response = self._session.post("{}/account/{}/deposit".format(self.url, to_account_id), json.dumps(payload))

        if not response.ok:
            raise AccountsServiceException("Accounts Service Error: status={} body='{}'"
                    .format(response.status_code, response.content))
            
    def do_account_withdraw(self, from_account_id, amount):
        payload = {
            'amount': amount
        }
        logger.debug("Sending /account/{}/withdrawal request: {}".format(from_account_id, json.dumps(payload)))
        
        response = self._session.post("{}/account/{}/withdrawal".format(self.url, from_account_id),json.dumps(payload))

        if not response.ok:
            raise AccountsServiceException("Accounts Service Error: status={} body='{}'"
                    .format(response.status_code, response.content))
