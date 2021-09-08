from unittest import TestCase
from financas_automatizadas.nubank import filter_account_transactions
from freezegun import freeze_time


class TestAccount(TestCase):
    @freeze_time("2021-09-07")
    def test_get_account_feed_events(self):
        account_feed = [
            {
                "id": "6137cd3a-58a4-4a0a-a04e-8be7b347d38d",
                "__typename": "GenericFeedEvent",
                "title": "Transferência enviada",
                "detail": "LIVEPIX LTDA\nR$\xa01,00",
                "postDate": "2021-09-07",
            },
            {
                "id": "61322d34-c3fa-4c02-98cb-05577381e44f",
                "__typename": "GenericFeedEvent",
                "title": "Transferência enviada",
                "detail": "THIAGO BARELLA\nR$\xa051.814,00",
                "postDate": "2021-09-03",
            },
            {
                "id": "61320fd0-e9c4-4e8e-9b2a-fe4f9ec366dd",
                "__typename": "GenericFeedEvent",
                "title": "Transferência enviada",
                "detail": "Josemar Afrovulto\nR$\xa03.233,36",
                "postDate": "2021-09-03",
            },
            {
                "id": "613202d0-f7fc-451c-91fb-26a470e654b3",
                "__typename": "TransferInEvent",
                "title": "Transferência recebida",
                "detail": "R$\xa03.233,36",
                "postDate": "2021-09-03",
                "amount": 3233.36,
                "originAccount": {
                    "name": "Paypal do Brasil Servicos de Pagamentos Ltda"
                },
            },
            {
                "id": "612f6cc5-f4e3-424b-a0c1-734f7fb62651",
                "__typename": "BarcodePaymentEvent",
                "title": "Pagamento efetuado",
                "detail": "AUXILIADORA PREDIAL LTDA",
                "postDate": "2021-09-01",
                "amount": 1032.44,
            },
            {
                "id": "612ec223-70d5-4f1b-b18c-cfb6912606bd",
                "__typename": "BillPaymentEvent",
                "title": "Pagamento da fatura",
                "detail": "Cartão Nubank - R$\xa08.937,11",
                "postDate": "2021-08-31",
                "amount": 8937.11,
            },
            {
                "id": "610bd40d-57e6-4524-a1ca-3af65985e049",
                "__typename": "DebitPurchaseEvent",
                "title": "Compra no débito",
                "detail": "Pag*Elgiodamiaodasilv - R$\xa04,00",
                "postDate": "2021-08-05",
                "amount": 4.0,
            },
        ]

        expected_transactions = [
            {
                "__typename": "PixTransferOutEvent",
                "amount": 1.0,
                "detail": "LIVEPIX LTDA\nR$\xa01,00",
                "id": "6137cd3a-58a4-4a0a-a04e-8be7b347d38d",
                "postDate": "2021-09-07",
                "title": "Transferência enviada",
            }
        ]

        filtered_transactions = filter_account_transactions(account_feed=account_feed)

        self.assertEqual(filtered_transactions, expected_transactions)
