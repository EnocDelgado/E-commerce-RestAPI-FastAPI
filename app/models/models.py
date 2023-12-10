from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# Import the Base class from the db.config module
from ..db.config import Base

# Define the User class representing the 'users' table in the database
class User(Base):
    # Specify the table name
    __tablename__ = "users"
    
    # Define columns for the 'users' table
    id = Column(Integer, primary_key=True, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                       nullable=False, server_default=text('now()'))

# Define the Product class representing the 'products' table in the database
class Product(Base):
    # Specify the table name
    __tablename__ = "products"

    # Define columns for the 'products' table
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    in_stock = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                       nullable=False, server_default=text('now()'))
    
    # Define a foreign key relationship with the 'users' table
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

# Define the Order class representing the 'orders' table in the database
class Order(Base):
    # Specify the table name
    __tablename__ = "orders"

    # Define columns for the 'orders' table
    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                       nullable=False, server_default=text('now()'))
    
    # Define foreign key relationships with the 'users' and 'products' tables
    owner = relationship("User")
    product = relationship("Product")
