from pydantic import BaseModel, ConfigDict
from typing import Optional


class ToolForSaleDTO(BaseModel):
    id: int
    tool_name: str
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    tool_number: Optional[str]
    remaining: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True


class CreateToolForSaleDTO(BaseModel):
    tool_name: str
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    tool_number: Optional[str]
    remaining: Optional[int]
    notes: Optional[str]


class UpdateToolForSaleDTO(BaseModel):
    tool_name: Optional[str] = None
    quantity: Optional[int] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    tool_number: Optional[str] = None
    remaining: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
