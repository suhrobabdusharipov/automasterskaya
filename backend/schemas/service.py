from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    price: float


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int

    class Config:
        orm_mode = True
