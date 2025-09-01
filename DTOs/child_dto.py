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
    child_image: str | None = None
    created_at: datetime | None = None
    child_type: ChildTypeEnum

    model_config = ConfigDict(from_attributes=True)


class CreateChildDTO(BaseModel):
    name: str
    birth_date: date
    age: int | None = None
    phone_number: str | None = None
    father_job: str | None = None
    mother_job: str | None = None
    notes: str | None = None
    child_image: str | None = None
    created_at: datetime | None = None
    child_type: ChildTypeEnum = ChildTypeEnum.FULL_DAY
