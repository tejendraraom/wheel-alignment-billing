from pydantic import BaseModel
from typing import List
from datetime import datetime

class BillItemCreate(BaseModel):
    particular_id: int
    quantity: float = 1
    unit_price: float

    class Config:
        json_schema_extra = {
            "example": {
                "particular_id": 1,
                "quantity": 2,
                "unit_price": 500,
            }
        }

class BillCreate(BaseModel):
    customer_id: int
    technician_id: int | None = None
    items: List[BillItemCreate]

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "technician_id": 1,
                "items": [
                    {"particular_id": 1, "quantity": 1, "unit_price": 700},
                    {"particular_id": 2, "quantity": 2, "unit_price": 250},
                ],
            }
        }

class BillItemResponse(BaseModel):
    particular_id: int
    quantity: float
    unit_price: float
    line_total: float


class CustomerMini(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TechnicianMini(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BillResponse(BaseModel):
    id: int
    bill_number: int
    customer_id: int
    technician_id: int | None = None
    customer: CustomerMini
    technician: TechnicianMini | None = None
    subtotal: float
    total: float
    created_at: datetime
    items: List[BillItemResponse]

    class Config:
        from_attributes = True
