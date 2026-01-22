from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.pin_auth import verify_pin
from app.models.sell_price import SellPrice
from app.models.product import Product
from app.schemas.sell_price import SellPriceCreate, SellPriceResponse, SellPriceUpdateSchema

router = APIRouter(
    prefix="/sell-prices",
    tags=["Sell Prices"],
    dependencies=[Depends(verify_pin)]
)

@router.post("/", response_model=SellPriceResponse)
def create_sell_price(
    payload: SellPriceCreate,
    db: Session = Depends(get_db)
):
    # cek product
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # OPTIONAL: cegah unit ganda
    existing = (
        db.query(SellPrice)
        .filter(
            SellPrice.product_id == payload.product_id,
            SellPrice.unit == payload.unit
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Sell price for this unit already exists"
        )

    sell_price = SellPrice(
        product_id=payload.product_id,
        unit=payload.unit,
        price=payload.price
    )

    db.add(sell_price)
    db.commit()
    db.refresh(sell_price)

    return sell_price


@router.get("/product/{product_id}", response_model=list[SellPriceResponse])
def get_sell_price_by_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(SellPrice)
        .filter(SellPrice.product_id == product_id)
        .all()
    )

@router.put("/{sell_price_id}")
def update_sell_price(
    sell_price_id: int,
    payload: SellPriceUpdateSchema,
    db: Session = Depends(get_db)
):
    price = db.query(SellPrice).get(sell_price_id)
    if not price:
        raise HTTPException(404, "Sell price not found")

    price.price = payload.price
    price.unit = payload.unit

    db.commit()
    db.refresh(price)
    return price
