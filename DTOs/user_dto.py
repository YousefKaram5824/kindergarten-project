from pydantic import BaseModel
from typing import Optional


class UserDTO(BaseModel):
    id: int
    username: str
    role: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True


class CreateUserDTO(BaseModel):
    username: str
    password: str
    role: Optional[str]
