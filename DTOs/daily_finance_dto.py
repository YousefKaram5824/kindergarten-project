from pydantic import BaseModel
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
        orm_mode = True
        from_attributes = True 


class CreateDailyFinanceDTO(BaseModel):
    value: Optional[float]
    remaining: Optional[float]
    count: Optional[int]
    service: Optional[str]
    payment_date: Optional[date]
    notes: Optional[str]
