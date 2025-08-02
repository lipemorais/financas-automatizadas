from datetime import date

from requests_mock import Mocker
from schemas import Transaction

from financas_automatizadas.my_pluggy import get_api_key, get_transactions


def test_get_itau_transactions(requests_mock: Mocker):
    # get itau transactions
    itau_transactions = {
        "total": 1,
        "totalPages": 1,
        "page": 1,
        "results": [
            {
                "id": "f011bdc5-4ced-4d50-9fff-f0bfd08e8b97",
                "description": "SAQUE DIN ATM BIOME00026",
                "descriptionRaw": "SAQUE DIN ATM BIOME00026",
                "currencyCode": "BRL",
                "amount": -100,
                "amountInAccountCurrency": None,
                "date": "2024-10-23T02:59:00.000Z",
                "category": "Same person transfer - CASH",
                "categoryId": "04010000",
                "balance": None,
                "accountId": "7209f910-6108-4371-bbd2-e4eb2a678cc7",
                "providerCode": None,
                "status": "POSTED",
                "paymentData": {
                    "payer": {
                        "accountNumber": None,
                        "branchNumber": None,
                        "documentNumber": {
                            "type": "CPF",
                            "value": "111.111.111-11",
                        },
                        "name": None,
                        "routingNumber": None,
                        "routingNumberISPB": None,
                    },
                    "paymentMethod": "OTHER",
                    "reason": None,
                    "receiver": None,
                    "receiverReferenceId": None,
                    "referenceNumber": None,
                    "boletoMetadata": None,
                },
                "type": "DEBIT",
                "operationType": "SAQUE",
                "creditCardMetadata": None,
                "acquirerData": None,
                "merchant": None,
                "createdAt": "2024-10-23T00:45:11.068Z",
                "updatedAt": "2024-10-24T00:46:24.504Z",
            }
        ],
    }
    # TODO: split it into 2 tests one for get_apy_key and a second for get_transactions
    # Arrange
    pluggy_auth_url = "https://api.pluggy.ai/auth"
    fake_client_id = "fake_client_id"
    fake_client_secret = "fake_client_secret"
    requests_mock.post(
        pluggy_auth_url,
        json={"apiKey": "fake_api_key"},
    )

    requests_mock.get(
        "https://api.pluggy.ai/transactions?accountId=fake_account_id&from=2024-10-17&to=2024-10-24&page=1&pageSize=50",
        [
            {
                "json": itau_transactions,
            }
        ],
    )

    fake_api_key = get_api_key(fake_client_id, fake_client_secret)
    fake_account_id = "fake_account_id"

    # Act
    transactions = get_transactions(
        account_id=fake_account_id,
    )
    # Assert
    assert len(transactions) == 1

    my_transaction: Transaction = transactions[0]
    assert my_transaction.external_id == "f011bdc5-4ced-4d50-9fff-f0bfd08e8b97"
    assert my_transaction.amount == -10000
    assert my_transaction.description == "SAQUE DIN ATM BIOME00026"
    assert my_transaction.date == date(2024, 10, 23)
