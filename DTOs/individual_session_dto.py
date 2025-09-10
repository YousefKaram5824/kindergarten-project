from pydantic import BaseModel, ConfigDict
from typing import Optional


class IndividualSessionDTO(BaseModel):
    id: int
    diagnosis: Optional[str]
    session_fee: Optional[float]
    monthly_sessions_count: Optional[int]
    attended_sessions_count: Optional[int]
    specialist_name: Optional[str]
    notes: Optional[str]
    birth_certificate: Optional[str]
    father_id_card: Optional[str]
    tests_applied_file: Optional[str]
    monthly_report_file: Optional[str]

    class Config:
        from_attributes = True


class CreateIndividualSessionDTO(BaseModel):
    diagnosis: Optional[str]
    session_fee: Optional[float]
    monthly_sessions_count: Optional[int]
    attended_sessions_count: Optional[int]
    specialist_name: Optional[str]
    notes: Optional[str]
    birth_certificate: Optional[str]
    father_id_card: Optional[str]
    tests_applied_file: Optional[str]
    monthly_report_file: Optional[str]


class UpdateIndividualSessionDTO(BaseModel):
    diagnosis: Optional[str] = None
    session_fee: Optional[float] = None
    monthly_sessions_count: Optional[int] = None
    attended_sessions_count: Optional[int] = None
    specialist_name: Optional[str] = None
    notes: Optional[str] = None
    birth_certificate: Optional[str] = None
    father_id_card: Optional[str] = None
    tests_applied_file: Optional[str] = None
    monthly_report_file: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
