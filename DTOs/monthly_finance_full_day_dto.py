from pydantic import BaseModel, ConfigDict
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
        #orm_mode = True
        from_attributes = True


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


class UpdateMonthlyFinanceFullDayDTO(BaseModel):
    month: Optional[str] = None
    total_income: Optional[float] = None
    rent: Optional[float] = None
    transport: Optional[float] = None
    loans: Optional[float] = None
    salaries: Optional[float] = None
    monthly_expenses: Optional[float] = None
    external_remaining: Optional[float] = None
    remaining: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
