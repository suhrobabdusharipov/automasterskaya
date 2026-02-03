from sqlalchemy.orm import Session
from models.client import Client
from schemas.client import ClientCreate, ClientUpdate


def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, db_client: Client, client: ClientUpdate):
    for field, value in client.model_dump(exclude_unset=True).items():
        setattr(db_client, field, value)

    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, db_client: Client):
    db.delete(db_client)
    db.commit()
