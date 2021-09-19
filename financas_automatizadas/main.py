from datetime import datetime
from pprint import pprint

from pynubank import Nubank

from financas_automatizadas import nubank
from financas_automatizadas import ynab


def main(nubank_client: Nubank = Nubank()) -> [dict]:
    created_account_transactions_in_ynab = sync_account(nubank_client)

    report_transactions(created_account_transactions_in_ynab)

    return created_account_transactions_in_ynab


def report_transactions(created_transaction_in_ynab):
    pprint("REPORT")
    pprint("Account transactions: ")
    pprint(f"{created_transaction_in_ynab}")


def sync_account(nubank_client):
    account_feed = nubank_client.get_account_feed()

    filtered_account_transactions = nubank.filter_account_transactions(
        account_feed=account_feed, threshold=datetime.now()
    )

    created_transaction_in_ynab = ynab.send_account_transaction(
        account_transactions=filtered_account_transactions
    )

    return created_transaction_in_ynab
