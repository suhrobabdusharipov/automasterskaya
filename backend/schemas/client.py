from pydantic import BaseModel, ConfigDict


class ClientBase(BaseModel):
    full_name: str
    phone: str
    email: str | None = None
    address: str | None = None


class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    full_name: str | None = None    
    phone: str | None = None
    email: str | None = None
    address: str | None = None

class ClientResponse(ClientBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
