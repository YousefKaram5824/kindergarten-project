from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from models import ChildTypeEnum


class ChildDTO(BaseModel):
    id: int
    name: str
    birth_date: date
    age: int | None = None
    phone_number: str | None = None
    father_job: str | None = None
    mother_job: str | None = None
    notes: str | None = None
    problems: str | None = None
    child_image: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    child_type: ChildTypeEnum
    has_left: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class CreateChildDTO(BaseModel):
    id: int
    name: str
    birth_date: date
    age: int | None = None
    phone_number: str | None = None
    father_job: str | None = None
    mother_job: str | None = None
    notes: str | None = None
    problems: str | None = None
    child_image: str | None = None
    created_at: datetime | None = None
    child_type: ChildTypeEnum = ChildTypeEnum.FULL_DAY
    has_left: Optional[bool] = False

    # New fields for FULL_DAY and SESSIONS
    monthly_fee: float | None = None
    bus_fee: float | None = None
    session_fee: float | None = None
    monthly_sessions_count: int | None = None
