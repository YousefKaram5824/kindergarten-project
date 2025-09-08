from pydantic import BaseModel, ConfigDict
from datetime import date as Date
from typing import Optional


class DailyVisitDTO(BaseModel):
    id: int
    child_id: int
    value: Optional[float]
    appointment: Optional[str]
    date: Optional[Date]
    purpose: Optional[str]
    notes: Optional[str]

    class Config:
        #orm_mode = True
        from_attributes = True


class CreateDailyVisitDTO(BaseModel):
    child_id: Optional[int]
    value: Optional[float]
    appointment: Optional[str]
    date: Optional[Date]
    purpose: Optional[str]
    notes: Optional[str]


class UpdateDailyVisitDTO(BaseModel):
    child_id: Optional[int] = None
    value: Optional[float] = None
    appointment: Optional[str] = None
    date: Optional[Date] = None  # pyright: ignore[reportInvalidTypeForm]
    purpose: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
