from pydantic import BaseModel

class ProductBase(BaseModel):
    code: str
    name: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductUpdateSchema(BaseModel):
    code: str
    name: str