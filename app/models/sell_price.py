from sqlalchemy import Column, Integer, ForeignKey, Enum
from app.database import Base
from app.models.enums import UnitEnum

class SellPrice(Base):
    __tablename__ = "sell_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    unit = Column(Enum(UnitEnum, name="unit_enum"), nullable=False)
    price = Column(Integer, nullable=False)
