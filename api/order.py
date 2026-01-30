from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from core.database import get_db
from schemas.order import OrderCreate, OrderResponse
from core.order import create_order
from core.dependencies import require_role
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product)).all()
    
    # Calculate total amount for each order
    for order in orders:
        total_amount = 0
        for item in order.items:
            if item.product:
                total_amount += item.quantity * item.product.unit_price
        order.total_amount = total_amount
    
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/delivery-users/", dependencies=[Depends(require_role("superadmin", "manager"))])
def get_delivery_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "delivery").all()

@router.get("/{order_id}/items")
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).options(joinedload(OrderItem.product)).all()
    
    result = []
    for item in items:
        result.append({
            "product_id": item.product_id,
            "product_name": item.product.name if item.product else "Unknown Product",
            "quantity": item.quantity
        })
    
    return result

@router.post("/", response_model=OrderResponse, dependencies=[Depends(require_role("superadmin", "manager"))])
def place_order(data: OrderCreate, db : Session = Depends(get_db)):
    return create_order(db, data)

@router.put("/{order_id}/assign/{user_id}", dependencies=[Depends(require_role("superadmin", "manager"))])
def assign_order(order_id: int, user_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    user = db.query(User).filter(User.id == user_id, User.role == "delivery").first()
    if not user:
        raise HTTPException(status_code=404, detail="Delivery agent not found")
    
    order.assigned_to = user_id
    order.status = "assigned"
    db.commit()
    return {"message": "Order assigned successfully"}

@router.put("/{order_id}/status/{status}", dependencies=[Depends(require_role("superadmin", "manager", "delivery"))])
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    valid_statuses = ["created", "assigned", "picked_up", "in_transit", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    return {"message": f"Order status updated to {status}"}