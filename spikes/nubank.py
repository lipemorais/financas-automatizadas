from pprint import pprint

from decouple import config
from pynubank import Nubank

CPF = config("CPF")
PASSWORD = config("PASSWORD")
PATH_TO_CERTIFICATE = config("PATH_TO_CERTIFICATE")

nu = Nubank()
nu.authenticate_with_cert(CPF, PASSWORD, PATH_TO_CERTIFICATE)
account_balance = nu.get_account_balance()
print(account_balance)

account_feed = nu.get_account_feed()
pprint(account_feed)

card_feed = nu.get_card_feed()
pprint(card_feed)
