from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    contact: str | None = None
    note: str | None = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True
        
class SupplierUpdateSchema(BaseModel):
    name: str