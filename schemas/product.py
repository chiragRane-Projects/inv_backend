from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: str
    unit_price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[float] = None
    
class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    unit_price: float

    class Config:
        from_attributes = True