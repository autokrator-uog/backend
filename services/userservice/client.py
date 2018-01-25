import requests

from services.userservice.exception import UserServiceException, UserNotFoundException


class UserServiceClient:
    def __init__(self, url):
        self.url = url

        if not url.startswith('http'):
            self.url = 'http://' + url

        self._session = requests.Session()

    def get_accounts_for_user(self, user_name):
        response = self._session.get("{}/user/{}".format(self.url, user_name))

        if response.status_code == 200:
            json = response.json()
            return json.get('accounts', [])

        elif response.status_code == 404:
            raise UserNotFoundException("User {} not found!".format(user_name))

        else:
            raise UserServiceException("Error: body='{}'".format(response.content))
