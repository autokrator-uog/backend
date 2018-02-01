from services.accountsservice.exception import AccountsServiceException, AccountNotFoundException
from services.baseclient import ServiceClient


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
            return response.json()
        elif response.status_code == 404:
            raise AccountNotFoundException("Account {} not found!".format(account_id))
        else:
            raise AccountsServiceException(
                "Error: status_code='{}' body='{}'".format(response.status_code, response.content))
