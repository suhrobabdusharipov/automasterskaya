from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.service import (
    get_service,
    get_services,
    create_service,
    update_service,
    delete_service,
)
from schemas.service import ServiceCreate, ServiceUpdate

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/")
def read_services(db: Session = Depends(get_db)):
    return get_services(db)

@router.get("/{service_id}")
def read_service(service_id: int, db: Session = Depends(get_db)):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return service

@router.post("/")
def add_service(service: ServiceCreate, db: Session = Depends(get_db)):
    return create_service(db, service)

@router.put("/{service_id}")
def edit_service(
    service_id: int, service: ServiceUpdate, db: Session = Depends(get_db)
):
    db_service = get_service(db, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return update_service(db, db_service, service)

@router.delete("/{service_id}")
def remove_service(service_id: int, db: Session = Depends(get_db)):
    db_service = get_service(db, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    delete_service(db, db_service)
    return {"detail": "Услуга удалена"}