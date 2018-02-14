from services.baseclient import ServiceClient
from services.userservice.exception import UserServiceException, UserNotFoundException


class UserServiceClient(ServiceClient):

    def get_accounts_for_user(self, user_name):
        response = self._session.get("{}/user/{}".format(self.url, user_name))
        
        """
        Example response:
        {
            "accounts": [
                1,
                2,
                3
            ]
        }
        """

        if response.status_code == 200:
            json = response.json()
            return json.get('username', []) # TODO change to accounts once the thingy is done

        elif response.status_code == 404:
            raise UserNotFoundException("User {} not found!".format(user_name))

        else:
            raise UserServiceException("Error: body='{}'".format(response.content))
