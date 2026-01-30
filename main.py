from fastapi import FastAPI
from api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from api.warehouse import router as warehouse_router
from api.product import router as product_router
from api.inventory import router as inv_router
from api.order import router as order_router
from api.ml import router as ml_router
from api.reorder import router as reorder_router

app = FastAPI(title="AI Logistics Platform")

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(warehouse_router)
app.include_router(product_router)
app.include_router(inv_router)
app.include_router(order_router)
app.include_router(ml_router)
app.include_router(reorder_router)

@app.get("/")
def health_check():
    return {"message": "Welcome to AI Logistics Platform API"}