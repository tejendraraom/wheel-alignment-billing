from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(Integer, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    subtotal = Column(Float, default=0)
    total = Column(Float, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer")
    items = relationship("BillItem", back_populates="bill", cascade="all, delete")
