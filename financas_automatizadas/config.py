import json

from decouple import config


def get_account_pairs():
    account_pairs_json = config("ACCOUNT_PAIRS")
    return json.loads(account_pairs_json)
