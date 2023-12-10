from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

# Define a Pydantic model for the base product data
class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    in_stock: bool = True

# Define a Pydantic model for creating new products, inheriting from ProductBase
class ProductCreate(ProductBase):
    pass

# Define a Pydantic model for displaying product details, inheriting from ProductBase
class Product(ProductBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # Embedded user details

    class Config:
        orm_mode = True  # Enables ORM mode for better compatibility with SQLAlchemy

# (Optional) Commented-out class for a potential ProductOut model (if needed)
# class ProductOut(BaseModel):
#     product: Product
#
#     class Config:
#         orm_mode = True
