from sqlalchemy.orm import Session
from models.manager import Manager
from schemas.manager import ManagerCreate, ManagerUpdate


def get_manager(db: Session, manager_id: int):
    return db.query(Manager).filter(Manager.id == manager_id).first()


def get_managers(db: Session):
    return db.query(Manager).all()


def create_manager(db: Session, manager: ManagerCreate):
    db_manager = Manager(**manager.model_dump())
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager


def update_manager(db: Session, db_manager: Manager, manager: ManagerUpdate):
    for field, value in manager.model_dump(exclude_unset=True).items():
        setattr(db_manager, field, value)

    db.commit()
    db.refresh(db_manager)
    return db_manager

def delete_manager(db: Session, db_manager: Manager):
    db.delete(db_manager)
    db.commit()
