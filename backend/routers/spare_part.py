from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.spare_part import (
    get_spare_part,
    get_spare_parts,
    create_spare_part,
    update_spare_part,
    delete_spare_part,
)
from schemas.spare_part import SparePartCreate, SparePartUpdate

router = APIRouter(prefix="/spare_parts", tags=["Spare Parts"])

@router.get("/")
def read_spare_parts(db: Session = Depends(get_db)):
    return get_spare_parts(db)

@router.get("/{spare_part_id}")
def read_spare_part(spare_part_id: int, db: Session = Depends(get_db)):
    spare_part = get_spare_part(db, spare_part_id)
    if not spare_part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    return spare_part

@router.post("/")
def add_spare_part(spare_part: SparePartCreate, db: Session = Depends(get_db)):
    return create_spare_part(db, spare_part)

@router.put("/{spare_part_id}")
def edit_spare_part(
    spare_part_id: int, spare_part: SparePartUpdate, db: Session = Depends(get_db)
):
    db_spare_part = get_spare_part(db, spare_part_id)
    if not db_spare_part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    return update_spare_part(db, db_spare_part, spare_part)

@router.delete("/{spare_part_id}")
def remove_spare_part(spare_part_id: int, db: Session = Depends(get_db)):
    db_spare_part = get_spare_part(db, spare_part_id)
    if not db_spare_part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    delete_spare_part(db, db_spare_part)
    return {"detail": "Запчасть удалена"}