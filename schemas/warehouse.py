from pydantic import BaseModel

class WarehouseCreate(BaseModel):
    name: str
    location: str
    capacity: int
    
class WarehouseResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    
    class Config:
        from_attributes = True