from datetime import datetime

from pydantic import BaseModel


class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: datetime

    class Config:
        orm_mode = True

class SpendRequest(BaseModel):
    points: int
