from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Product
from ..schemas import product
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import  List, Optional

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.get("/", response_model=List[product.Product])
def get_products(db: Session = Depends(get_db), 
              current_user: int = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    

    product = db.query(Product).limit(limit).offset(skip).all()

    return product


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=product.Product)
def create_product(product: product.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    new_product = Product(owner_id=current_user.id, **product.dict())
    # add product to our database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{id}", response_model=product.Product)
def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    product = db.query(Product).group_by(
            Product.id).filter(Product.id == id).first()

    # Validation
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"product with id: {id} was not found")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    return product


@router.put("/{id}", response_model=product.Product, status_code=status.HTTP_200_OK)
def update_product(id: int, updated_product: product.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    task_product = db.query(Product).filter(Product.id == id)

    product = task_product.first()

    # Validation
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"product with id: {id} does not exist")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    task_product.update(updated_product.dict(), synchronize_session=False)

    db.commit()

    return task_product.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    task_product  = db.query(Product).filter(Product.id == id)

    product = task_product.first()

    # Validation
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"product with id: {id} does not exists")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    task_product .delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
