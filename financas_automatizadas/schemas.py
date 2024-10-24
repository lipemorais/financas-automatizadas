from datetime import date
from pydantic import BaseModel


class Transaction(BaseModel):
    external_id: str
    amount: int
    description: str
    date: date
