from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from app.core.database import get_db
from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.models.particular import Particular
from app.models.technician import Technician
from app.schemas.bill import BillCreate, BillResponse
from fastapi.responses import StreamingResponse
from app.utils.pdf import generate_invoice_pdf
from io import BytesIO


router = APIRouter(prefix="/bills", tags=["Billing"])


@router.get("/", response_model=List[BillResponse])
def list_bills(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    customer_id: Optional[int] = Query(None),
    technician_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Bill)
        .options(
            selectinload(Bill.items).selectinload(BillItem.particular),
            selectinload(Bill.customer),
            selectinload(Bill.technician),
        )
    )

    if customer_id is not None:
        query = query.filter(Bill.customer_id == customer_id)

    if technician_id is not None:
        query = query.filter(Bill.technician_id == technician_id)

    return (
        query.order_by(Bill.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = (
        db.query(Bill)
        .options(
            selectinload(Bill.items).selectinload(BillItem.particular),
            selectinload(Bill.customer),
            selectinload(Bill.technician),
        )
        .filter(Bill.id == bill_id)
        .first()
    )

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    return bill


@router.post("/", response_model=BillResponse)
def create_bill(data: BillCreate, db: Session = Depends(get_db)):
    # Generate bill number (simple version)
    last_bill = db.query(Bill).order_by(Bill.bill_number.desc()).first()
    bill_number = (last_bill.bill_number + 1) if last_bill else 1

    if data.technician_id is not None:
        technician = db.query(Technician).get(data.technician_id)
        if not technician:
            raise HTTPException(status_code=404, detail="Technician not found")
        if technician.is_active is False:
            raise HTTPException(status_code=400, detail="Technician is inactive")

    bill = Bill(
        bill_number=bill_number,
        customer_id=data.customer_id,
        technician_id=data.technician_id,
    )

    db.add(bill)
    db.flush()  # get bill.id

    subtotal = 0

    for item in data.items:
        particular = db.query(Particular).get(item.particular_id)
        if not particular:
            raise HTTPException(status_code=404, detail="Particular not found")

        unit_price = item.unit_price
        line_total = unit_price * item.quantity

        bill_item = BillItem(
            bill_id=bill.id,
            particular_id=particular.id,
            quantity=item.quantity,
            unit_price=unit_price,
            line_total=line_total,
        )
        db.add(bill_item)
        subtotal += line_total

    bill.subtotal = subtotal
    bill.total = subtotal  # tax later

    db.commit()
    bill = (
        db.query(Bill)
        .options(
            selectinload(Bill.items).selectinload(BillItem.particular),
            selectinload(Bill.customer),
            selectinload(Bill.technician),
        )
        .filter(Bill.id == bill.id)
        .first()
    )
    return bill

@router.get("/{bill_id}/pdf")
def download_bill_pdf(bill_id: int, db: Session = Depends(get_db)):
    bill = (
        db.query(Bill)
        .filter(Bill.id == bill_id)
        .first()
    )

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    pdf_bytes = generate_invoice_pdf(bill)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=bill_{bill.bill_number}.pdf"
        }
    )
