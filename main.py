from fastapi import FastAPI
from api.auth import router as auth_router
from api.warehouse import router as warehouse_router
from api.product import router as product_router
from api.inventory import router as inv_router
from api.order import router as order_router
from api.ml import router as ml_router

app = FastAPI(title="AI Logistics Platform")

app.include_router(auth_router)
app.include_router(warehouse_router)
app.include_router(product_router)
app.include_router(inv_router)
app.include_router(order_router)
app.include_router(ml_router)

@app.get("/")
def health_check():
    return {"message": "Welcome to AI Logistics Platform API"}