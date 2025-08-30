from pydantic import BaseModel
from datetime import date
from typing import Optional


class IndividualSessionDTO(BaseModel):
    id: int
    entry_date: Optional[date]
    diagnosis: Optional[str]
    tests_applied: Optional[str]
    session_fee: Optional[float]
    monthly_sessions_count: Optional[int]
    attended_sessions_count: Optional[int]
    specialist_name: Optional[str]
    monthly_report: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True 


class CreateIndividualSessionDTO(BaseModel):
    entry_date: Optional[date]
    diagnosis: Optional[str]
    tests_applied: Optional[str]
    session_fee: Optional[float]
    monthly_sessions_count: Optional[int]
    attended_sessions_count: Optional[int]
    specialist_name: Optional[str]
    monthly_report: Optional[str]
    notes: Optional[str]
