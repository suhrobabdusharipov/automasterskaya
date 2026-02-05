from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.crud.car import (
    get_car,
    get_cars,
    create_car,
    update_car,
    delete_car,
)
from backend.schemas.car import CarCreate, CarUpdate

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/")
def read_cars(db: Session = Depends(get_db)):
    return get_cars(db)

@router.get("/{car_id}")
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return car

@router.post("/")
def add_car(car: CarCreate, db: Session = Depends(get_db)):
    return create_car(db, car)

@router.put("/{car_id}")
def edit_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return update_car(db, db_car, car)

@router.delete("/{car_id}")
def remove_car(car_id: int, db: Session = Depends(get_db)):
    db_car = get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    delete_car(db, db_car)
    return {"detail": "Машина удалена"}