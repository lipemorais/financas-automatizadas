from datetime import datetime
from pprint import pprint

from pynubank import Nubank

from financas_automatizadas import nubank
from financas_automatizadas import ynab


def main(nubank_client: Nubank = Nubank()) -> [dict]:
    account_feed = nubank_client.get_account_feed()

    filtered_account_transactions = nubank.filter_account_transactions(
        account_feed=account_feed, threshold=datetime.now()
    )

    created_transaction_in_ynab = ynab.send_account_transaction(
        account_transactions=filtered_account_transactions
    )

    pprint("\n\n\n REPORT \n\n\n")
    pprint("Created transaction: ")
    pprint(f"{created_transaction_in_ynab}")

    return created_transaction_in_ynab
