from fastapi import FastAPI
from app.database import Base, engine

from app.models.product import Product
from app.models.supplier import Supplier
from app.models.sell_price import SellPrice
from app.models.base_price import BasePrice
from app.models.enums import UnitEnum
from app.routers import product
from app.routers import supplier
from app.routers import sell_price
from app.routers import base_price
from app.routers import catalog

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(product.router)
app.include_router(supplier.router)
app.include_router(sell_price.router)
app.include_router(base_price.router)
app.include_router(catalog.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # untuk development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend + PostgreSQL via pgAdmin siap 🎉"}