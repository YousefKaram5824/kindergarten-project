from pydantic import BaseModel
from typing import Optional


class MonthlyFinanceOverallDTO(BaseModel):
    id: int
    month: str
    full_day_income: Optional[float]
    individual_income: Optional[float]
    full_day_expenses: Optional[float]
    individual_expenses: Optional[float]
    external_remaining_full_day: Optional[float]
    external_remaining_individual: Optional[float]
    loans: Optional[float]
    current_total: Optional[float]
    notes: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True


class CreateMonthlyFinanceOverallDTO(BaseModel):
    month: str
    full_day_income: Optional[float]
    individual_income: Optional[float]
    full_day_expenses: Optional[float]
    individual_expenses: Optional[float]
    external_remaining_full_day: Optional[float]
    external_remaining_individual: Optional[float]
    loans: Optional[float]
    current_total: Optional[float]
    notes: Optional[str]
