from pydantic import BaseModel
from datetime import datetime
from .user import UserOut
from .product import Product

# Define a Pydantic model for the base order data
class OrderBase(BaseModel):
    product_id: int
    quantity: int

# Define a Pydantic model for creating new orders, inheriting from OrderBase
class OrderCreate(OrderBase):
    pass

# Define a Pydantic model for displaying order details, inheriting from OrderBase
class Order(OrderBase):
    id: int
    created_at: datetime
    owner_id: int
    product_id: int
    owner: UserOut  # Embedded user details
    product: Product  # Embedded product details

    class Config:
        orm_mode = True  # Enables ORM mode for better compatibility with SQLAlchemy
