from pydantic import BaseModel
from typing import List
from datetime import datetime

class BillItemCreate(BaseModel):
    particular_id: int
    quantity: float = 1

class BillCreate(BaseModel):
    customer_id: int
    items: List[BillItemCreate]

class BillItemResponse(BaseModel):
    particular_id: int
    quantity: float
    unit_price: float
    line_total: float

class BillResponse(BaseModel):
    id: int
    bill_number: int
    customer_id: int
    subtotal: float
    total: float
    created_at: datetime
    items: List[BillItemResponse]

    class Config:
        from_attributes = True
