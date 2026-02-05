from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.crud.master import (
    get_master,
    get_masters,
    create_master,
    update_master,
    delete_master,
)
from backend.schemas.master import MasterCreate, MasterUpdate

router = APIRouter(prefix="/masters", tags=["Masters"])

@router.get("/")
def read_masters(db: Session = Depends(get_db)):
    return get_masters(db)

@router.get("/{master_id}")
def read_master(master_id: int, db: Session = Depends(get_db)):
    master = get_master(db, master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Мастер не найден")
    return master

@router.post("/")
def add_master(master: MasterCreate, db: Session = Depends(get_db)):
    return create_master(db, master)

@router.put("/{master_id}")
def edit_master(
    master_id: int, master: MasterUpdate, db: Session = Depends(get_db)
):
    db_master = get_master(db, master_id)
    if not db_master:
        raise HTTPException(status_code=404, detail="Мастер не найден")
    return update_master(db, db_master, master)

@router.delete("/{master_id}")
def remove_master(master_id: int, db: Session = Depends(get_db)):
    db_master = get_master(db, master_id)
    if not db_master:
        raise HTTPException(status_code=404, detail="Мастер не найден")
    delete_master(db, db_master)
    return {"detail": "Мастер удален"}
