import pandas as pd
from core.database import DB_URL
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

engine = create_engine(DB_URL)

query = """
SELECT 
    warehouse_id,
    product_id,
    DATE(timestamp) AS date,
    ABS(SUM(change_qty)) AS demand
FROM inventory_logs
WHERE change_qty < 0
GROUP BY warehouse_id, product_id, DATE(timestamp)
ORDER BY date;
"""

df = pd.read_sql(query, engine)

df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.weekday
df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)

le_wh = LabelEncoder()
le_prod = LabelEncoder()

df["warehouse_enc"] = le_wh.fit_transform(df["warehouse_id"])
df["product_enc"] = le_prod.fit_transform(df["product_id"])

df = df.sort_values("date")

X = df[
    ["warehouse_enc", "product_enc", "day", "month", "weekday", "is_weekend"]
]

y = df["demand"]

split_idx = int(len(df) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)


preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print("MAE", mae)

joblib.dump(model, "ml/models/demand_model.pkl")
joblib.dump(le_wh, "ml/models/warehouse_encoder.pkl")
joblib.dump(le_prod, "ml/models/product_encoder.pkl")