from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, index=True)
    unit_price = Column(Float, nullable=False)