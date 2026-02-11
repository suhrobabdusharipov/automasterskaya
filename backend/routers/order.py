from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional

from backend.database import get_db
from backend.crud.order import (
    get_order,
    get_orders,
    create_order,
    update_order,
    delete_order,
)
from backend.schemas.order import OrderCreate, OrderUpdate
from backend.models.contract import Contract
from backend.models.client import Client
from backend.models.car import Car

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def orders_page(request: Request, db: Session = Depends(get_db)):
    orders = get_orders(db)
    
    for order in orders:
        if order.contract_id:
            order.contract = db.query(Contract).filter(Contract.id == order.contract_id).first()
            if order.contract and order.contract.client_id:
                order.contract.client = db.query(Client).filter(Client.id == order.contract.client_id).first()
    
    return templates.TemplateResponse(
        "orders/list.html",
        {"request": request, "orders": orders}
    )

@router.get("/new")
def create_order_page(request: Request, db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    
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
            "today": datetime.now().strftime("%Y-%m-%dT%H:%M")
        }
    )

@router.post("/new")
def create_order_form(
    request: Request,
    contract_id: int = Form(...),
    date: str = Form(...),
    services_description: str = Form(...),
    total_cost: float = Form(0.0),
    db: Session = Depends(get_db)
):
    try:
        try:
            order_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except:
            try:
                order_date = datetime.strptime(date, "%Y-%m-%d")
            except:
                order_date = datetime.now()
        
        order_data = OrderCreate(
            contract_id=contract_id,
            date=order_date.date(),
            services_description=services_description,
            total_cost=total_cost
        )
        
        order = create_order(db, order_data)
        return RedirectResponse(f"/orders/{order.id}?success=created", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании заказа: {e}")
        return RedirectResponse(f"/orders/new?error=server&error_message={str(e)}", status_code=303)

@router.get("/{order_id}")
def order_detail_page(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
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

@router.get("/{order_id}/edit")
def edit_order_page(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    if order.contract_id:
        order.contract = db.query(Contract).filter(Contract.id == order.contract_id).first()
    
    contracts = db.query(Contract).all()
    
    return templates.TemplateResponse(
        "orders/edit.html",
        {
            "request": request,
            "order": order,
            "contracts": contracts,
            "today": datetime.now().strftime("%Y-%m-%dT%H:%M")
        }
    )

@router.post("/{order_id}/edit")
def edit_order_form(
    request: Request,
    order_id: int,
    contract_id: int = Form(...),
    date: str = Form(...),
    services_description: str = Form(...),
    total_cost: float = Form(0.0),
    db: Session = Depends(get_db)
):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    try:
        try:
            order_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except:
            try:
                order_date = datetime.strptime(date, "%Y-%m-%d")
            except:
                order_date = datetime.now()
        
        update_data = OrderUpdate(
            contract_id=contract_id,
            date=order_date.date(),
            services_description=services_description,
            total_cost=total_cost
        )
        
        updated_order = update_order(db, db_order, update_data)
        
        return RedirectResponse(f"/orders/{order_id}?success=updated", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении заказа: {e}")
        return RedirectResponse(f"/orders/{order_id}/edit?error=server", status_code=303)

@router.get("/api/")
def read_orders_api(db: Session = Depends(get_db)):
    return get_orders(db)

@router.get("/api/{order_id}")
def read_order_api(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@router.post("/api/")
def add_order_api(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

@router.put("/api/{order_id}")
def edit_order_api(
    order_id: int, order: OrderUpdate, db: Session = Depends(get_db)
):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return update_order(db, db_order, order)

@router.delete("/api/{order_id}")
def remove_order_api(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    delete_order(db, db_order)
    return {"detail": "Заказ удален"}

@router.delete("/{order_id}")
def remove_order_html(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    delete_order(db, db_order)
    return RedirectResponse("/orders?success=deleted", status_code=303)
