from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional

from backend.database import get_db, engine, Base
from backend.models.client import Client
from backend.models.car import Car
from backend.models.contract import Contract
from backend.models.order import Order

app = FastAPI(title="Автомастерская")

# Создаем таблицы при запуске
Base.metadata.create_all(bind=engine)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Главная страница
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {"request": request}
    )

# ==================== КЛИЕНТЫ ====================
@app.get("/clients")
def clients_page(request: Request, db: Session = Depends(get_db)):
    """Страница списка клиентов"""
    clients = db.query(Client).all()
    return templates.TemplateResponse(
        "clients/list.html",
        {"request": request, "clients": clients}
    )

@app.get("/clients/new")
def create_client_page(request: Request):
    """Форма создания клиента"""
    return templates.TemplateResponse(
        "clients/new.html",
        {"request": request}
    )

@app.post("/clients/new")
def create_client(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(None),
    address: str = Form(None),
    db: Session = Depends(get_db)
):
    """Создание клиента"""
    try:
        # Проверяем уникальность телефона
        existing = db.query(Client).filter(Client.phone == phone).first()
        if existing:
            return RedirectResponse("/clients/new?error=phone_exists", status_code=303)
        
        # Создаем клиента
        client = Client(
            full_name=full_name,
            phone=phone,
            email=email,
            address=address
        )
        db.add(client)
        db.commit()
        return RedirectResponse(f"/clients/{client.id}?success=created", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        return RedirectResponse("/clients/new?error=server", status_code=303)

@app.get("/clients/{client_id}")
def client_detail(request: Request, client_id: int, db: Session = Depends(get_db)):
    """Детали клиента"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return RedirectResponse("/clients", status_code=303)
    
    # Загружаем автомобили клиента
    client.cars = db.query(Car).filter(Car.client_id == client_id).all()
    
    return templates.TemplateResponse(
        "clients/detail.html",
        {"request": request, "client": client}
    )

# ==================== АВТОМОБИЛИ ====================
@app.get("/cars")
def cars_page(request: Request, db: Session = Depends(get_db)):
    """Страница списка автомобилей"""
    cars = db.query(Car).all()
    
    # Загружаем владельцев
    for car in cars:
        if car.client_id:
            car.client = db.query(Client).filter(Client.id == car.client_id).first()
    
    return templates.TemplateResponse(
        "cars/list.html",
        {"request": request, "cars": cars}
    )

@app.get("/cars/new")
def create_car_page(request: Request, db: Session = Depends(get_db)):
    """Форма создания автомобиля"""
    clients = db.query(Client).all()
    return templates.TemplateResponse(
        "cars/new.html",
        {"request": request, "clients": clients}
    )

@app.post("/cars/new")
def create_car(
    request: Request,
    brand: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    vin: str = Form(...),
    license_plate: str = Form(None),
    color: str = Form(None),
    client_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """Создание автомобиля"""
    try:
        # Проверяем VIN
        existing = db.query(Car).filter(Car.vin == vin).first()
        if existing:
            return RedirectResponse("/cars/new?error=vin_exists", status_code=303)
        
        # Создаем автомобиль
        car = Car(
            brand=brand,
            model=model,
            year=year,
            vin=vin,
            license_plate=license_plate,
            color=color,
            client_id=client_id
        )
        db.add(car)
        db.commit()
        return RedirectResponse(f"/cars/{car.id}?success=created", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        return RedirectResponse("/cars/new?error=server", status_code=303)

@app.get("/cars/{car_id}")
def car_detail(request: Request, car_id: int, db: Session = Depends(get_db)):
    """Детали автомобиля"""
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return RedirectResponse("/cars", status_code=303)
    
    # Загружаем владельца
    if car.client_id:
        car.client = db.query(Client).filter(Client.id == car.client_id).first()
    
    return templates.TemplateResponse(
        "cars/detail.html",
        {"request": request, "car": car}
    )

# ==================== ДОГОВОРЫ ====================
@app.get("/contracts")
def contracts_page(request: Request, db: Session = Depends(get_db)):
    """Страница списка договоров"""
    contracts = db.query(Contract).all()
    
    # Загружаем связанные данные
    for contract in contracts:
        if contract.client_id:
            contract.client = db.query(Client).filter(Client.id == contract.client_id).first()
        if contract.car_id:
            contract.car = db.query(Car).filter(Car.id == contract.car_id).first()
    
    return templates.TemplateResponse(
        "contracts/list.html",
        {"request": request, "contracts": contracts}
    )

@app.get("/contracts/new")
def create_contract_page(request: Request, db: Session = Depends(get_db)):
    """Форма создания договора"""
    clients = db.query(Client).all()
    cars = db.query(Car).all()
    
    return templates.TemplateResponse(
        "contracts/new.html",
        {
            "request": request,
            "clients": clients,
            "cars": cars,
            "today": date.today().strftime("%Y-%m-%d")
        }
    )

@app.post("/contracts/new")
def create_contract(
    request: Request,
    client_id: int = Form(...),
    car_id: int = Form(...),
    date: str = Form(...),
    status: str = Form("draft"),
    total_amount: float = Form(0.0),
    db: Session = Depends(get_db)
):
    """Создание договора"""
    try:
        # Парсим дату
        try:
            contract_date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            contract_date = date.today()
        
        # Создаем договор
        contract = Contract(
            client_id=client_id,
            car_id=car_id,
            date=contract_date,
            status=status,
            total_amount=total_amount
        )
        db.add(contract)
        db.commit()
        return RedirectResponse(f"/contracts/{contract.id}?success=created", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        return RedirectResponse("/contracts/new?error=server", status_code=303)

@app.get("/contracts/{contract_id}")
def contract_detail(request: Request, contract_id: int, db: Session = Depends(get_db)):
    """Детали договора"""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return RedirectResponse("/contracts", status_code=303)
    
    # Загружаем связанные данные
    if contract.client_id:
        contract.client = db.query(Client).filter(Client.id == contract.client_id).first()
    if contract.car_id:
        contract.car = db.query(Car).filter(Car.id == contract.car_id).first()
    
    # Загружаем заказы по договору
    contract.orders = db.query(Order).filter(Order.contract_id == contract_id).all()
    
    return templates.TemplateResponse(
        "contracts/detail.html",
        {"request": request, "contract": contract}
    )

# ==================== ЗАКАЗЫ ====================
@app.get("/orders")
def orders_page(request: Request, db: Session = Depends(get_db)):
    """Страница списка заказов"""
    orders = db.query(Order).all()
    
    # Загружаем связанные данные
    for order in orders:
        if order.contract_id:
            order.contract = db.query(Contract).filter(Contract.id == order.contract_id).first()
            if order.contract and order.contract.client_id:
                order.contract.client = db.query(Client).filter(Client.id == order.contract.client_id).first()
    
    return templates.TemplateResponse(
        "orders/list.html",
        {"request": request, "orders": orders}
    )

@app.get("/orders/new")
def create_order_page(request: Request, db: Session = Depends(get_db)):
    """Форма создания заказа"""
    contracts = db.query(Contract).all()
    
    # Загружаем данные договоров
    for contract in contracts:
        if contract.client_id:
            contract.client = db.query(Client).filter(Client.id == contract.client_id).first()
        if contract.car_id:
            contract.car = db.query(Car).filter(Car.id == contract.car_id).first()
    
    return templates.TemplateResponse(
        "orders/new.html",
        {
            "request": request,
            "contracts": contracts,
            "today": date.today().strftime("%Y-%m-%d")
        }
    )

@app.post("/orders/new")
def create_order(
    request: Request,
    contract_id: int = Form(...),
    date: str = Form(...),
    services_description: str = Form(...),
    total_cost: float = Form(0.0),
    db: Session = Depends(get_db)
):
    """Создание заказа"""
    try:
        # Парсим дату
        try:
            order_date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            order_date = date.today()
        
        # Создаем заказ
        order = Order(
            contract_id=contract_id,
            date=order_date,
            services_description=services_description,
            total_cost=total_cost
        )
        db.add(order)
        db.commit()
        return RedirectResponse(f"/orders/{order.id}?success=created", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        return RedirectResponse("/orders/new?error=server", status_code=303)

@app.get("/orders/{order_id}")
def order_detail(request: Request, order_id: int, db: Session = Depends(get_db)):
    """Детали заказа"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return RedirectResponse("/orders", status_code=303)
    
    # Загружаем договор
    if order.contract_id:
        order.contract = db.query(Contract).filter(Contract.id == order.contract_id).first()
        if order.contract:
            if order.contract.client_id:
                order.contract.client = db.query(Client).filter(Client.id == order.contract.client_id).first()
            if order.contract.car_id:
                order.contract.car = db.query(Car).filter(Car.id == order.contract.car_id).first()
    
    return templates.TemplateResponse(
        "orders/detail.html",
        {"request": request, "order": order}
    )
