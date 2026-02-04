from pydantic import BaseModel


class MasterBase(BaseModel):
    full_name: str
    specialization: str | None = None


class MasterCreate(MasterBase):
    pass

class MasterUpdate(BaseModel):
    full_name: str | None = None
    specialization: str | None = None

class MasterResponse(MasterBase):
    id: int

    class Config:
        orm_mode = True
