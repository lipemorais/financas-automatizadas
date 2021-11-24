from datetime import datetime

from dateutil.parser import isoparse
from decouple import config
from pynubank.utils.parsing import parse_pix_transaction



def setup_nubank_client_authentication(nubank_client):
    CPF = config("CPF")
    PASSWORD = config("PASSWORD")
    PATH_TO_CERTIFICATE = config("PATH_TO_CERTIFICATE")

    nubank_client.authenticate_with_cert(CPF, PASSWORD, PATH_TO_CERTIFICATE)

    return nubank_client


def filter_account_transactions(account_feed: [dict], threshold: datetime) -> [dict]:
    filtered_account_transactions = [
        parse_pix_transaction(transaction)
        for transaction in account_feed
        if threshold <= datetime.fromisoformat(transaction["postDate"])
    ]

    return filtered_account_transactions


def filter_card_transactions(card_feed: [dict], threshold: datetime):
    filtered_card_transactions = [
        transaction
        for transaction in card_feed
        if threshold < isoparse(transaction["time"])
    ]

    return filtered_card_transactions
