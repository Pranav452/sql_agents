"""Discount model for Quick Commerce"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from .base import Base


class Discount(Base):
    __tablename__ = 'discounts'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    discount_type = Column(String(20))  # percentage, fixed, bogo
    discount_value = Column(Float)
    min_quantity = Column(Integer, default=1)
    max_quantity = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="discounts")
    
    # Indexes
    __table_args__ = (
        Index('idx_discount_product_platform', 'product_id', 'platform_id'),
        Index('idx_discount_dates', 'start_date', 'end_date'),
    ) 