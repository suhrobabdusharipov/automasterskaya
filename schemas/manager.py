from pydantic import BaseModel


class ManagerBase(BaseModel):
    full_name: str
    contacts: str | None = None


class ManagerCreate(ManagerBase):
    pass


class ManagerResponse(ManagerBase):
    id: int

    class Config:
        orm_mode = True
