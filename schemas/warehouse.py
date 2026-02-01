from pydantic import BaseModel
from typing import Optional

class WarehouseCreate(BaseModel):
    name: str
    location: str
    capacity: int

class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    
class WarehouseResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    
    class Config:
        from_attributes = True