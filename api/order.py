from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.order import OrderCreate, OrderResponse
from core.order import create_order
from core.dependencies import require_role

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, dependencies=[Depends(require_role("superadmin", "manager"))])
def place_order(data: OrderCreate, db : Session = Depends(get_db)):
    return create_order(db, data)