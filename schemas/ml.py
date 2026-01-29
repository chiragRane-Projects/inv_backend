from pydantic import BaseModel

class DemandForecastRequest(BaseModel):
    warehouse_id: int
    product_id: int
    days: int = 7
    
class DemandPrediction(BaseModel):
    date: str
    predicted_demand: int