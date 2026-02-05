from sqlalchemy.orm import Session
from backend.models.contract import Contract
from backend.schemas.contract import ContractCreate, ContractUpdate


def get_contract(db: Session, contract_id: int):
    return db.query(Contract).filter(Contract.id == contract_id).first()


def get_contracts(db: Session):
    return db.query(Contract).all()


def create_contract(db: Session, contract: ContractCreate):
    db_contract = Contract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def update_contract(db: Session, db_contract: Contract, contract: ContractUpdate):
    for field, value in contract.model_dump(exclude_unset=True).items():
        setattr(db_contract, field, value)

    db.commit()
    db.refresh(db_contract)
    return db_contract


def delete_contract(db: Session, db_contract: Contract):
    db.delete(db_contract)
    db.commit()
