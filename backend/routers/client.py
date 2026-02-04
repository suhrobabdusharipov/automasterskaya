from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.client import (
    get_client,
    get_clients,
    create_client,
    update_client,
    delete_client,
)
from schemas.client import ClientCreate, ClientUpdate

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/")
def read_clients(db: Session = Depends(get_db)):
    return get_clients(db)

@router.get("/{client_id}")
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client

@router.post("/")
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.put("/{client_id}")
def edit_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return update_client(db, db_client, client)


@router.delete("/{client_id}")
def remove_client(client_id: int, db: Session = Depends(get_db)):
    db_client = get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    delete_client(db, db_client)
    return {"detail": "Клиент удален"}
