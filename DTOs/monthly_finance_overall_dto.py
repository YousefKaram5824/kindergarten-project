from pydantic import BaseModel, ConfigDict
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
        #orm_mode = True
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


class UpdateMonthlyFinanceOverallDTO(BaseModel):
    month: Optional[str] = None
    full_day_income: Optional[float] = None
    individual_income: Optional[float] = None
    full_day_expenses: Optional[float] = None
    individual_expenses: Optional[float] = None
    external_remaining_full_day: Optional[float] = None
    external_remaining_individual: Optional[float] = None
    loans: Optional[float] = None
    current_total: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
