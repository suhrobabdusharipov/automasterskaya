from sqlalchemy.orm import Session
from models.master import Master
from schemas.master import MasterCreate, MasterUpdate


def get_master(db: Session, master_id: int):
    return db.query(Master).filter(Master.id == master_id).first()

def get_masters(db: Session):
    return db.query(Master).all()


def create_master(db: Session, master: MasterCreate):
    db_master = Master(**master.model_dump())
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master


def update_master(db: Session, db_master: Master, master: MasterUpdate):
    for field, value in master.model_dump(exclude_unset=True).items():
        setattr(db_master, field, value)

    db.commit()
    db.refresh(db_master)
    return db_master

def delete_master(db: Session, db_master: Master):
    db.delete(db_master)
    db.commit()
