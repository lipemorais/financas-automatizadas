from datetime import date, timedelta
from decouple import config

import requests

# url = "https://api.pluggy.ai/connectors"
# url = "https://api.pluggy.ai/accounts"
client_id = PLUGGY_CLIENT_ID = config("PLUGGY_CLIENT_ID")
client_secret = config("PLUGGY_CLIENT_SECRET")
itau_account_id = "7209f910-6108-4371-bbd2-e4eb2a678cc7"

nubank_credit_card_id = "36b6b61c-0b07-419d-b9ec-cf3b4ea11d75"
nubank_account_id = "b27ac45a-2e39-4581-989f-77d7c24ee8c4"

itau_connection_item_id = "45894536-cc41-41cf-815e-96dc1427236f"
nubank_connection_item_id = "09c9a9a6-898d-4ecb-b228-daabb7d8ca6d"


def get_api_key(client_id: str, client_secret: str) -> str:
    url = "https://api.pluggy.ai/auth"
    payload = {
        "clientId": client_id,
        "clientSecret": client_secret,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
    )
    data = response.json()
    api_key = data["apiKey"]

    print(response.json())
    return api_key


# api_key = get_api_key(client_id, client_secret)
# print(api_key)


def get_connectors():
    api_key = get_api_key(client_id, client_secret)
    url = "https://api.pluggy.ai/connectors"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }

    response = requests.get(url=url, headers=headers)
    print(response.json())
    return response.json()


# my_connectors = get_connectors()


def get_items():
    api_key = get_api_key(client_id, client_secret)
    item_url = "https://api.pluggy.ai/items"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }

    response = requests.get(
        url=f"{item_url}/09c9a9a6-898d-4ecb-b228-daabb7d8ca6d",
        headers=headers,
    )
    print(response.json())
    return response.json()


# items = get_items()


def get_accounts():
    api_key = get_api_key(client_id, client_secret)
    account_url = "https://api.pluggy.ai/accounts"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }

    response = requests.get(
        url=f"{account_url}",
        params={"itemId": nubank_connection_item_id},
        headers=headers,
    )
    print(response.json())
    return response.json()


# accounts = get_accounts()


def get_transactions():
    api_key = get_api_key(client_id, client_secret)

    account_transaction_surl = "https://api.pluggy.ai/transactions"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }

    today = date.today()
    a_week_ago = today - timedelta(days=7)
    response = requests.get(
        url=f"{account_transaction_surl}",
        params={
            "accountId": itau_account_id,
            "from": a_week_ago.strftime("%Y-%m-%d"),
            "to": today.strftime("%Y-%m-%d"),
            "page": 1,
            "pageSize": 50,
        },
        headers=headers,
    )
    print(response.json())
    return response.json()


transactions = get_transactions()

print(transactions)
