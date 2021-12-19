import base64
from datetime import datetime

from dateutil.parser import isoparse
from decouple import config
from pynubank.utils.parsing import parse_pix_transaction


def setup_nubank_certificate(NUBANK_CERTIFICATE: str) -> None:
    with open("cert.p12", "wb") as certificate_file:
        certificate_content = base64.b64decode(NUBANK_CERTIFICATE)
        certificate_file.write(certificate_content)


def setup_nubank_client_authentication(nubank_client):
    CPF = config("CPF")
    PASSWORD = config("PASSWORD")
    NUBANK_CERTIFICATE = config("NUBANK_CERTIFICATE")
    PATH_TO_CERTIFICATE = config("PATH_TO_CERTIFICATE")
    setup_nubank_certificate(NUBANK_CERTIFICATE)

    nubank_client.authenticate_with_cert(CPF, PASSWORD, PATH_TO_CERTIFICATE)

    return nubank_client


def filter_account_transactions(
    account_statements: [dict], threshold: datetime
) -> [dict]:
    filtered_account_transactions = [
        transaction
        for transaction in account_statements
        if threshold.date() <= datetime.fromisoformat(transaction["postDate"]).date()
    ]

    return filtered_account_transactions


def filter_card_transactions(card_statements: [dict], threshold: datetime):
    filtered_card_transactions = [
        transaction
        for transaction in card_statements
        if threshold < isoparse(transaction["time"])
    ]

    return filtered_card_transactions
