from pydantic import BaseModel

class InventoryCreate(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int
    reorder_level: int
    
class InventoryResponse(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reorder_level: int
    
    class Config:
        from_attributes = True