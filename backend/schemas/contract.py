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

class ContractUpdate(BaseModel):
    client_id: int | None = None
    car_id: int | None = None
    date: date  
    status: str | None = None
    total_amount: float | None = None   

class ContractResponse(ContractBase):
    id: int

    class Config:
        orm_mode = True
