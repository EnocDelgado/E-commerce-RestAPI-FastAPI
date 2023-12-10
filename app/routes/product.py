from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Product
from ..schemas import product
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import List, Optional

# Create an instance of APIRouter for handling products-related routes
router = APIRouter(
    prefix="/products",
    tags=['Products']
)

# Define a route to retrieve a list of products
@router.get("/", response_model=List[product.Product])
def get_products(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""
):
    # Query the database to retrieve a list of products with optional limit and offset
    product = db.query(Product).limit(limit).offset(skip).all()
    
    return product

# Define a route to create a new product
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=product.Product)
def create_product(
    product: product.ProductCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Create a new product instance with the owner ID and product details
    new_product = Product(owner_id=current_user.id, **product.dict())
    # Add the product to the database, commit, and refresh
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Define a route to retrieve a specific product by ID
@router.get("/{id}", response_model=product.Product)
def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve a specific product by ID
    product = db.query(Product).group_by(Product.id).filter(Product.id == id).first()

    # Validation: Check if the product exists and if the current user is authorized
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} was not found")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    return product

# Define a route to update a specific product by ID
@router.put("/{id}", response_model=product.Product, status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: product.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve the product for updating
    task_product = db.query(Product).filter(Product.id == id)
    product = task_product.first()

    # Validation: Check if the product exists and if the current user is authorized
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    # Update the product with the provided data and commit changes
    task_product.update(updated_product.dict(), synchronize_session=False)
    db.commit()

    return task_product.first()

# Define a route to delete a specific product by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve the product for deletion
    task_product = db.query(Product).filter(Product.id == id)
    product = task_product.first()

    # Validation: Check if the product exists and if the current user is authorized
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    # Delete the product from the database, commit changes, and return a success response
    task_product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
