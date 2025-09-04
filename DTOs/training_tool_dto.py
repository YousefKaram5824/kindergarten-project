from pydantic import BaseModel
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
        orm_mode = True
        from_attributes = True


class CreateTrainingToolDTO(BaseModel):
    tool_name: str
    tool_number: Optional[str]
    tool_image: Optional[str]
    department: Optional[str]
    purchase_date: Optional[date]
    notes: Optional[str]
