from decouple import config

import ynab
from my_pluggy import get_transactions
from schemas import Transaction
from my_pluggy import get_api_key


def main() -> [dict]:
    PLUGGY_CLIENT_ID = config("PLUGGY_CLIENT_ID")
    PLUGGY_CLIENT_SECRET = config("PLUGGY_CLIENT_SECRET")
    api_key = get_api_key(
        client_id=PLUGGY_CLIENT_ID, client_secret=PLUGGY_CLIENT_SECRET
    )

    # YNAB
    ynab_nuconta_account_id = "d928b335-f1c5-4cf4-8d8b-99d6d8df67bb"
    ynab_credit_card_account_id = "e98ed2b0-2c5e-4f37-b82d-9e1fb5caa510"
    ynab_itau_account_id = "ad709b27-5540-4d2a-ab6a-66f0f4f0e18c"

    # My pluggy
    pluggy_itau_account_id = "7209f910-6108-4371-bbd2-e4eb2a678cc7"
    pluggy_nubank_credit_card_id = "36b6b61c-0b07-419d-b9ec-cf3b4ea11d75"
    pluggy_nubank_account_id = "b27ac45a-2e39-4581-989f-77d7c24ee8c4"

    account_id_pairs = [
        {
            "pluggy": pluggy_itau_account_id,
            "ynab": ynab_itau_account_id,
            "name": "Itaú - Account",
        },
        {
            "pluggy": pluggy_nubank_credit_card_id,
            "ynab": ynab_credit_card_account_id,
            "name": "Nubank - Credit Card",
        },
        {
            "pluggy": pluggy_nubank_account_id,
            "ynab": ynab_nuconta_account_id,
            "name": "Nubank - Account",
        },
    ]

    transactions = {}
    for account_id_pair in account_id_pairs:
        print("######")
        print(f'SYNCING {account_id_pair["name"]}')
        print("######")

        transactions: [Transaction] = get_transactions(
            account_id=account_id_pair["pluggy"],
            api_key=api_key,
        )

        transactions.append(
            ynab.send_transactions_to_ynab(
                transactions=transactions,
                account_id=account_id_pair["ynab"],
            )
        )

    print("######")
    print(f"SYNCED {len(transactions)} TRANSACTIONS")
    print("######")
    return transactions



if __name__ == "__main__":
    main()
