from unittest import TestCase
from financas_automatizadas.ynab import send_account_transaction, send_card_transaction
import requests_mock


class SendAccountTransactionsToYNABTest(TestCase):
    @requests_mock.Mocker()
    def test_send_account_transaction_to_ynab(
        self, requests_mock: requests_mock.Mocker
    ):
        # Arrange
        expected_ynab_transaction_response = {
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
        }
        requests_mock.post(
            url="https://api.youneedabudget.com/v1/budgets/72bf90ed-5c22-4f88-bc02-95fcd82474cb/transactions",
            json=expected_ynab_transaction_response,
            status_code=201,
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

        # Act
        transactions = send_account_transaction(
            account_transactions=account_transactions
        )

        # Assert
        self.assertEqual(transactions, [expected_ynab_transaction_response])

    @requests_mock.Mocker()
    def test_send_card_transaction(self, requests_mocker: requests_mock.Mocker):
        # Arrange
        expected_ynab_transaction_responses = [
            {
                "data": {
                    "transaction_ids": ["e2852594-8fcd-48af-ba13-7df857cdc142"],
                    "transaction": {
                        "id": "e2852594-8fcd-48af-ba13-7df857cdc142",
                        "date": "2021-08-26",
                        "amount": 18839,
                        "memo": "Bourbon Ipiranga - supermercado",
                        "cleared": "cleared",
                        "approved": True,
                        "flag_color": None,
                        "account_id": "e98ed2b0-2c5e-4f37-b82d-9e1fb5caa510",
                        "account_name": "Nubank",
                        "payee_id": None,
                        "payee_name": None,
                        "category_id": None,
                        "category_name": "Uncategorized",
                        "transfer_account_id": None,
                        "transfer_transaction_id": None,
                        "matched_transaction_id": None,
                        "import_id": "61281a14-2674-45d6-8e50-1c097bdc966f",
                        "deleted": False,
                        "subtransactions": [],
                    },
                    "server_knowledge": 9406,
                }
            },
            {
                "data": {
                    "transaction_ids": ["277bdf05-11be-4fd1-a3f6-1a488a316ae1"],
                    "transaction": {
                        "id": "277bdf05-11be-4fd1-a3f6-1a488a316ae1",
                        "date": "2021-08-26",
                        "amount": 3250,
                        "memo": "Usina da Massa - restaurante",
                        "cleared": "cleared",
                        "approved": True,
                        "flag_color": None,
                        "account_id": "e98ed2b0-2c5e-4f37-b82d-9e1fb5caa510",
                        "account_name": "Nubank",
                        "payee_id": None,
                        "payee_name": None,
                        "category_id": None,
                        "category_name": "Uncategorized",
                        "transfer_account_id": None,
                        "transfer_transaction_id": None,
                        "matched_transaction_id": None,
                        "import_id": "61281afe-d463-468b-a043-e3bcba8a5931",
                        "deleted": False,
                        "subtransactions": [],
                    },
                    "server_knowledge": 9408,
                }
            },
        ]
        card_transactions = [
            {
                "description": "Bourbon Ipiranga",
                "category": "transaction",
                "amount": 18839,
                "time": "2021-08-26T22:47:48Z",
                "source": "upfront_national",
                "title": "supermercado",
                "amount_without_iof": 18839,
                "account": "55c0e5cc-5014-4d2b-800a-c40c86c6448b",
                "details": {"status": "settled", "subcategory": "card_present"},
                "id": "61281a14-2674-45d6-8e50-1c097bdc966f",
                "_links": {
                    "self": {
                        "href": "https://prod-s0-facade.nubank.com.br/api/transactions/61281a14-2674-45d6-8e50-1c097bdc966f"
                    }
                },
                "tokenized": False,
                "href": "nuapp://transaction/61281a14-2674-45d6-8e50-1c097bdc966f",
            },
            {
                "description": "Usina da Massa",
                "category": "transaction",
                "amount": 3250,
                "time": "2021-08-26T22:51:41Z",
                "source": "upfront_national",
                "title": "restaurante",
                "amount_without_iof": 3250,
                "account": "55c0e5cc-5014-4d2b-800a-c40c86c6448b",
                "details": {"status": "settled", "subcategory": "card_present"},
                "id": "61281afe-d463-468b-a043-e3bcba8a5931",
                "_links": {
                    "self": {
                        "href": "https://prod-s0-facade.nubank.com.br/api/transactions/61281afe-d463-468b-a043-e3bcba8a5931"
                    }
                },
                "tokenized": False,
                "href": "nuapp://transaction/61281afe-d463-468b-a043-e3bcba8a5931",
            },
        ]

        requests_mocker.post(
            "https://api.youneedabudget.com/v1/budgets/72bf90ed-5c22-4f88-bc02-95fcd82474cb/transactions",
            [
                {"json": expected_ynab_transaction_responses[0], "status_code": 201},
                {"json": expected_ynab_transaction_responses[1], "status_code": 201},
            ],
        )

        # Act
        ynab_transactions = send_card_transaction(card_transactions=card_transactions)

        # Assert
        self.assertEqual(ynab_transactions, expected_ynab_transaction_responses)
