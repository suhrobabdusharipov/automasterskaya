from pydantic import BaseModel


class MasterBase(BaseModel):
    full_name: str
    specialization: str | None = None


class MasterCreate(MasterBase):
    pass


class MasterResponse(MasterBase):
    id: int

    class Config:
        orm_mode = True
