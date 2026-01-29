from sqlalchemy.orm import Session
from models.inventory import Inventory
from ml.demand_model import model, build_features
import math

def recommend_reorder(
    db: Session,
    warehouse_id: int,
    product_id: int,
    forecast_days: int = 7,
    lead_time: int = 3
):
    inventory = db.query(Inventory).filter_by(
        warehouse_id=warehouse_id, product_id=product_id
    ).first()
    
    if not inventory:
        raise Exception("Inventory not found")
    
    df = build_features(warehouse_id, product_id, forecast_days)
    preds = model.predict(df[
        ["warehouse_enc", "product_enc", "day", "month", "weekday", "is_weekend"]
    ])
    
    avg_daily_demand = preds.mean()
    lead_time_demand = avg_daily_demand * lead_time
    safety_stock = 0.2 * lead_time_demand
    reorder_point = lead_time_demand * safety_stock
    
    forecast_total = preds.sum()
    reorder_qty = max(0, math.ceil(forecast_total - inventory.quantity))
    
    return {
        "current_stock": inventory.quantity,
        "avg_daily_demand": round(avg_daily_demand, 2),
        "reorder_point": math.ceil(reorder_point),
        "recommended_quantity": reorder_qty
    }