from pydantic import BaseModel
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
        orm_mode = True
        from_attributes = True


class CreateToolForSaleDTO(BaseModel):
    tool_name: str
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    tool_number: Optional[str]
    remaining: Optional[int]
    notes: Optional[str]
