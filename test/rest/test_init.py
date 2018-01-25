import pytest
import json

from unittest.mock import patch

from services.userservice.exception import UserNotFoundException


class TestInit(object):
    @pytest.fixture()
    def patch_user_service_client(self):
        p = patch("rest.init.UserServiceClient")
        yield p.start().return_value
        p.stop()

    @pytest.fixture()
    def patch_accounts_service_client(self):
        p = patch("rest.init.AccountsServiceClient")
        yield p.start().return_value
        p.stop()

    def test_user_doesnt_exist(self, test_client, patch_user_service_client, patch_accounts_service_client):
        patch_user_service_client.get_accounts_for_user.side_effect = UserNotFoundException

        response = test_client.get('/init?user_name=John', follow_redirects=True)
        print(response.status_code)
        print(response.data)

        assert response.status_code == 404

    def test_user_exists_no_accounts(self, test_client, patch_user_service_client, patch_accounts_service_client):
        response = test_client.get('/init?user_name=John', follow_redirects=True)
        print(response.status_code)
        print(response.data)

        json_object = json.loads(response.data)
        print(json_object)

        assert json_object['user_name'] == 'John'
        assert json_object['accounts'] == []

    def test_user_exists_one_account(self, test_client, patch_user_service_client, patch_accounts_service_client):
        patch_user_service_client.get_accounts_for_user.return_value = [1]
        patch_accounts_service_client.get_account_details.return_value = {
            "balance": 100.0
        }
        patch_accounts_service_client.get_account_statement.return_value = []

        response = test_client.get('/init?user_name=John', follow_redirects=True)
        print(response.status_code)
        print(response.data)

        json_object = json.loads(response.data)
        print(json_object)

        assert json_object['user_name'] == 'John'
        assert len(json_object['accounts']) == 1
        assert json_object['accounts'][0]['details']['balance'] == 100.0
        assert json_object['accounts'][0]['statement'] == []

    def test_user_exists_multiple_accounts(self, test_client, patch_user_service_client, patch_accounts_service_client):
        patch_user_service_client.get_accounts_for_user.return_value = [1, 5, 66]
        patch_accounts_service_client.get_account_details.side_effect = [{"balance": 100.0}, {"balance": 120.0}, {"balance": 80.0}]
        patch_accounts_service_client.get_account_statement.side_effect = [[], [], []]

        response = test_client.get('/init?user_name=John', follow_redirects=True)
        print(response.status_code)
        print(response.data)

        json_object = json.loads(response.data)
        print(json_object)

        assert json_object['user_name'] == 'John'
        assert len(json_object['accounts']) == 3

        assert json_object['accounts'][0]['details']['balance'] == 100.0
        assert json_object['accounts'][1]['details']['balance'] == 120.0
        assert json_object['accounts'][2]['details']['balance'] == 80.0
