from pydantic import BaseModel
from app.models.enums import UnitEnum

class BasePriceCreate(BaseModel):
    product_id: int
    supplier_id: int
    price: int
    unit: UnitEnum
    note: str | None = None

class BasePriceResponse(BasePriceCreate):
    id: int

    class Config:
        from_attributes = True

class BasePriceUpdateSchema(BaseModel):
    price: float
    unit: UnitEnum