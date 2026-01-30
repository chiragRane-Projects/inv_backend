from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderCreate(BaseModel):
    warehouse_id: int
    items: List[OrderItemCreate]
    assigned_to: Optional[int] = None

class OrderResponse(BaseModel):
    id: int
    warehouse_id: int
    status: str
    order_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    total_amount: Optional[float] = 0.0
    
    class Config:
        from_attributes = True