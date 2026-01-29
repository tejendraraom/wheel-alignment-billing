from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    particular_id = Column(Integer, ForeignKey("particulars.id"), nullable=False)

    quantity = Column(Float, default=1)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)

    bill = relationship("Bill", back_populates="items")
    particular = relationship("Particular")  # 👈 THIS LINE
