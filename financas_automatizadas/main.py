from datetime import datetime, timedelta
from pprint import pprint

from dateutil.tz import tzutc
from pynubank import Nubank

from financas_automatizadas import nubank
from financas_automatizadas import ynab
from financas_automatizadas.nubank import setup_nubank_client_authentication


def main(nubank_client: Nubank = Nubank()) -> [dict]:
    setup_nubank_client_authentication(nubank_client=nubank_client)
    # created_account_transactions_in_ynab = sync_account(nubank_client)
    created_card_transactions_in_ynab = sync_card(nubank_client)

    # report_transactions("Nu Conta", created_account_transactions_in_ynab)
    report_transactions("Cartão de crédito", created_card_transactions_in_ynab)

    # return created_account_transactions_in_ynab + created_card_transactions_in_ynab
    return created_card_transactions_in_ynab


def report_transactions(account, created_transaction_in_ynab):
    pprint("REPORT")
    pprint(f"{account} transactions: ")
    pprint(f"{created_transaction_in_ynab}")


def sync_account(nubank_client: Nubank) -> [dict]:
    pprint("Sync Account starting")
    account_statements = nubank_client.get_account_statements()

    yesterday = datetime.now() - timedelta(days=1)
    filtered_account_transactions = nubank.filter_account_transactions(
        account_statements=account_statements, threshold=yesterday
    )

    created_transactions_in_ynab = ynab.send_account_transaction(
        account_transactions=filtered_account_transactions
    )

    pprint("Sync Account ending")
    return created_transactions_in_ynab


def sync_card(nubank_client: Nubank) -> [dict]:
    pprint("Sync Card starting")
    card_statements = nubank_client.get_card_statements()

    yesterday = datetime.now(tz=tzutc()) - timedelta(days=1)
    filtered_card_transactions = nubank.filter_card_transactions(
        card_statements=card_statements, threshold=yesterday
    )

    created_transactions_in_ynab = ynab.send_card_transaction(
        card_transactions=filtered_card_transactions
    )

    pprint("Sync Card ending")
    return created_transactions_in_ynab


if __name__ == "__main__":
    main(nubank_client=Nubank())
