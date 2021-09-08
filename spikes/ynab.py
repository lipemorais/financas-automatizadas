import requests
from decouple import config

auth_token = config("YNAB_TOKEN")
headers = {'Authorization': 'Bearer ' + auth_token,
           'Content-Type': 'application/json'}

nuconta_account_id = "d928b335-f1c5-4cf4-8d8b-99d6d8df67bb"
credit_card_account_id = "e98ed2b0-2c5e-4f37-b82d-9e1fb5caa510"
data = {
    "transaction": {
        "account_id": nuconta_account_id,
        "date": "2021-05-23",
        "amount": 150491,
        "payee_id": None,
        "payee_name": "Magalu",
        "category_id": None,
        "memo": "Comprar do arcondicionado na Magalu",
        "cleared": "cleared",
        "approved": True,
        "flag_color": "purple",
        # "import_id": # Nubanks transaction ID
    }
}
base_url = "https://api.youneedabudget.com/v1"
moraix_budget_id = "72bf90ed-5c22-4f88-bc02-95fcd82474cb"
url = '{base_url}/budgets/{moraix_budget_id}/transactions'.format(base_url=base_url, moraix_budget_id=moraix_budget_id)

response = requests.post(url, json=data, headers=headers)
print(response)
print(response.json())
