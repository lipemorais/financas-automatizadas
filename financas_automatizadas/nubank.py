from datetime import datetime

from decouple import config
from pynubank import Nubank
from pynubank.utils.parsing import parse_pix_transaction

CPF = config("CPF")
PASSWORD = config("PASSWORD")
PATH_TO_CERTIFICATE = config("PATH_TO_CERTIFICATE")

nu = Nubank()
# nu.authenticate_with_cert(CPF, PASSWORD, PATH_TO_CERTIFICATE)


def filter_account_transactions(account_feed: [dict]) -> [dict]:
    threshold = datetime.now()

    filtered_account_transactions = [
        parse_pix_transaction(transaction)
        for transaction in account_feed
        if not datetime.fromisoformat(transaction["postDate"]) < threshold
    ]

    return filtered_account_transactions


def send_account_transactions_to_ynab():
    return None
