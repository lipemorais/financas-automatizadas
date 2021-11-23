from datetime import datetime

from decouple import config
from pynubank import Nubank
from pynubank.utils.parsing import parse_pix_transaction



def setup_nubank_client_authentication():
    CPF = config("CPF")
    PASSWORD = config("PASSWORD")
    PATH_TO_CERTIFICATE = config("PATH_TO_CERTIFICATE")

    nubank_client = Nubank()
    nubank_client.authenticate_with_cert(CPF, PASSWORD, PATH_TO_CERTIFICATE)

    return nubank_client


def filter_account_transactions(account_feed: [dict], threshold: datetime) -> [dict]:
    filtered_account_transactions = [
        parse_pix_transaction(transaction)
        for transaction in account_feed
        if not datetime.fromisoformat(transaction["postDate"]) < threshold
    ]

    return filtered_account_transactions


def filter_card_transactions(card_feed: [dict], threshold: datetime):
    filtered_card_transactions = [
        transaction
        for transaction in card_feed
        if not parse_transaction_time(transaction["time"]) < threshold
    ]

    return filtered_card_transactions


def parse_transaction_time(transaction_time):
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    return datetime.strptime(transaction_time, datetime_format)
