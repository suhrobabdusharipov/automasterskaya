from pydantic import BaseModel, ConfigDict


class ManagerBase(BaseModel):
    full_name: str
    contacts: str | None = None


class ManagerCreate(ManagerBase):
    pass

class ManagerUpdate(BaseModel):
    full_name: str | None = None
    contacts: str | None = None

class ManagerResponse(ManagerBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
