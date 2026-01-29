import joblib
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "ml/models/demand_model.pkl")
warehouse_encoder = joblib.load(BASE_DIR / "ml/models/warehouse_encoder.pkl")
product_encoder = joblib.load(BASE_DIR / "ml/models/product_encoder.pkl")

def build_features(warehouse_id, product_id, days):
    future_dates = [
        datetime.utcnow().date() + timedelta(days=i)
        for i in range(1, days + 1)
    ]
    
    df = pd.DataFrame({
        "date": future_dates
    })
    
    df["day"] = pd.to_datetime(df["date"]).dt.day
    df["month"] = pd.to_datetime(df["date"]).dt.month
    df["weekday"] = pd.to_datetime(df["date"]).dt.weekday
    df["is_weekend"] = df["weekday"].isin([5,6]).astype(int)
    
    df["warehouse_enc"] = warehouse_encoder.transform([warehouse_id])[0]
    df["product_enc"] = product_encoder.transform([product_id])[0]
    
    return df