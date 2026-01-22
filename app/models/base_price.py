from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import UnitEnum

class BasePrice(Base):
    __tablename__ = "base_prices"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)

    price = Column(Integer, nullable=False)
    unit = Column(Enum(UnitEnum, name="unit_enum"), nullable=False)
    note = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
