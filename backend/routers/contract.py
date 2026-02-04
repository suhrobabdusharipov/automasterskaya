from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.crud.contract import (
    get_contract,
    get_contracts,
    create_contract,
    update_contract,
    delete_contract,
)
from backend.schemas.contract import ContractCreate, ContractUpdate

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.get("/")
def read_contracts(db: Session = Depends(get_db)):
    return get_contracts(db)


@router.get("/{contract_id}")
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return contract


@router.post("/")
def add_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    return create_contract(db, contract)


@router.put("/{contract_id}")
def edit_contract(
    contract_id: int, contract: ContractUpdate, db: Session = Depends(get_db)
):
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return update_contract(db, db_contract, contract)


@router.delete("/{contract_id}")
def remove_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = get_contract(db, contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    delete_contract(db, db_contract)
    return {"detail": "Договор удален"}
