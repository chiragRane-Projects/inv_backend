from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from core.inventory import create_inventory
from core.dependencies import require_role
from models.inventory import Inventory

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)

@router.get("/", response_model=list[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@router.post("/", response_model=InventoryResponse, dependencies=[Depends(require_role("manager", "superadmin"))])
def add_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(db, data)

@router.put("/{inventory_id}", response_model=InventoryResponse, dependencies=[Depends(require_role("manager", "superadmin"))])
def update_inventory(inventory_id: int, data: InventoryUpdate, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(inventory, field, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

@router.delete("/{inventory_id}", dependencies=[Depends(require_role("manager", "superadmin"))])
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    db.delete(inventory)
    db.commit()
    return {"message": "Inventory deleted successfully"}