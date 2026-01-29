from pydantic import BaseModel
from typing import List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderCreate(BaseModel):
    warehouse_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    warehouse_id: int
    status: str
    
    class Config:
        from_attributes = True