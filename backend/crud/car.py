from sqlalchemy.orm import Session
from backend.models.car import Car
from backend.schemas.car import CarCreate, CarUpdate


def get_car(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()


def get_cars(db: Session):
    return db.query(Car).all()


def create_car(db: Session, car: CarCreate):
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_car(db: Session, db_car: Car, car: CarUpdate):
    for field, value in car.model_dump(exclude_unset=True).items():
        setattr(db_car, field, value)

    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, db_car: Car):
    db.delete(db_car)
    db.commit()
