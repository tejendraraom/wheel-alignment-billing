from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TechnicianCreate(BaseModel):
    name: str
    phone_number: Optional[str] = None

class TechnicianUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

class TechnicianResponse(BaseModel):
    id: int
    name: str
    phone_number: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
