from pydantic import BaseModel
from typing import Optional


class MonthlyFinanceIndividualDTO(BaseModel):
    id: int
    month: str
    total_income: Optional[float]
    specialists_total: Optional[float]
    center_total: Optional[float]
    loans: Optional[float]
    specialists_details: Optional[str]
    external_remaining: Optional[float]
    remaining: Optional[float]
    notes: Optional[str]

    class Config:
        orm_mode = True


class CreateMonthlyFinanceIndividualDTO(BaseModel):
    month: str
    total_income: Optional[float]
    specialists_total: Optional[float]
    center_total: Optional[float]
    loans: Optional[float]
    specialists_details: Optional[str]
    external_remaining: Optional[float]
    remaining: Optional[float]
    notes: Optional[str]
