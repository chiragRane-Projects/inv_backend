from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.inventory import InventoryCreate, InventoryResponse
from core.inventory import create_inventory
from core.dependencies import require_role

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)

@router.post("/", response_model=InventoryResponse, dependencies=[Depends(require_role("manager", "superadmin"))])
def add_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(db, data)