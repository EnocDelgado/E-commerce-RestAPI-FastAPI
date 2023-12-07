from pydantic import BaseModel
from datetime import datetime
from .user import UserOut
from .product import Product
# from pydantic.types import conint

class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime
    owner_id: int
    product_id: int
    owner: UserOut
    product: Product
    

    class Config:
        orm_mode = True
