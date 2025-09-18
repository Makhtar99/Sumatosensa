from pydantic import BaseModel

class SensorRenameRequest(BaseModel):
    name: str

class SensorResponse(BaseModel):
    id: int
    source_address: str
    name: str
    is_active: bool

    class Config:
        orm_mode = True