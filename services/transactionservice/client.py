import json

from services.baseclient import ServiceClient
from services.transactionservice.exception import TransactionServiceException


class TransactionServiceClient(ServiceClient):
    def do_transaction_request(self, from_account_id, to_account_id, amount):
        payload = {
            'fromAccountId': from_account_id,
            'toAccountId': to_account_id,
            'amount': amount
        }

        response = self._session.post("{}/transaction/send".format(self.url), json.dumps(payload))

        if response.status_code != 200:
            raise TransactionServiceException("Error making transaction: {}".format(response.content))
