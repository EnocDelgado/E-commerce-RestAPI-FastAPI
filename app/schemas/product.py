from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

# from pydantic.types import conint

class PrdouctBase(BaseModel):
    name: str
    description: str
    price: int
    in_stock: bool = True


class ProductCreate(PrdouctBase):
    pass

class Product(PrdouctBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# class ProductOut(BaseModel):
#     product: Product

#     class Config:
#         orm_mode = True