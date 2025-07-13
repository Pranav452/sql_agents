"""Inventory model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from .base import Base


class Inventory(Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    quantity_available = Column(Integer, default=0)
    is_in_stock = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory")
    
    # Indexes
    __table_args__ = (
        Index('idx_inventory_product_platform', 'product_id', 'platform_id'),
    ) 