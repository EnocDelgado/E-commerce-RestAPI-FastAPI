from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Order
from ..schemas import order
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import  List, Optional

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

@router.get("/", response_model=List[order.Order])
def get_orders(db: Session = Depends(get_db), 
              current_user: int = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    

    tasks = db.query(Order).limit(limit).offset(skip).all()

    return tasks


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=order.Order)
def create_order(order: order.OrderCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    new_task = Order(owner_id=current_user.id, **order.dict())
    # add order to our database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/{id}", response_model=order.Order)
def get_order(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    order = db.query(Order).group_by(
            Order.id).filter(Order.id == id).first()

    # Validation
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"order with id: {id} was not found")
    
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    return order


@router.put("/{id}", response_model=order.Order, status_code=status.HTTP_200_OK)
def update_order(id: int, updated_order: order.OrderCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    task_order = db.query(Order).filter(Order.id == id)

    order = task_order.first()

    # Validation
    if order == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"order with id: {id} does not exist")
    
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    task_order.update(updated_order.dict(), synchronize_session=False)

    db.commit()

    return task_order.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    task_order  = db.query(Order).filter(Order.id == id)

    order = task_order.first()

    # Validation
    if order == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"order with id: {id} does not exists")
    
    if order.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    task_order .delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
