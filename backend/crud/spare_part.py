from sqlalchemy.orm import Session
from models.spare_part import SparePart
from schemas.spare_part import SparePartCreate, SparePartUpdate


def get_spare_part(db: Session, spare_part_id: int):
    return db.query(SparePart).filter(SparePart.id == spare_part_id).first()

def get_spare_parts(db: Session):
    return db.query(SparePart).all()


def create_spare_part(db: Session, spare_part: SparePartCreate):
    db_spare_part = SparePart(**spare_part.model_dump())
    db.add(db_spare_part)
    db.commit()
    db.refresh(db_spare_part)
    return db_spare_part


def update_spare_part(db: Session, db_spare_part: SparePart, spare_part: SparePartUpdate):
    for field, value in spare_part.model_dump(exclude_unset=True).items():
        setattr(db_spare_part, field, value)

    db.commit()
    db.refresh(db_spare_part)
    return db_spare_part


def delete_spare_part(db: Session, db_spare_part: SparePart):
    db.delete(db_spare_part)
    db.commit()
