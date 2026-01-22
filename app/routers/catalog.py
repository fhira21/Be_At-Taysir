from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.base_price import BasePrice
from app.models.sell_price import SellPrice
from app.models.supplier import Supplier
from app.dependencies.pin_auth import verify_pin
from sqlalchemy import or_

router = APIRouter(prefix="/catalog", tags=["Catalog"], dependencies=[Depends(verify_pin)])

@router.get("/search")
def search_product(q: str, db: Session = Depends(get_db)):
    keywords = q.lower().split()

    query = db.query(Product)

    for word in keywords:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{word}%"),
                Product.code.ilike(f"%{word}%")
            )
        )

    product = query.first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    sell_prices = (
        db.query(SellPrice)
        .filter(SellPrice.product_id == product.id)
        .all()
    )

    base_prices = (
        db.query(BasePrice, Supplier)
        .join(Supplier, BasePrice.supplier_id == Supplier.id)
        .filter(BasePrice.product_id == product.id)
        .all()
    )

    return {
        "product": {
            "id": product.id,
            "code": product.code,
            "name": product.name
        },
        "sell_prices": [
            {
                "price": sp.price,
                "unit": sp.unit
            } for sp in sell_prices
        ],
        "base_prices": [
            {
                "supplier": supplier.name,
                "price": bp.price,
                "unit": bp.unit,
                "note": bp.note
            } for bp, supplier in base_prices
        ]
    }

@router.get("/all")
def get_all_catalog(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    result = []

    for product in products:
        sell_price = (
            db.query(SellPrice)
            .filter(SellPrice.product_id == product.id)
            .first()
        )

        base_prices = (
            db.query(BasePrice, Supplier)
            .join(Supplier, BasePrice.supplier_id == Supplier.id)
            .filter(BasePrice.product_id == product.id)
            .all()
        )

        result.append({
            "id": product.id,
            "code": product.code,
            "name": product.name,
            "sell_price": {
                "price": sell_price.price,
                "unit": sell_price.unit
            } if sell_price else None,
            "base_prices": [
                {
                    "supplier": supplier.name,
                    "price": bp.price,
                    "unit": bp.unit
                }
                for bp, supplier in base_prices
            ]
        })

    return result
