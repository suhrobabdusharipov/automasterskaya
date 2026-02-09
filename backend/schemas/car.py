from pydantic import BaseModel, ConfigDict


class CarBase(BaseModel):
    client_id: int
    brand: str
    model: str
    year: int | None = None
    vin: str


class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    vin: str | None = None

class CarResponse(CarBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)