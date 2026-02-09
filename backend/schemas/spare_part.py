from pydantic import BaseModel, ConfigDict


class SparePartBase(BaseModel):
    name: str
    price: float
    quantity: int = 0


class SparePartCreate(SparePartBase):
    pass

class SparePartUpdate(BaseModel):
    name: str | None = None
    price: float | None = None  
    quantity: int | None = None

class SparePartResponse(SparePartBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
