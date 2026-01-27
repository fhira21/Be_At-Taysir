

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdateSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.put("/{product_id}")
def update_product(
    product_id: int,
    payload: ProductUpdateSchema,
    db: Session = Depends(get_db)
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    product.name = payload.name
    product.code = payload.code

    db.commit()
    db.refresh(product)
    return product
