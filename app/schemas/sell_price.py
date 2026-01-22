from pydantic import BaseModel
from app.models.enums import UnitEnum

class SellPriceCreate(BaseModel):
    product_id: int
    unit: UnitEnum
    price: int

class SellPriceResponse(SellPriceCreate):
    id: int

    class Config:
        from_attributes = True

class SellPriceUpdateSchema(BaseModel):
    price: float
    unit: UnitEnum