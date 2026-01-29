from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from core.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="created")