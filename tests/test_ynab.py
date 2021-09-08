from unittest import TestCase
from financas_automatizadas.ynab import send_account_transaction
import requests_mock


class SendAccountTransactionsToYNAB(TestCase):
    @requests_mock.Mocker()
    def test_send_account_transaction_to_ynab(self, requests_mock):
        requests_mock(
            "POST",
            url="https://api.youneedabudget.com/v1/budgets/72bf90ed-5c22-4f88-bc02-95fcd82474cb/transactions",
            json={
                "transaction": {
                    "account_id": "d928b335-f1c5-4cf4-8d8b-99d6d8df67bb",
                    "date": "2021-09-07",
                    "amount": 100,
                    "payee_id": None,
                    "payee_name": None,
                    "category_id": None,
                    "memo": "LIVEPIX LTDA\nR$\xa01,00",
                    "cleared": "cleared",
                    "approved": True,
                    "import_id": "6137cd3a-58a4-4a0a-a04e-8be7b347d38d",
                }
            },
        )
        account_transactions = [
            {
                "__typename": "PixTransferOutEvent",
                "amount": 1.0,
                "detail": "LIVEPIX LTDA\nR$\xa01,00",
                "id": "6137cd3a-58a4-4a0a-a04e-8be7b347d38d",
                "postDate": "2021-09-07",
                "title": "Transferência enviada",
            }
        ]

        response = send_account_transaction(account_transactions=account_transactions)

        self.assertEqual(response, {})
