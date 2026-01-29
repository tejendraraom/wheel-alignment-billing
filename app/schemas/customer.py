from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    vehicle_number: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    vehicle_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
