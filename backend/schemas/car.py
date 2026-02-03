from pydantic import BaseModel


class CarBase(BaseModel):
    client_id: int
    brand: str
    model: str
    year: int | None = None
    vin: str


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int

    class Config:
        orm_mode = True
