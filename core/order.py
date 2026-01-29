from sqlalchemy.orm import Session
from models.order import Order
from models.order_item import OrderItem
from core.inventory import consume_inventory
from schemas.order import OrderCreate

def create_order(db: Session, data: OrderCreate):
    try:
        order = Order(warehouse_id=data.warehouse_id)
        db.add(order)
        
        db.flush()
        
        for item in data.items:
            consume_inventory(
                db,
                data.warehouse_id,
                item.product_id,
                item.quantity
            )
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(order_item)
            
            order.status = "confirmed"
            db.commit()
            return order
    
    except Exception:
        db.rollback()
        raise