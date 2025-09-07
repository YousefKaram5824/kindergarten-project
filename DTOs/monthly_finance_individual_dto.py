from pydantic import BaseModel, ConfigDict
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
        from_attributes = True


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

class UpdateMonthlyFinanceIndividualDTO(BaseModel):
    month: Optional[str] = None
    total_income: Optional[float] = None
    specialists_total: Optional[float] = None
    center_total: Optional[float] = None
    loans: Optional[float] = None
    specialists_details: Optional[str] = None
    external_remaining: Optional[float] = None
    remaining: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
