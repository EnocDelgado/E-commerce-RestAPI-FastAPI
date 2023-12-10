from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Order
from ..schemas import order
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import List, Optional

# Create an instance of APIRouter for handling orders-related routes
router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

# Define a route to retrieve a list of orders
@router.get("/", response_model=List[order.Order])
def get_orders(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""
):
    # Query the database to retrieve a list of orders with optional limit and offset
    tasks = db.query(Order).limit(limit).offset(skip).all()
    
    return tasks

# Define a route to create a new order
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=order.Order)
def create_order(
    order: order.OrderCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Create a new order instance with the owner ID and order details
    new_task = Order(owner_id=current_user.id, **order.dict())
    # Add the order to the database, commit, and refresh
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# Define a route to retrieve a specific order by ID
@router.get("/{id}", response_model=order.Order)
def get_order(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve a specific order by ID
    order = db.query(Order).group_by(Order.id).filter(Order.id == id).first()

    # Validation: Check if the order exists and if the current user is authorized
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {id} was not found")
    
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    return order

# Define a route to update a specific order by ID
@router.put("/{id}", response_model=order.Order, status_code=status.HTTP_200_OK)
def update_order(id: int, updated_order: order.OrderCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve the order for updating
    task_order = db.query(Order).filter(Order.id == id)
    order = task_order.first()

    # Validation: Check if the order exists and if the current user is authorized
    if order == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {id} does not exist")
    
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    # Update the order with the provided data and commit changes
    task_order.update(updated_order.dict(), synchronize_session=False)
    db.commit()

    return task_order.first()

# Define a route to delete a specific order by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve the order for deletion
    task_order = db.query(Order).filter(Order.id == id)
    order = task_order.first()

    # Validation: Check if the order exists and if the current user is authorized
    if order == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {id} does not exist")
    
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    # Delete the order from the database, commit changes, and return a success response
    task_order.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
