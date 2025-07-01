from decouple import config

import ynab
from my_pluggy import get_transactions
from schemas import Transaction
from my_pluggy import get_api_key

import sys
import os

NAME_ENVVAR_SUFFIX = "NAME"
PLUGGY_ID_ENVVAR_SUFFIX = "PLUGGY_ID"
YNAB_BUDGET_ID_ENVVAR_SUFFIX = "YNAB_BUDGET_ID"
YNAB_ID_ENVVAR_SUFFIX = "YNAB_ID"
ACCT_ENVVAR_SUFFIXES = [
    NAME_ENVVAR_SUFFIX,
    PLUGGY_ID_ENVVAR_SUFFIX,
    YNAB_BUDGET_ID_ENVVAR_SUFFIX,
    YNAB_ID_ENVVAR_SUFFIX,
]

def get_bank_accounts_from_env():
    """
    Parses the user's provided envvars into bank accounts, ensuring that we have
    at least one bank account, and any bank account has all the information we need
    """
    bank_accounts = []
    idx = 0
    while True:
        envvars = map(lambda suffix: f'ACCOUNT_{idx}_{suffix}', ACCT_ENVVAR_SUFFIXES)

        vars_present = 0
        envvar_to_value = {}
        suffix_to_value = {}
        for i, envvar in enumerate(envvars):
            value = config(envvar, default=None)
            if value is not None:
                vars_present += 1
            envvar_to_value[envvar] = value
            suffix_to_value[ACCT_ENVVAR_SUFFIXES[i]] = value

        if vars_present == 0:
            # If we haven't seen a signle account yet, throw an error
            if idx == 0:
                print("Error: You must define at least one bank account using the following envvars: " + ", ".join(envvars))
                sys.exit(1)

            # Otherwise, the user's done defining bank account info
            break

        # We have at least one piece of information; verify that all fields
        # are filled out and build the return object
        missing_info = False
        for envvar, value in envvar_to_value.items():
            if value is None:
                print("Error: Missing required bank information envvar: " + envvar)
                missing_info = True
        if missing_info:
            sys.exit(1)

        bank_accounts.append(suffix_to_value)
        idx += 1

    return bank_accounts

def main() -> [dict]:
    PLUGGY_CLIENT_ID = config("PLUGGY_CLIENT_ID")
    PLUGGY_CLIENT_SECRET = config("PLUGGY_CLIENT_SECRET")
    pluggy_api_key = get_api_key(
        client_id=PLUGGY_CLIENT_ID,
        client_secret=PLUGGY_CLIENT_SECRET,
    )

    # Mapping envvar suffix -> value
    bank_accounts = get_bank_accounts_from_env()

    transactions = {}
    for account in bank_accounts:
        name = account[NAME_ENVVAR_SUFFIX]
        pluggy_id = account[PLUGGY_ID_ENVVAR_SUFFIX]
        ynab_budget_id = account[YNAB_BUDGET_ID_ENVVAR_SUFFIX]
        ynab_id = account[YNAB_ID_ENVVAR_SUFFIX]

        print("######")
        print(f'SYNCING {name}')
        print("######")

        transactions: [Transaction] = get_transactions(
            account_id=pluggy_id,
            api_key=pluggy_api_key,
        )

        transactions.append(
            ynab.send_transactions_to_ynab(
                transactions=transactions,
                budget_id=ynab_budget_id,
                account_id=ynab_id,
            )
        )

    print("######")
    print(f"SYNCED {len(transactions)} TRANSACTIONS")
    print("######")
    return transactions

if __name__ == "__main__":
    main()
