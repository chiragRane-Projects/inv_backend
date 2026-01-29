from fastapi import APIRouter, Depends, status, HTTPException
from models.warehouse import Warehouse
from schemas.warehouse import WarehouseCreate, WarehouseResponse
from core.dependencies import require_role, get_current_user
from core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Warehouse"],
    prefix="/warehouses"
)

@router.get("/", response_model=list[WarehouseResponse])
def get_warehouses(db: Session = Depends(get_db)):
    return db.query(Warehouse).all()

@router.post("/", response_model=WarehouseResponse, dependencies=[Depends(require_role("superadmin"))])
def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db)):
    warehouse = Warehouse(**data.model_dump())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse