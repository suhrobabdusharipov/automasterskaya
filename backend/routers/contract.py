from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from typing import Optional

from backend.database import get_db
from backend.crud.contract import (
    get_contract,
    get_contracts,
    create_contract,
    update_contract,
    delete_contract,
)
from backend.schemas.contract import ContractCreate, ContractUpdate
from backend.models.client import Client
from backend.models.car import Car
from backend.models.order import Order

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.get("/")
def contracts_page(request: Request, db: Session = Depends(get_db)):
    contracts = get_contracts(db)
    
    for contract in contracts:
        if contract.client_id:
            contract.client = db.query(Client).filter(Client.id == contract.client_id).first()
        if contract.car_id:
            contract.car = db.query(Car).filter(Car.id == contract.car_id).first()
    
    return templates.TemplateResponse(
        "contracts/list.html",
        {"request": request, "contracts": contracts}
    )

@router.get("/new")
def create_contract_page(request: Request, db: Session = Depends(get_db)):
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

@router.post("/new")
def create_contract_form(
    request: Request,
    client_id: int = Form(...),
    car_id: int = Form(...),
    date: str = Form(...),
    status: str = Form("draft"),
    total_amount: float = Form(0.0),
    db: Session = Depends(get_db)
):
    try:
        try:
            contract_date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            contract_date = date.today()
        
        contract_data = ContractCreate(
            client_id=client_id,
            car_id=car_id,
            date=contract_date,
            status=status,
            total_amount=total_amount
        )
        contract = create_contract(db, contract_data)
        
        return RedirectResponse(f"/contracts/{contract.id}?success=created", status_code=303)
        
    except IntegrityError:
        db.rollback()
        return RedirectResponse("/contracts/new?error=integrity", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании договора: {e}")
        return RedirectResponse("/contracts/new?error=server", status_code=303)

@router.get("/{contract_id}")
def contract_detail_page(request: Request, contract_id: int, db: Session = Depends(get_db)):
    contract = get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    
    if contract.client_id:
        contract.client = db.query(Client).filter(Client.id == contract.client_id).first()
    if contract.car_id:
        contract.car = db.query(Car).filter(Car.id == contract.car_id).first()
    
    contract.orders = db.query(Order).filter(Order.contract_id == contract_id).all()
    
    return templates.TemplateResponse(
        "contracts/detail.html",
        {"request": request, "contract": contract}
    )

@router.get("/{contract_id}/edit")
def edit_contract_page(request: Request, contract_id: int, db: Session = Depends(get_db)):
    contract = get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    
    if contract.client_id:
        contract.client = db.query(Client).filter(Client.id == contract.client_id).first()
    if contract.car_id:
        contract.car = db.query(Car).filter(Car.id == contract.car_id).first()
    
    contract.orders = db.query(Order).filter(Order.contract_id == contract_id).all()
    
    clients = db.query(Client).all()
    cars = db.query(Car).all()
    
    return templates.TemplateResponse(
        "contracts/edit.html",
        {
            "request": request,
            "contract": contract,
            "clients": clients,
            "cars": cars,
            "today": date.today().strftime("%Y-%m-%d")
        }
    )

@router.post("/{contract_id}/edit")
def edit_contract_form(
    request: Request,
    contract_id: int,
    client_id: int = Form(...),
    car_id: int = Form(...),
    date: str = Form(...),
    status: str = Form(...),
    total_amount: float = Form(0.0),
    db: Session = Depends(get_db)
):
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    
    try:
        try:
            contract_date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            contract_date = date.today()
        
        update_data = ContractUpdate(
            client_id=client_id,
            car_id=car_id,
            date=contract_date,
            status=status,
            total_amount=total_amount
        )
        
        updated_contract = update_contract(db, db_contract, update_data)
        
        return RedirectResponse(f"/contracts/{contract_id}?success=updated", status_code=303)
        
    except IntegrityError:
        db.rollback()
        return RedirectResponse(f"/contracts/{contract_id}/edit?error=integrity", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении договора: {e}")
        return RedirectResponse(f"/contracts/{contract_id}/edit?error=server", status_code=303)

@router.get("/api/")
def read_contracts_api(db: Session = Depends(get_db)):
    return get_contracts(db)

@router.get("/api/{contract_id}")
def read_contract_api(contract_id: int, db: Session = Depends(get_db)):
    contract = get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return contract

@router.post("/api/")
def add_contract_api(contract: ContractCreate, db: Session = Depends(get_db)):
    return create_contract(db, contract)

@router.put("/api/{contract_id}")
def edit_contract_api(
    contract_id: int, contract: ContractUpdate, db: Session = Depends(get_db)
):
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return update_contract(db, db_contract, contract)

@router.delete("/api/{contract_id}")
def remove_contract_api(contract_id: int, db: Session = Depends(get_db)):
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    
    orders = db.query(Order).filter(Order.contract_id == contract_id).first()
    if orders:
        raise HTTPException(
            status_code=400, 
            detail="Нельзя удалить договор, у которого есть заказ-наряды"
        )
    
    delete_contract(db, db_contract)
    return {"detail": "Договор удален"}

@router.delete("/{contract_id}")
def remove_contract_html(contract_id: int, db: Session = Depends(get_db)):
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    
    orders = db.query(Order).filter(Order.contract_id == contract_id).first()
    if orders:
        return RedirectResponse(
            f"/contracts/{contract_id}?error=has_orders", 
            status_code=303
        )
    
    delete_contract(db, db_contract)
    return RedirectResponse("/contracts?success=deleted", status_code=303)
