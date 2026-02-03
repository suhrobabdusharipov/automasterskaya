from pydantic import BaseModel


class SparePartBase(BaseModel):
    name: str
    price: float
    quantity: int = 0


class SparePartCreate(SparePartBase):
    pass


class SparePartResponse(SparePartBase):
    id: int

    class Config:
        orm_mode = True
