from decouple import config

import ynab
from config import get_account_pairs
from my_pluggy import get_transactions
from schemas import Transaction
from my_pluggy import get_api_key


def main() -> [dict]:
    PLUGGY_CLIENT_ID = config("PLUGGY_CLIENT_ID")
    PLUGGY_CLIENT_SECRET = config("PLUGGY_CLIENT_SECRET")
    api_key = get_api_key(
        client_id=PLUGGY_CLIENT_ID,
        client_secret=PLUGGY_CLIENT_SECRET,
    )
    ynab_budget_id = config("YNAB_BUDGET_ID")
    account_id_pairs = get_account_pairs()

    created_transactions = []
    for account_id_pair in account_id_pairs:
        print("######")
        print(f'SYNCING {account_id_pair["name"]}')
        print("######")

        transactions: [Transaction] = get_transactions(
            account_id=account_id_pair["pluggy"],
            api_key=api_key,
        )

        transactions_to_ynab = ynab.send_transactions_to_ynab(
            transactions=transactions,
            account_id=account_id_pair["ynab"],
            budget_id=ynab_budget_id,
        )

        created_transactions += transactions_to_ynab

    print("######")
    print(f"SYNCED {len(created_transactions)} TRANSACTIONS")
    print("######")
    return created_transactions



if __name__ == "__main__":
    main()
