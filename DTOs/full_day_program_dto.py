from pydantic import BaseModel
from datetime import date
from typing import Optional


class FullDayProgramDTO(BaseModel):
    id: int
    entry_date: Optional[date]
    diagnosis: Optional[str]
    tests_applied: Optional[str]
    monthly_fee: Optional[float]
    bus_fee: Optional[float]
    training_plan: Optional[str]
    monthly_report: Optional[str]
    attendance_status: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True 


class CreateFullDayProgramDTO(BaseModel):
    entry_date: Optional[date]
    diagnosis: Optional[str]
    tests_applied: Optional[str]
    monthly_fee: Optional[float]
    bus_fee: Optional[float]
    training_plan: Optional[str]
    monthly_report: Optional[str]
    attendance_status: Optional[str]
    notes: Optional[str]
