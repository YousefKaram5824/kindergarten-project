from pydantic import BaseModel
from typing import Optional


class UniformForSaleDTO(BaseModel):
    id: int
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    remaining: Optional[int]
    notes: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True 


class CreateUniformForSaleDTO(BaseModel):
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    remaining: Optional[int]
    notes: Optional[str]
