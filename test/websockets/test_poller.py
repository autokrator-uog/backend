import pytest
from unittest.mock import patch

from endpoints.websockets.poller import NewInfoPollerThread


class TestPoller(object):
    @pytest.fixture()
    def patch_accounts_service_client(self):
        p = patch("endpoints.websockets.poller.AccountsServiceClient")
        yield p.start().return_value
        p.stop()

    @pytest.fixture()
    def patch_get_all_account_ids_to_update(self):
        p = patch("endpoints.websockets.poller.get_all_account_ids_to_update")
        yield p.start()
        p.stop()

    @pytest.fixture()
    def patch_get_socket_for_account_id(self):
        p = patch("endpoints.websockets.poller.get_socket_for_account_id")
        yield p.start()
        p.stop()

    @pytest.fixture()
    def poller_thread(self, flask_app, patch_accounts_service_client, patch_get_all_account_ids_to_update, patch_get_socket_for_account_id):
        return NewInfoPollerThread(flask_app)

    def test_poller_nothing_to_poll(self, poller_thread, patch_accounts_service_client, patch_get_all_account_ids_to_update, patch_get_socket_for_account_id):
        patch_get_all_account_ids_to_update.return_value = []

        poller_thread.poll()

        patch_accounts_service_client.get_account_statement.assert_not_called()
        patch_get_socket_for_account_id.assert_not_called()

    def test_poller_no_change(self, poller_thread, patch_accounts_service_client, patch_get_all_account_ids_to_update, patch_get_socket_for_account_id):
        patch_get_all_account_ids_to_update.return_value = [1]
        patch_accounts_service_client.get_account_statement.return_value = []

        # first poll, sets up
        poller_thread.poll()

        assert patch_get_all_account_ids_to_update.called
        patch_accounts_service_client.get_account_statement.assert_called_with(1)
        patch_get_socket_for_account_id.assert_not_called()

        # must reset the mocks
        patch_get_all_account_ids_to_update.reset_mock()
        patch_accounts_service_client.get_account_statement.reset_mock()
        patch_get_socket_for_account_id.reset_mock()

        # second poll, no change
        poller_thread.poll()

        assert patch_get_all_account_ids_to_update.called
        patch_accounts_service_client.get_account_statement.assert_called_with(1)
        patch_get_socket_for_account_id.assert_not_called()

    def test_poller_changed(self, poller_thread, patch_accounts_service_client, patch_get_all_account_ids_to_update, patch_get_socket_for_account_id):
        patch_get_all_account_ids_to_update.return_value = [1]
        patch_accounts_service_client.get_account_statement.return_value = []

        # first poll, sets up
        poller_thread.poll()

        assert patch_get_all_account_ids_to_update.called
        patch_accounts_service_client.get_account_statement.assert_called_with(1)
        patch_get_socket_for_account_id.assert_not_called()

        # must reset the mocks
        patch_get_all_account_ids_to_update.reset_mock()
        patch_accounts_service_client.get_account_statement.reset_mock()
        patch_get_socket_for_account_id.reset_mock()

        # set up the change
        patch_accounts_service_client.get_account_statement.return_value = [{"Amount": 1234}]

        # second poll, should detect change and fire a message on websockets
        poller_thread.poll()

        assert patch_get_all_account_ids_to_update.called
        patch_accounts_service_client.get_account_statement.assert_called_with(1)
        patch_get_socket_for_account_id.return_value.send.assert_called_with({
            "type": "new_statement_item",
            "data": {
                "Amount": 1234
            }
        })
