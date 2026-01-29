from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.core.database import get_db
from app.models.particular import Particular
from app.schemas.particular import ParticularCreate, ParticularResponse


router = APIRouter(prefix="/particulars", tags=["Particulars"])


@router.post("/", response_model=ParticularResponse)
def create_particular(data: ParticularCreate, db: Session = Depends(get_db)):
    item = Particular(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=List[ParticularResponse])
def list_particulars(db: Session = Depends(get_db)):
    return db.query(Particular).filter(Particular.is_active == True).all()

@router.get("/search", response_model=list[ParticularResponse])
def search_particulars(
    q: str = Query(..., description="Search by particular name"),
    type: Optional[str] = Query(None, description="service or product"),
    db: Session = Depends(get_db),
):
    query = db.query(Particular).filter(
        Particular.is_active == True,
        Particular.name.ilike(f"%{q}%")
    )

    if type:
        query = query.filter(Particular.type == type)

    return query.all()
