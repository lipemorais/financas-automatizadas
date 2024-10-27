from datetime import date
from enum import Enum

from pydantic import BaseModel


class TransactionKind(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class Transaction(BaseModel):
    external_id: str
    amount: int
    description: str
    date: date
    kind: str
