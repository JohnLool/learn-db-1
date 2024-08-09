from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    name: str
    email: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    price: float


class ProductRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int
    product_id: int


class OrderRead(BaseModel):
    id: int
    user_id: int
    product_id: int

    class Config:
        from_attributes = True
