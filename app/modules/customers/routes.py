from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(**data.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/search", response_model=List[CustomerResponse])
def search_customer(
    q: str = Query(..., description="Phone or vehicle number"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Customer)
        .filter(
            (Customer.phone_number.ilike(f"%{q}%"))
            | (Customer.vehicle_number.ilike(f"%{q}%"))
        )
        .all()
    )
