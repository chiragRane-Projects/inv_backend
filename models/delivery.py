from sqlalchemy import Column, Integer, ForeignKey, Float, String
from core.database import Base

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    delivery_boy_id = Column(Integer, ForeignKey("users.id"))
    distance_km = Column(Float)
    expected_time = Column(Float)
    actual_time = Column(Float)
    status = Column(String, default="pending") 