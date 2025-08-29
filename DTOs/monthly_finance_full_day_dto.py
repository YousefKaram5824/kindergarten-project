from pydantic import BaseModel
from typing import Optional


class MonthlyFinanceFullDayDTO(BaseModel):
    id: int
    month: str
    total_income: Optional[float]
    rent: Optional[float]
    transport: Optional[float]
    loans: Optional[float]
    salaries: Optional[float]
    monthly_expenses: Optional[float]
    external_remaining: Optional[float]
    remaining: Optional[float]
    notes: Optional[str]

    class Config:
        orm_mode = True


class CreateMonthlyFinanceFullDayDTO(BaseModel):
    month: str
    total_income: Optional[float]
    rent: Optional[float]
    transport: Optional[float]
    loans: Optional[float]
    salaries: Optional[float]
    monthly_expenses: Optional[float]
    external_remaining: Optional[float]
    remaining: Optional[float]
    notes: Optional[str]
