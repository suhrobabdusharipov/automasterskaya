from sqlalchemy.orm import Session
from backend.models.service import Service
from backend.schemas.service import ServiceCreate, ServiceUpdate


def get_service(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()


def get_services(db: Session):
    return db.query(Service).all()


def create_service(db: Session, service: ServiceCreate):
    db_service = Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, db_service: Service, service: ServiceUpdate):
    for field, value in service.model_dump(exclude_unset=True).items():
        setattr(db_service, field, value)

    db.commit()
    db.refresh(db_service)
    return db_service


def delete_service(db: Session, db_service: Service):
    db.delete(db_service)
    db.commit()
