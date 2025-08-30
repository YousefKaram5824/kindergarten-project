from pydantic import BaseModel
from typing import Optional


class BookForSaleDTO(BaseModel):
    id: int
    book_name: str
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    remaining: Optional[int]
    notes: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True 


class CreateBookForSaleDTO(BaseModel):
    book_name: str
    quantity: Optional[int]
    buy_price: Optional[float]
    sell_price: Optional[float]
    remaining: Optional[int]
    notes: Optional[str]
