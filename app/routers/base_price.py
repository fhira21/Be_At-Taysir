from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.pin_auth import verify_pin
from app.models.base_price import BasePrice
from app.models.product import Product
from app.models.supplier import Supplier
from app.schemas.base_price import BasePriceCreate, BasePriceResponse, BasePriceUpdateSchema

router = APIRouter(
    prefix="/base-prices",
    tags=["Base Prices"],
    dependencies=[Depends(verify_pin)]
)

@router.post("/", response_model=BasePriceResponse)
def create_base_price(
    payload: BasePriceCreate,
    db: Session = Depends(get_db)
):
    # cek product
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # cek supplier
    supplier = db.query(Supplier).filter(Supplier.id == payload.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    base_price = BasePrice(
        product_id=payload.product_id,
        supplier_id=payload.supplier_id,
        price=payload.price,
        unit=payload.unit,
        note=payload.note
    )

    db.add(base_price)
    db.commit()
    db.refresh(base_price)

    return base_price


@router.get("/product/{product_id}", response_model=list[BasePriceResponse])
def get_base_price_by_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(BasePrice)
        .filter(BasePrice.product_id == product_id)
        .order_by(BasePrice.created_at.desc())
        .all()
    )

@router.put("/{base_price_id}")
def update_base_price(
    base_price_id: int,
    payload: BasePriceUpdateSchema,
    db: Session = Depends(get_db)
):
    price = db.query(BasePrice).get(base_price_id)
    if not price:
        raise HTTPException(404, "Base price not found")

    price.price = payload.price
    price.unit = payload.unit

    db.commit()
    db.refresh(price)
    return price
