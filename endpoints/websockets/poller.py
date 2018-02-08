from threading import Thread
import time
import logging

from endpoints.websockets.updates import get_all_account_ids_to_update, get_socket_for_account_id
from services.accountsservice.client import AccountsServiceClient


logger = logging.getLogger(__name__)


class NewInfoPollerThread(Thread):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exit = False
        self.prev_statements = {}

        self.accounts_service = AccountsServiceClient(app.config.get("ACCOUNTS_SERVICE_URL"))

    def poll(self):
        account_ids = get_all_account_ids_to_update()
        if len(account_ids) == 0:
            logger.debug("Would poll, but there's no accounts set to poll. Skip...")
            return

        logger.debug("Polling...")

        for account_id in account_ids:
            new_stmt = self.accounts_service.get_account_statement(account_id)

            if self.prev_statements.get(account_id) is None:
                logger.debug("New account_id to poll for: {}".format(account_id))
                self.prev_statements[account_id] = new_stmt
            else:
                prev = self.prev_statements.get(account_id)
                if prev != new_stmt:
                    new_entries = []

                    for entry in new_stmt:
                        if entry not in prev:
                            new_entries.append(entry)

                    socket = get_socket_for_account_id(account_id)
                    for entry in new_entries:
                        socket.send({
                            "update_type": "new_statement_item",
                            "for_account_id": account_id,
                            "data": entry
                        })
                else:
                    logger.debug("No change in account {}".format(account_id))

                self.prev_statements[account_id] = new_stmt

    def run(self):
        while not self.exit:
            self.poll()
            time.sleep(1)
