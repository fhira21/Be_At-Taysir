from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.pin_auth import verify_pin
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdateSchema

router = APIRouter(prefix="/suppliers", tags=["Suppliers"],dependencies=[Depends(verify_pin)])

@router.post("/", response_model=SupplierResponse)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.get("/", response_model=list[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.put("/{supplier_id}")
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdateSchema,
    db: Session = Depends(get_db)
):
    supplier = db.query(Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(404, "Supplier not found")

    supplier.name = payload.name

    db.commit()
    db.refresh(supplier)
    return supplier
