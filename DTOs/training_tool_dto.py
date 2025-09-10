from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class TrainingToolDTO(BaseModel):
    id: int
    tool_name: str
    tool_number: Optional[str]
    tool_image: Optional[str]
    department: Optional[str]
    purchase_date: Optional[date]
    notes: Optional[str]

    class Config:
        from_attributes = True


class CreateTrainingToolDTO(BaseModel):
    tool_name: str
    tool_number: Optional[str]
    tool_image: Optional[str]
    department: Optional[str]
    purchase_date: Optional[date]
    notes: Optional[str]


class UpdateTrainingToolDTO(BaseModel):
    tool_name: Optional[str] = None
    tool_number: Optional[str] = None
    tool_image: Optional[str] = None
    department: Optional[str] = None
    purchase_date: Optional[date] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
