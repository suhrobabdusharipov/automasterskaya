from pydantic import BaseModel


class ClientBase(BaseModel):
    full_name: str
    phone: str
    email: str | None = None
    address: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int

    class Config:
        orm_mode = True
