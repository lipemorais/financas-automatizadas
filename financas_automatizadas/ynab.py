import requests
from decouple import config

from schemas import TransactionKind, Transaction

auth_token = config("YNAB_TOKEN")
headers = {"Authorization": "Bearer " + auth_token, "Content-Type": "application/json"}



def get_amount(transaction: Transaction) -> int:
    if transaction.kind == TransactionKind.DEBIT:
        return -abs(transaction.amount)
    else:  # TransactionKind is CREDIT
        return +abs(transaction.amount)


def send_transactions_to_ynab(transactions: [Transaction], account_id) -> [dict]:
    base_url = "https://api.youneedabudget.com/v1"
    moraix_budget_id = "72bf90ed-5c22-4f88-bc02-95fcd82474cb"
    url = f"{base_url}/budgets/{moraix_budget_id}/transactions"
    created_transactions = []

    for transaction in transactions:
        amount = get_amount(transaction)

        payload = {
            "transaction": {
                "account_id": account_id,
                "date": transaction.date.strftime("%Y-%m-%d"),
                "amount": amount,
                "payee_id": None,
                "payee_name": None,
                "category_id": None,
                "memo": transaction.description,
                "cleared": "cleared",
                "approved": True,
                "import_id": transaction.external_id,
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        created_transactions.append(response.json())

    return created_transactions
