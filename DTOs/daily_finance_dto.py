from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class DailyFinanceDTO(BaseModel):
    id: int
    value: Optional[float]
    remaining: Optional[float]
    count: Optional[int]
    service: Optional[str]
    payment_date: Optional[date]
    notes: Optional[str]

    class Config:
        from_attributes = True


class CreateDailyFinanceDTO(BaseModel):
    value: Optional[float]
    remaining: Optional[float]
    count: Optional[int]
    service: Optional[str]
    payment_date: Optional[date]
    notes: Optional[str]


class UpdateDailyFinanceDTO(BaseModel):
    value: Optional[float] = None
    remaining: Optional[float] = None
    count: Optional[int] = None
    service: Optional[str] = None
    payment_date: Optional[date] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
