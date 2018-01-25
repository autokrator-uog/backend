import requests

from services.accountsservice.exception import AccountsServiceException, AccountNotFoundException


class AccountsServiceClient:
    def __init__(self, url):
        self.url = url

        if not url.startswith('http'):
            self.url = 'http://' + url

        self._session = requests.Session()

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
