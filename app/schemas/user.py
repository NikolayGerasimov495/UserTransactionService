from typing import List, Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field


class UserRead(schemas.BaseUser[int]):
    balance: float = Field(default=0.0)


class UserCreate(schemas.BaseUserCreate):
    pass


class UserBase(BaseModel):
    email: EmailStr
    balance: float = Field(default=0.0)


class UserUpdate(BaseModel):
    password: Optional[str]


class UserDB(UserBase):
    id: int
    transactions: List[int] = []

    class Config:
        orm_mode = True
