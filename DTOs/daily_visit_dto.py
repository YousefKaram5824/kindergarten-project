from pydantic import BaseModel
from datetime import date
from typing import Optional


class DailyVisitDTO(BaseModel):
    id: int
    value: Optional[float]
    appointment: Optional[str]
    date: Optional[date]
    purpose: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True


class CreateDailyVisitDTO(BaseModel):
    value: Optional[float]
    appointment: Optional[str]
    date: Optional[date]
    purpose: Optional[str]
    notes: Optional[str]
