from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.manager import (
    get_manager,
    get_managers,
    create_manager,
    update_manager,
    delete_manager,
)
from schemas.manager import ManagerCreate, ManagerUpdate

router = APIRouter(prefix="/managers", tags=["Managers"])


@router.get("/")
def read_managers(db: Session = Depends(get_db)):
    return get_managers(db)


@router.get("/{manager_id}")
def read_manager(manager_id: int, db: Session = Depends(get_db)):
    manager = get_manager(db, manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Менеджер не найден")
    return manager


@router.post("/")
def add_manager(manager: ManagerCreate, db: Session = Depends(get_db)):
    return create_manager(db, manager)


@router.put("/{manager_id}")
def edit_manager(
    manager_id: int, manager: ManagerUpdate, db: Session = Depends(get_db)
):
    db_manager = get_manager(db, manager_id)
    if not db_manager:
        raise HTTPException(status_code=404, detail="Менеджер не найден")
    return update_manager(db, db_manager, manager)


@router.delete("/{manager_id}")
def remove_manager(manager_id: int, db: Session = Depends(get_db)):
    db_manager = get_manager(db, manager_id)
    if not db_manager:
        raise HTTPException(status_code=404, detail="Менеджер не найден")
    delete_manager(db, db_manager)
    return {"detail": "Менеджер удален"}

