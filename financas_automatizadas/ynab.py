import requests
from decouple import config

auth_token = config("YNAB_TOKEN")
headers = {"Authorization": "Bearer " + auth_token, "Content-Type": "application/json"}

nuconta_account_id = "d928b335-f1c5-4cf4-8d8b-99d6d8df67bb"
credit_card_account_id = "e98ed2b0-2c5e-4f37-b82d-9e1fb5caa510"

INFLOW = (
    "TransferInEvent",
    "TransferOutReversalEvent",
    "DebitPurchaseReversalEvent",
    "PixTransferInEvent",
    "PixTransferOutReversalEvent",
    "PixTransferFailedEvent",
)

OUTFLOW = (
    "TransferOutEvent",
    "BarcodePaymentEvent",
    "DebitPurchaseEvent",
    "BillPaymentEvent",
    "DebitWithdrawalFeeEvent",
    "DebitWithdrawalEvent",
    "PixTransferOutEvent",
)


def send_account_transaction(account_transactions: [dict]) -> [dict]:
    base_url = "https://api.youneedabudget.com/v1"
    moraix_budget_id = "72bf90ed-5c22-4f88-bc02-95fcd82474cb"
    url = f"{base_url}/budgets/{moraix_budget_id}/transactions"
    created_transactions = []

    for account_transaction in account_transactions:
        amount = int(account_transaction["amount"] * 1000)
        payload = {
            "transaction": {
                "account_id": nuconta_account_id,
                "date": account_transaction["postDate"],
                "amount": amount
                if account_transaction["__typename"] in INFLOW
                else -amount,
                "payee_id": None,
                "payee_name": None,
                "category_id": None,
                "memo": account_transaction["detail"],
                "cleared": "cleared",
                "approved": True,
                "import_id": account_transaction["id"],
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        created_transactions.append(response.json())

    return created_transactions


def send_card_transaction(card_transactions: [dict]) -> [dict]:
    base_url = "https://api.youneedabudget.com/v1"
    moraix_budget_id = "72bf90ed-5c22-4f88-bc02-95fcd82474cb"
    url = f"{base_url}/budgets/{moraix_budget_id}/transactions"
    transactions = []

    for card_transaction in card_transactions:
        payload = {
            "transaction": {
                "account_id": credit_card_account_id,
                "date": card_transaction["time"].split("T")[0],
                "amount": -card_transaction["amount"] * 10,
                "payee_id": None,
                "payee_name": None,
                "category_id": None,
                "memo": f"{card_transaction['description']} - {card_transaction['title']}",
                "cleared": "cleared",
                "approved": True,
                "import_id": card_transaction["id"],
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        transactions.append(response.json())

    return transactions
