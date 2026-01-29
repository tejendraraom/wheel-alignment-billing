from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.technician import Technician
from app.schemas.technician import (
    TechnicianCreate,
    TechnicianUpdate,
    TechnicianResponse,
)

router = APIRouter(prefix="/technicians", tags=["Technicians"])


# CREATE
@router.post("/", response_model=TechnicianResponse)
def create_technician(
    data: TechnicianCreate,
    db: Session = Depends(get_db),
):
    tech = Technician(**data.dict())
    db.add(tech)
    db.commit()
    db.refresh(tech)
    return tech


# READ ALL (with optional search)
@router.get("/", response_model=List[TechnicianResponse])
def list_technicians(
    q: Optional[str] = Query(None, description="Search by name or phone"),
    db: Session = Depends(get_db),
):
    query = db.query(Technician)

    if q:
        query = query.filter(
            (Technician.name.ilike(f"%{q}%"))
            | (Technician.phone_number.ilike(f"%{q}%"))
        )

    return query.order_by(Technician.name).all()


# READ ONE
@router.get("/{technician_id}", response_model=TechnicianResponse)
def get_technician(
    technician_id: int,
    db: Session = Depends(get_db),
):
    tech = db.query(Technician).get(technician_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")
    return tech


# UPDATE
@router.put("/{technician_id}", response_model=TechnicianResponse)
def update_technician(
    technician_id: int,
    data: TechnicianUpdate,
    db: Session = Depends(get_db),
):
    tech = db.query(Technician).get(technician_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(tech, key, value)

    db.commit()
    db.refresh(tech)
    return tech


# SOFT DELETE (Deactivate)
@router.delete("/{technician_id}")
def deactivate_technician(
    technician_id: int,
    db: Session = Depends(get_db),
):
    tech = db.query(Technician).get(technician_id)
    if not tech:
        raise HTTPException(status_code=404, detail="Technician not found")

    tech.is_active = False
    db.commit()
    return {"success": True}
