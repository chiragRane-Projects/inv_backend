from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.reorder import recommend_reorder
from core.dependencies import require_role

router = APIRouter(
    prefix="/reorder",
    tags=["Reorder"]
)

@router.get("/recommendation", dependencies=[Depends(require_role("manager", "superadmin"))])
def get_reorder_recommendation(
    warehouse_id: int, product_id: int, db: Session = Depends(get_db)
):
    return recommend_reorder(db, warehouse_id, product_id)