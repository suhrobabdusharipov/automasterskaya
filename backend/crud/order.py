from sqlalchemy.orm import Session
from backend.models.order import Order
from backend.schemas.order import OrderCreate, OrderUpdate


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session):
    return db.query(Order).all()


def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, db_order: Order, order: OrderUpdate):
    for field, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)

    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, db_order: Order):
    db.delete(db_order)
    db.commit()
