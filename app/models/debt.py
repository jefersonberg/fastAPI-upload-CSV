from pydantic import BaseModel
from datetime import date

class Debt(BaseModel):
    name: str
    governmentId: str
    email: str
    debtAmount: float
    debtDueDate: date
    debtId: str
