from sqlalchemy.orm import Session
from models.order import Order
from models.order_item import OrderItem
from core.inventory import consume_inventory
from schemas.order import OrderCreate
from fastapi import HTTPException
from datetime import datetime

def create_order(db: Session, data: OrderCreate):
    try:
        order = Order(
            warehouse_id=data.warehouse_id,
            order_date=datetime.now(),
            assigned_to=getattr(data, 'assigned_to', None)
        )
        db.add(order)
        db.flush()
        
        for item in data.items:
            # Check if inventory exists before consuming
            try:
                consume_inventory(
                    db,
                    data.warehouse_id,
                    item.product_id,
                    item.quantity
                )
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(order_item)
        
        order.status = "confirmed"
        db.commit()
        return order
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))