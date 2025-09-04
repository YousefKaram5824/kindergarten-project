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

    personal_photo: Optional[str]
    birth_certificate: Optional[str]
    father_id_card: Optional[str]
    test_documents: Optional[str]

    tests_applied_file: Optional[str]
    training_plan_file: Optional[str]
    monthly_report_file: Optional[str]
    child_documents_file: Optional[str]

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

    personal_photo: Optional[str]
    birth_certificate: Optional[str]
    father_id_card: Optional[str]
    test_documents: Optional[str]

    tests_applied_file: Optional[str]
    training_plan_file: Optional[str]
    monthly_report_file: Optional[str]
    child_documents_file: Optional[str]


class UpdateFullDayProgramDTO(BaseModel):
    entry_date: Optional[date] = None
    diagnosis: Optional[str] = None
    tests_applied: Optional[str] = None
    monthly_fee: Optional[float] = None
    bus_fee: Optional[float] = None
    training_plan: Optional[str] = None
    monthly_report: Optional[str] = None
    attendance_status: Optional[str] = None
    notes: Optional[str] = None

    personal_photo: Optional[str] = None
    birth_certificate: Optional[str] = None
    father_id_card: Optional[str] = None
    test_documents: Optional[str] = None

    tests_applied_file: Optional[str] = None
    training_plan_file: Optional[str] = None
    monthly_report_file: Optional[str] = None
    child_documents_file: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
