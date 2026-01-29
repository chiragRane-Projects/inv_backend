from fastapi import APIRouter
from schemas.ml import DemandForecastRequest
from ml.demand_model import model, build_features

router = APIRouter(prefix="/ml", tags=["ML"])

@router.post("/demand_forecast")
def forecast_demand(data: DemandForecastRequest):
    df = build_features(
        data.warehouse_id,
        data.product_id,
        data.days
    )
    
    preds = model.predict(df[
        ["warehouse_enc", "product_enc", "day", "month", "weekday", "is_weekend"]
    ])
    
    results = []
    
    for i, p in enumerate(preds):
        results.append({
            "date": str(df.iloc[i]["date"]),
            "predicted_demand": int(round(p))
        })
    
    
    return {
        "warehouse_id": data.warehouse_id,
        "product_id": data.product_id,
        "predictions": results
    }
