from pydantic import BaseModel
from datetime import datetime

class ParticularCreate(BaseModel):
    name: str
    type: str  # service | product
    unit_price: float

class ParticularResponse(BaseModel):
    id: int
    name: str
    type: str
    unit_price: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
