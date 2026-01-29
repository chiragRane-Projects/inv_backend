import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import (
    Warehouse, Product, Order, OrderItem,
    InventoryLog, Delivery, Inventory
)

random.seed(42)

print("=== SYNTHETIC DATA SCRIPT STARTED ===")

def generate_orders(days=180):
    db: Session = SessionLocal()

    try:
        warehouses = db.query(Warehouse).all()
        products = db.query(Product).all()

        if not warehouses or not products:
            raise ValueError("Warehouses or Products missing")

        start_date = datetime.utcnow() - timedelta(days=days)

        for day in range(days):
            current_date = start_date + timedelta(days=day)

            orders_today = random.randint(10, 20)
            if current_date.weekday() >= 5:
                orders_today += 10

            for _ in range(orders_today):
                warehouse = random.choice(warehouses)

                order = Order(
                    warehouse_id=warehouse.id,
                    order_date=current_date,
                    status="confirmed"
                )
                db.add(order)
                db.flush()  # get order.id

                items_added = 0

                items_count = random.randint(1, 5)
                chosen_products = random.sample(products, items_count)

                for product in chosen_products:
                    qty = random.randint(1, 5)

                    inventory = (
                        db.query(Inventory)
                        .filter_by(
                            warehouse_id=warehouse.id,
                            product_id=product.id
                        )
                        .with_for_update()
                        .first()
                    )

                    if not inventory or inventory.quantity < qty:
                        continue

                    inventory.quantity -= qty
                    items_added += 1

                    db.add(OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=qty
                    ))

                    db.add(InventoryLog(
                        warehouse_id=warehouse.id,
                        product_id=product.id,
                        change_qty=-qty,
                        timestamp=current_date,
                        reason="synthetic_order"
                    ))

                if items_added == 0:
                    db.delete(order)

            db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def generate_deliveries():
    db: Session = SessionLocal()

    try:
        orders = db.query(Order).all()

        for order in orders:
            distance = random.uniform(2, 30)
            expected_time = distance * random.uniform(3, 5)
            actual_time = expected_time * random.uniform(0.8, 1.3)

            db.add(Delivery(
                order_id=order.id,
                delivery_boy_id=random.randint(1, 5),
                distance_km=distance,
                expected_time=expected_time,
                actual_time=actual_time,
                status="delivered"
            ))

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

if __name__ == "__main__":
    generate_orders()
    generate_deliveries()
    print("=== SYNTHETIC DATA SCRIPT FINISHED ===")
