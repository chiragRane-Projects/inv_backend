from fastapi import APIRouter, Depends, status, HTTPException
from models.warehouse import Warehouse
from schemas.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
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

@router.put("/{warehouse_id}", response_model=WarehouseResponse, dependencies=[Depends(require_role("superadmin"))])
def update_warehouse(warehouse_id: int, data: WarehouseUpdate, db: Session = Depends(get_db)):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(warehouse, field, value)
    
    db.commit()
    db.refresh(warehouse)
    return warehouse

@router.delete("/{warehouse_id}", dependencies=[Depends(require_role("superadmin"))])
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    db.delete(warehouse)
    db.commit()
    return {"message": "Warehouse deleted successfully"}