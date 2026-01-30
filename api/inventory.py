from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.inventory import InventoryCreate, InventoryResponse
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