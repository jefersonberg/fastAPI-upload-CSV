from pydantic import BaseModel, EmailStr, Field
from datetime import date

class DebtBase(BaseModel):
    name: str = Field(..., example="John Doe")
    governmentId: str = Field(..., example="1234567890")
    email: EmailStr = Field(..., example="johndoe@example.com")
    debtAmount: float = Field(..., example=100.0)
    debtDueDate: date = Field(..., example="2024-01-01")
    debtId: str = Field(..., example="1")

class DebtCreate(DebtBase):
    pass

class DebtInDB(DebtBase):
    id: str

    class Config:
        orm_mode = True
