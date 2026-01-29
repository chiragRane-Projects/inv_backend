from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductResponse
from core.dependencies import require_role

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_product(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product