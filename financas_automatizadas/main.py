from datetime import datetime
from pprint import pprint

from pynubank import Nubank

from financas_automatizadas import nubank
from financas_automatizadas import ynab
from financas_automatizadas.nubank import setup_nubank_client_authentication


def main(nubank_client: Nubank = Nubank()) -> [dict]:
    setup_nubank_client_authentication()
    created_account_transactions_in_ynab = sync_account(nubank_client)
    created_card_transactions_in_ynab = sync_card(nubank_client)

    report_transactions("Nu Conta", created_account_transactions_in_ynab)
    report_transactions("Cartão de crédito", created_card_transactions_in_ynab)

    return created_account_transactions_in_ynab + created_card_transactions_in_ynab


def report_transactions(account, created_transaction_in_ynab):
    pprint("REPORT")
    pprint(f"{account} transactions: ")
    pprint(f"{created_transaction_in_ynab}")


def sync_account(nubank_client: Nubank) -> [dict]:
    account_feed = nubank_client.get_account_feed()

    filtered_account_transactions = nubank.filter_account_transactions(
        account_feed=account_feed, threshold=datetime.now()
    )

    created_transactions_in_ynab = ynab.send_account_transaction(
        account_transactions=filtered_account_transactions
    )

    return created_transactions_in_ynab


def sync_card(nubank_client: Nubank) -> [dict]:
    card_feed = nubank_client.get_card_feed()

    filtered_card_transactions = nubank.filter_card_transactions(
        card_feed=card_feed, threshold=datetime.now()
    )

    created_transactions_in_ynab = ynab.send_card_transaction(
        card_transactions=filtered_card_transactions
    )

    return created_transactions_in_ynab
