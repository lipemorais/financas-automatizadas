from unittest import TestCase, mock, skip
from unittest.mock import MagicMock

import requests_mock
from freezegun import freeze_time
from pynubank import MockHttpClient

from financas_automatizadas.main import main


class MainTest(TestCase):
    @mock.patch("financas_automatizadas.main.setup_nubank_client_authentication")
    @requests_mock.Mocker()
    @freeze_time("2021-09-07")
    def test_send_account_transactions_to_ynab(
        self,
        setup_nubank_client_authentication_mocked,
        requests_mock: requests_mock.Mocker,
    ):
        # Arrange
        MockedNubank = MagicMock()
        account_statements = {
            "pageInfo": {"hasNextPage": True},
            "edges": [
                # Pagamendo agendado
                {
                    "cursor": "ezpwcmlvcml0eSAwLCA6dGltZXN0YW1wICNudS90aW1lICIyMDIzLTAyLTA4VDEyOjAwOjAwWiIsIDppZCAjdXVpZCAiNjNiNDNjYWQtYzQ0YS00ZTc1LWFhNzYtNjA1NTUwZDBmNjA4In0=",
                    "node": {
                        "tags": ["money-out"],
                        "showClock": False,
                        "displayDate": "Ontem",
                        "footer": "Pix",
                        "title": "Transferência enviada",
                        "detailsDeeplink": "nuapp://flutter/savings/details-screen/type/PIX_TRANSFER_OUT_REQUEST/id/63b96ace-d914-482d-8d6e-6cba2b4d1287",
                        "id": "63b96ace-d914-482d-8d6e-6cba2b4d1287",
                        "strikethrough": False,
                        "kind": "NEUTRAL",
                        "iconKey": "nuds_v2_icon.money_out",
                        "postDate": "2023-01-07",
                        "detail": "Joãozinho \nR$\xa015,00",
                        "amount": 15.0,
                    },
                },
                # Falha no pagamento strikethrough True
                {
                    "cursor": "ezpwcmlvcml0eSAwLCA6dGltZXN0YW1wICNudS90aW1lICIyMDIzLTAxLTAzVDA0OjQ5OjM5LjM3NVoiLCA6aWQgI3V1aWQgIjYzOGEyNGY3LTNiYTQtNDMxMi05ZTAxLTcxNmQ0ODYxNWY5MiJ9",
                    "node": {
                        "tags": ["money-out", "payments"],
                        "showClock": False,
                        "displayDate": "03 JAN",
                        "footer": "R$\xa04.028,50",
                        "title": "Falha no agendamento",
                        "detailsDeeplink": None,
                        "id": "638a24f7-3ba4-4312-9e01-716d48615f92",
                        "strikethrough": True,
                        "kind": "NEUTRAL",
                        "iconKey": "nuds_v2_icon.bar_code",
                        "postDate": "2023-01-03",
                        "detail": "NAO INFORMADO",
                        "amount": 4028.5,
                    },
                },
            ],
        }
        card_statements = [
            {
                "description": "Willy da Silva Mendes",
                "category": "transaction",
                "amount": 200,
                "time": "2021-08-27T22:29:04Z",
                "source": "upfront_national",
                "title": "lazer",
                "amount_without_iof": 200,
                "account": "55c0e5cc-5014-4d2b-800a-c40c86c6448b",
                "details": {"status": "settled", "subcategory": "card_present"},
                "id": "61296731-3757-4f04-a66e-46c2b510d3a0",
                "_links": {
                    "self": {
                        "href": "https://prod-s0-facade.nubank.com.br/api/transactions/61296731-3757-4f04-a66e-46c2b510d3a0"
                    }
                },
                "tokenized": False,
                "href": "nuapp://transaction/61296731-3757-4f04-a66e-46c2b510d3a0",
            },
            {
                "description": "Pag*Tananimalthadesou",
                "category": "transaction",
                "amount": 500,
                "time": "2021-08-27T22:27:05Z",
                "source": "upfront_national",
                "title": "outros",
                "amount_without_iof": 500,
                "account": "55c0e5cc-5014-4d2b-800a-c40c86c6448b",
                "details": {"status": "settled", "subcategory": "card_present"},
                "id": "612966b9-01cc-4a11-8b5e-cb580e63ac10",
                "_links": {
                    "self": {
                        "href": "https://prod-s0-facade.nubank.com.br/api/transactions/612966b9-01cc-4a11-8b5e-cb580e63ac10"
                    }
                },
                "tokenized": False,
                "href": "nuapp://transaction/612966b9-01cc-4a11-8b5e-cb580e63ac10",
            },
            {
                "description": "Usina da Massa",
                "category": "transaction",
                "amount": 3250,
                "time": "2021-09-07T22:51:41Z",
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

        mocked_nu_instance = MagicMock()
        MockedNubank.return_value = mocked_nu_instance
        mocked_nu_instance.get_account_statements_paginated.return_value = (
            account_statements
        )
        mocked_nu_instance.get_card_statements.return_value = card_statements

        ynab_account_transaction_response = {
            "transaction": {
                "account_id": "d928b335-f1c5-4cf4-8d8b-99d6d8df67bb",
                "date": "2021-09-07",
                "amount": 101,
                "payee_id": None,
                "payee_name": None,
                "category_id": None,
                "memo": "LIVEPIX LTDA\nR$\xa01,00",
                "cleared": "cleared",
                "approved": True,
                "import_id": "6137cd3a-58a4-4a0a-a04e-8be7b347d38d",
            }
        }

        ynab_card_transaction_response = {
            "transaction": {
                "account_id": "e98ed2b0-2c5e-4f37-b82d-9e1fb5caa510",
                "date": "2021-09-07",
                "amount": 3250,
                "payee_id": None,
                "payee_name": None,
                "category_id": None,
                "memo": "Usina da Massa - restaurante",
                "cleared": "cleared",
                "approved": True,
                "import_id": "61281afe-d463-468b-a043-e3bcba8a5931",
            }
        }

        requests_mock.post(
            "https://api.youneedabudget.com/v1/budgets/72bf90ed-5c22-4f88-bc02-95fcd82474cb/transactions",
            [
                {"json": ynab_account_transaction_response, "status_code": 201},
                {"json": ynab_card_transaction_response, "status_code": 201},
            ],
        )

        # Act
        result = main(nubank_client=MockedNubank(client=MockHttpClient))

        # Assert
        self.assertEqual(
            [ynab_account_transaction_response, ynab_card_transaction_response], result
        )
