import json
import logging

from services.baseclient import ServiceClient
from services.transactionservice.exception import TransactionServiceException

logger = logging.getLogger(__name__)


class TransactionServiceClient(ServiceClient):
    def do_transaction_request(self, from_account_id, to_account_id, amount):
        payload = {
            'fromAccountId': from_account_id,
            'toAccountId': to_account_id,
            'amount': amount
        }
        logger.debug("Sending /createTransaction request: {}".format(json.dumps(payload)))
        
        response = self._session.post("{}/createTransaction".format(self.url), json.dumps(payload))

        if not response.ok:
            raise TransactionServiceException("Error making transaction: {}".format(response.content))
