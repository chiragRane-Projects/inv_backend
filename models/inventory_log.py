from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from core.database import Base

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    change_qty = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reason = Column(String)