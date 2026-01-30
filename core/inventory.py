from sqlalchemy.orm import Session
from models.inventory import Inventory
from models.inventory_log import InventoryLog

def create_inventory(db: Session, data):
    inventory = Inventory(**data.model_dump())
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    
    log = InventoryLog(
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        change_qty=data.quantity,
        reason="initial_stock"
    )
    
    db.add(log)
    db.commit()
    
    return inventory

def consume_inventory(db: Session, warehouse_id: int, product_id: int, qty: int):
    inventory = db.query(Inventory).filter_by(
        warehouse_id=warehouse_id,
        product_id=product_id
    ).first()
    
    if not inventory:
        raise Exception(f"No inventory found for product {product_id} in warehouse {warehouse_id}")
    
    if inventory.quantity < qty:
        raise Exception(f"Insufficient stock. Available: {inventory.quantity}, Requested: {qty}")
    
    inventory.quantity -= qty
    
    log = InventoryLog(
        warehouse_id=warehouse_id,
        product_id=product_id,
        change_qty=-qty,
        reason="consumption"
    )
    
    db.add(log)
    db.commit()
    
def refill_inventory(db: Session, warehouse_id: int, product_id: int, qty: int):
    inventory = db.query(Inventory).filter_by(
        warehouse_id=warehouse_id,
        product_id=product_id
    ).first()
    
    inventory.quantity += qty
    
    log = InventoryLog(
        warehouse_id=warehouse_id,
        product_id=product_id,
        change_qty=qty,
        reason="refill"
    )
    db.add(log)
    db.commit()