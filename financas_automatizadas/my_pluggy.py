from datetime import timedelta, date, datetime
from unittest.mock import ANY

import requests
from decouple import config


from schemas import Transaction

PLUGGY_URL = "https://api.pluggy.ai/"
PLUGGY_CLIENT_ID = config("PLUGGY_CLIENT_ID")
PLUGGY_CLIENT_SECRET = config("PLUGGY_CLIENT_SECRET")


def get_api_key(client_id: str, client_secret: str) -> str:
    pluggy_auth_url = f"{PLUGGY_URL}auth"
    payload = {
        "clientId": client_id,
        "clientSecret": client_secret,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    response = requests.post(
        pluggy_auth_url,
        json=payload,
        headers=headers,
    )
    data = response.json()
    api_key = data["apiKey"]

    return api_key


headers_with_api_key = {
    "accept": "application/json",
    "X-API-KEY": get_api_key(
        client_id=PLUGGY_CLIENT_ID,
        client_secret=PLUGGY_CLIENT_SECRET,
    ),
}


# get account/credit card transactions
def normalize_transactions(pluggy_transactions) -> [Transaction]:
    normalized_transactions = []

    for transaction in pluggy_transactions:
        description = transaction["description"].strip()
        description_parts = description.split("|")
        payee=None
        if len(description_parts) >= 2:
            payee=description_parts[1]

        new_transaction = Transaction(
            external_id=transaction["id"],
            amount=int(
                transaction["amount"] * 1000
            ),  # ynab data format ref: https://api.ynab.com/#response-format
            description=transaction["description"].strip(),
            date=datetime.fromisoformat(
                transaction["date"].replace("Z", "+00:00")
            ).date(),
            kind=transaction["type"],
            payee=payee,
        )

        normalized_transactions.append(new_transaction)

    return normalized_transactions


def get_transactions(account_id: str, api_key: str) -> list[ANY]:
    account_transactions_url = f"{PLUGGY_URL}transactions"
    today = date.today()
    a_week_ago = today - timedelta(days=7)

    response = requests.get(
        url=f"{account_transactions_url}",
        params={
            "accountId": account_id,
            "from": a_week_ago.strftime("%Y-%m-%d"),
            "to": today.strftime("%Y-%m-%d"),
            "page": 1,
            "pageSize": 50,
        },
        headers={
            "accept": "application/json",
            "X-API-KEY": api_key,
        },
    )
    transactions = normalize_transactions(response.json()["results"])
    return transactions
