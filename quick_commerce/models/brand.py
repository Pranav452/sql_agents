"""Brand model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Brand(Base):
    __tablename__ = 'brands'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    logo_url = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="brand") 