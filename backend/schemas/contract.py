from pydantic import BaseModel
from datetime import date


class ContractBase(BaseModel):
    client_id: int
    car_id: int
    date: date
    status: str
    total_amount: float = 0


class ContractCreate(ContractBase):
    pass


class ContractResponse(ContractBase):
    id: int

    class Config:
        orm_mode = True
