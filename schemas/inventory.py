from pydantic import BaseModel
from typing import Optional

class InventoryCreate(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int
    reorder_level: int

class InventoryUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    reorder_level: Optional[int] = None
    
class InventoryResponse(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reorder_level: int
    
    class Config:
        from_attributes = True