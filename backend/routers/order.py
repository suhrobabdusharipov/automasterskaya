from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.order import (
    get_order,
    get_orders,
    create_order,
    update_order,
    delete_order,
)
from schemas.order import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def read_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.get("/{order_id}")
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@router.post("/")
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

@router.put("/{order_id}")
def edit_order(
    order_id: int, order: OrderUpdate, db: Session = Depends(get_db)
):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return update_order(db, db_order, order)

@router.delete("/{order_id}")
def remove_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    delete_order(db, db_order)
    return {"detail": "Заказ удален"}