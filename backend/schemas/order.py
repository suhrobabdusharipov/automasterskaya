from pydantic import BaseModel
from datetime import date


class OrderBase(BaseModel):
    contract_id: int
    date: date
    services_description: str | None = None
    total_cost: float = 0


class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    contract_id: int | None = None
    date: date  
    services_description: str | None = None
    total_cost: float | None = None
    
class OrderResponse(OrderBase):
    id: int

    class Config:
        orm_mode = True
