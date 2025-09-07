from pydantic import BaseModel, ConfigDict
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

class UpdateBookForSaleDTO(BaseModel):
    book_name: Optional[str] = None
    quantity: Optional[int] = None
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    remaining: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
