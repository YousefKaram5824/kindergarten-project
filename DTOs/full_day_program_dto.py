from pydantic import BaseModel
from datetime import date
from typing import Optional


class FullDayProgramDTO(BaseModel):
    id: int
    diagnosis: Optional[str]
    monthly_fee: Optional[float]
    bus_fee: Optional[float]
    attendance_status: Optional[str]
    notes: Optional[str]

    birth_certificate: Optional[str]
    father_id_card: Optional[str]

    tests_applied_file: Optional[str]
    training_plan_file: Optional[str]
    monthly_report_file: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True


class CreateFullDayProgramDTO(BaseModel):
    diagnosis: Optional[str]
    monthly_fee: Optional[float]
    bus_fee: Optional[float]
    attendance_status: Optional[str]
    notes: Optional[str]

    birth_certificate: Optional[str]
    father_id_card: Optional[str]

    tests_applied_file: Optional[str]
    training_plan_file: Optional[str]
    monthly_report_file: Optional[str]


class UpdateFullDayProgramDTO(BaseModel):
    diagnosis: Optional[str] = None
    monthly_fee: Optional[float] = None
    bus_fee: Optional[float] = None
    attendance_status: Optional[str] = None
    notes: Optional[str] = None

    birth_certificate: Optional[str] = None
    father_id_card: Optional[str] = None

    tests_applied_file: Optional[str] = None
    training_plan_file: Optional[str] = None
    monthly_report_file: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
