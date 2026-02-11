from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.crud.client import get_client, get_clients, create_client, update_client, delete_client
from backend.schemas.client import ClientCreate, ClientUpdate
from backend.models.car import Car

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
def clients_page(request: Request, db: Session = Depends(get_db)):
    clients = get_clients(db)
    return templates.TemplateResponse(
        "clients/list.html",
        {"request": request, "clients": clients}
    )

@router.get("/new")
def new_client_page(request: Request):
    return templates.TemplateResponse(
        "clients/new.html",
        {"request": request}
    )

@router.post("/new")
def create_client_form(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(None),
    address: str = Form(None),
    db: Session = Depends(get_db)
):
    client_data = ClientCreate(
        full_name=full_name,
        phone=phone,
        email=email,
        address=address
    )
    try:
        create_client(db, client_data)
        return RedirectResponse(url="/clients?success=created", status_code=303)
    except IntegrityError:
        db.rollback()
        return RedirectResponse(url="/clients/new?error=duplicate", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        return RedirectResponse(url="/clients/new?error=server", status_code=303)

@router.get("/{client_id}")
def client_detail_page(request: Request, client_id: int, db: Session = Depends(get_db)):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    
    client.cars = db.query(Car).filter(Car.client_id == client_id).all()
    
    return templates.TemplateResponse(
        "clients/detail.html",
        {"request": request, "client": client}
    )

@router.get("/api/")
def read_clients_api(db: Session = Depends(get_db)):
    return get_clients(db)

@router.get("/api/{client_id}")
def read_client_api(client_id: int, db: Session = Depends(get_db)):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client

@router.post("/api/")
def add_client_api(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.put("/api/{client_id}")
def edit_client_api(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return update_client(db, db_client, client)

@router.delete("/api/{client_id}")
def remove_client_api(client_id: int, db: Session = Depends(get_db)):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    delete_client(db, db_client)
    return {"detail": "Клиент удален"}
