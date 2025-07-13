"""Category model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    level = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Self-referential relationship
    parent = relationship("Category", remote_side=[id])
    products = relationship("Product", back_populates="category") 