from pydantic import BaseModel, ConfigDict, Field
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
    child_type: ChildTypeEnum = ChildTypeEnum.NONE
    has_left: Optional[bool] = False


class UpdateChildDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = None
    birth_date: Optional[date] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    father_job: Optional[str] = None
    mother_job: Optional[str] = None
    notes: Optional[str] = None
    problems: Optional[str] = None
    child_image: Optional[str] = None
    child_type: Optional[ChildTypeEnum] = None
    has_left: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

