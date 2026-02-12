from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.crud.car import (
    get_car,
    get_cars,
    create_car,
    update_car,
    delete_car,
)
from backend.schemas.car import CarCreate, CarUpdate
from backend.models.car import Car
from backend.models.client import Client
templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/")
def cars_page(request: Request, db: Session = Depends(get_db)):
    cars = get_cars(db)
    for car in cars:
        if car.client_id:
            car.client = db.query(Client).filter(Client.id == car.client_id).first()
    
    return templates.TemplateResponse(
        "cars/list.html",
        {"request": request, "cars": cars}
    )

@router.get("/new")
def create_car_page(request: Request, db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return templates.TemplateResponse(
        "cars/new.html",
        {"request": request, "clients": clients}
    )

@router.post("/new")
def create_car_form(
    request: Request,
    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    vin: str = Form(...),
    client_id: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        existing = db.query(Car).filter(Car.vin == vin).first()
        if existing:
            return RedirectResponse("/cars/new?error=vin_exists", status_code=303)
        
        car_data = CarCreate(
            client_id=client_id,
            brand=brand,
            model=model,
            year=year,
            vin=vin,

        )
        car = create_car(db, car_data)
        return RedirectResponse(f"/cars/{car.id}?success=created", status_code=303)
        
    except IntegrityError:
        db.rollback()
        return RedirectResponse("/cars/new?error=vin_exists", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        return RedirectResponse("/cars/new?error=server", status_code=303)

@router.get("/{car_id}")
def car_detail_page(request: Request, car_id: int, db: Session = Depends(get_db)):
    car = get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    if car.client_id:
        car.client = db.query(Client).filter(Client.id == car.client_id).first()
    return templates.TemplateResponse(
        "cars/detail.html",
        {"request": request, "car": car}
    )

@router.get("/{car_id}/edit")
def edit_car_page(request: Request, car_id: int, db: Session = Depends(get_db)):
    car = get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return templates.TemplateResponse(
        "cars/edit.html",
        {"request": request, "car": car}
    )

@router.post("/{car_id}/edit")
def edit_car_form(
    request: Request,
    car_id: int,
    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    vin: str = Form(...),
    db: Session = Depends(get_db)
):
    db_car = get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    car_update = CarUpdate(
        brand=brand,
        model = model,
        year=year,
        vin=vin
    )
    try:
        update_car(db,db_car,car_update)
        return RedirectResponse(f"/clients/{car_id}?success=updated", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении автомобиля: {e}")
        return RedirectResponse(f"/clients/{car_id}/edit?error=server", status_code=303)

@router.get("/api/")
def read_cars_api(db: Session = Depends(get_db)):
    return get_cars(db)

@router.get("/api/{car_id}")
def read_car_api(car_id: int, db: Session = Depends(get_db)):
    car = get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return car

@router.post("/api/")
def add_car_api(car: CarCreate, db: Session = Depends(get_db)):
    return create_car(db, car)

@router.put("/api/{car_id}")
def edit_car_api(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    return update_car(db, db_car, car)

@router.delete("/api/{car_id}")
def remove_car_api(car_id: int, db: Session = Depends(get_db)):
    db_car = get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    delete_car(db, db_car)
    return {"detail": "Машина удалена"}
