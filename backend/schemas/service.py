from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    price: float


class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: str | None = None
    price: float | None = None  
    
class ServiceResponse(ServiceBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
